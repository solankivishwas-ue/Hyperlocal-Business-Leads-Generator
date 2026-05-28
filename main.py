"""Local Business Leads Generator backend.

This file can run as a CLI script and can also be imported by Django.

CLI:
    python main.py

Django:
    from main import run_lead_generation
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
CLEANED_DATA_DIR = BASE_DIR / "cleaned_data"
OUTPUT_DIR = BASE_DIR / "output"

FINAL_COLUMNS = [
    "Business Name",
    "Category",
    "Area",
    "Address",
    "Phone Number",
    "Website",
    "Google Rating",
    "Review Count",
    "Google Maps URL",
]


# Easy CLI defaults. The Django frontend sends these dynamically from the form.
KEYWORD = "Dental Clinics"
AREA = "Ranip"
CITY = "Ahmedabad"
MAX_RESULTS = 250


def load_environment_file() -> None:
    """Load simple KEY=value pairs from .env without requiring extra packages."""
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_environment_file()


APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "").strip()
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "compass/crawler-google-places")
APIFY_TIMEOUT_SECONDS = 180
MAX_RESULTS_LIMIT = int(os.getenv("MAX_RESULTS_LIMIT", "1000"))
APIFY_OUTPUT_FIELDS = ",".join(
    [
        "title",
        "name",
        "businessName",
        "categoryName",
        "category",
        "type",
        "address",
        "street",
        "fullAddress",
        "phone",
        "phoneNumber",
        "contactPhone",
        "website",
        "webUrl",
        "totalScore",
        "rating",
        "stars",
        "reviewsCount",
        "reviewCount",
        "reviews",
        "url",
        "googleMapsUrl",
        "placeUrl",
        "searchPageUrl",
    ]
)

CITY_STATE_MAP = {
    "Ahmedabad": "Gujarat",
    "Surat": "Gujarat",
    "Vadodara": "Gujarat",
    "Rajkot": "Gujarat",
    "Gandhinagar": "Gujarat",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Nagpur": "Maharashtra",
    "Nashik": "Maharashtra",
    "Delhi": "Delhi",
    "Noida": "Uttar Pradesh",
    "Gurugram": "Haryana",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh",
    "Indore": "Madhya Pradesh",
    "Bhopal": "Madhya Pradesh",
    "Chandigarh": "Chandigarh",
    "Kochi": "Kerala",
    "Coimbatore": "Tamil Nadu",
    "Visakhapatnam": "Andhra Pradesh",
}

GENERIC_KEYWORD_WORDS = {
    "a",
    "an",
    "and",
    "best",
    "business",
    "center",
    "centre",
    "clinic",
    "clinics",
    "company",
    "near",
    "service",
    "services",
    "shop",
    "shops",
    "store",
    "stores",
    "the",
}

KEYWORD_MATCH_TERMS = {
    "dental clinics": ["dental", "dentist", "orthodont", "endodont", "periodont"],
    "gyms": ["gym", "fitness", "health club", "workout", "crossfit"],
    "restaurants": ["restaurant", "dining", "food", "cafe", "bistro"],
    "salons": ["salon", "beauty", "hair", "spa"],
    "doctors": ["doctor", "physician", "medical practitioner"],
    "hospitals": ["hospital", "medical center", "medical centre"],
    "real estate agents": ["real estate", "property dealer", "realtor", "broker"],
    "interior designers": ["interior", "designer", "decor"],
    "cafes": ["cafe", "coffee", "bakery"],
    "coaching classes": ["coaching", "tuition", "classes", "academy", "institute"],
    "car repair shops": ["car repair", "auto repair", "garage", "mechanic"],
    "law firms": ["law", "lawyer", "advocate", "legal"],
    "chartered accountants": ["chartered accountant", "ca firm", "accountant"],
    "pet clinics": ["pet", "veterinary", "vet", "animal hospital"],
    "boutiques": ["boutique", "fashion", "clothing"],
}

LOCATION_KEYS = [
    "address",
    "street",
    "fullAddress",
    "neighborhood",
    "city",
    "state",
    "postalCode",
    "locatedIn",
]

TYPE_KEYS = [
    "title",
    "name",
    "businessName",
    "categoryName",
    "category",
    "type",
    "categories",
    "types",
]


def build_search_query(keyword: str, area: str, city: str) -> str:
    """Build a hyper-local Google Maps search query."""
    clean_area = area.strip()
    clean_city = city.strip()
    state = CITY_STATE_MAP.get(clean_city)
    location = f"{clean_area}, {clean_city}"
    if state:
        location = f"{location}, {state}"

    return f"{keyword.strip()} in {location}".strip()


def normalize_search_text(value: Any) -> str:
    """Convert nested API values into lowercase searchable text."""
    if value is None:
        return ""
    if isinstance(value, dict):
        value = " ".join(normalize_search_text(item) for item in value.values())
    elif isinstance(value, list):
        value = " ".join(normalize_search_text(item) for item in value)
    else:
        value = str(value)

    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def build_record_text(record: dict[str, Any], keys: list[str]) -> str:
    """Build searchable text from selected fields in a Google Maps record."""
    return normalize_search_text([record.get(key, "") for key in keys])


def contains_term(text: str, term: str) -> bool:
    """Match normalized words or exact normalized phrases."""
    normalized_term = normalize_search_text(term)
    if not normalized_term:
        return False

    if " " in normalized_term:
        return f" {normalized_term} " in f" {text} "

    words = text.split()
    return any(
        word == normalized_term
        or word == f"{normalized_term}s"
        or (len(normalized_term) >= 5 and word.startswith(normalized_term))
        for word in words
    )


def keyword_terms(keyword: str) -> list[str]:
    """Build business-type terms used to reject unrelated categories."""
    normalized_keyword = normalize_search_text(keyword)
    preset_terms = KEYWORD_MATCH_TERMS.get(normalized_keyword)
    if preset_terms:
        return preset_terms

    terms = []
    for token in normalized_keyword.split():
        if token in GENERIC_KEYWORD_WORDS or len(token) < 3:
            continue

        terms.append(token)
        if token.endswith("s") and len(token) > 4:
            terms.append(token[:-1])

    return list(dict.fromkeys(terms))


def record_matches_location(record: dict[str, Any], area: str, city: str) -> bool:
    """Keep only records that still look local to the selected area and city."""
    location_text = build_record_text(record, LOCATION_KEYS)
    title_text = build_record_text(record, ["title", "name", "businessName"])
    combined_text = f"{location_text} {title_text}".strip()

    return contains_term(combined_text, area) and contains_term(combined_text, city)


def record_matches_keyword(record: dict[str, Any], keyword: str) -> bool:
    """Keep only records whose name/category still matches the requested niche."""
    type_text = build_record_text(record, TYPE_KEYS)
    terms = keyword_terms(keyword)

    if not terms:
        return True

    return any(contains_term(type_text, term) for term in terms)


def filter_relevant_records(
    records: list[dict[str, Any]],
    keyword: str,
    area: str,
    city: str,
) -> list[dict[str, Any]]:
    """Reject broad Google Maps results from other areas, cities, or niches."""
    return [
        record
        for record in records
        if record_matches_location(record, area, city)
        and record_matches_keyword(record, keyword)
    ]


def ensure_folders() -> None:
    """Create output folders if they are missing."""
    RAW_DATA_DIR.mkdir(exist_ok=True)
    CLEANED_DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)


def build_demo_businesses(
    keyword: str,
    area: str,
    city: str,
    max_results: int,
) -> list[dict[str, Any]]:
    """Create realistic demo rows that match the user's search inputs."""
    clean_keyword = keyword.strip() or "Businesses"
    clean_area = area.strip() or "Local Area"
    clean_city = city.strip() or "City"
    clean_state = CITY_STATE_MAP.get(clean_city, "India")
    base_query = quote_plus(f"{clean_keyword} {clean_area} {clean_city}")
    name_patterns = [
        "{area} {keyword} Hub",
        "Prime {keyword} {area}",
        "{city} {keyword} Studio",
        "Trusted {keyword} Center",
        "Local {keyword} Point",
        "Urban {keyword} House",
        "NextGen {keyword}",
        "{area} Business Center",
        "Elite {keyword} Services",
        "Metro {keyword} Works",
    ]

    demo_rows = []
    for index in range(1, max_results + 1):
        local_phone = str(7000000000 + index)
        pattern = name_patterns[(index - 1) % len(name_patterns)]
        name = pattern.format(
            keyword=clean_keyword,
            area=clean_area,
            city=clean_city,
        )
        if index > len(name_patterns):
            name = f"{name} {index}"
        name = f"{name} - Sample"

        demo_rows.append(
            {
                "title": name,
                "categoryName": clean_keyword,
                "address": f"Business Road {index}, {clean_area}, {clean_city}, {clean_state}",
                "phone": f"+91 {local_phone[:5]} {local_phone[5:]}",
                "website": f"https://example.com/{quote_plus(name.lower()).replace('+', '-')}",
                "totalScore": round(4.0 + (index % 10) * 0.1, 1),
                "reviewsCount": 40 + index * 19,
                "url": f"https://www.google.com/maps/search/?api=1&query={base_query}",
            }
        )

    return demo_rows


def fetch_google_maps_leads(
    search_query: str,
    max_results: int,
    keyword: str,
    area: str,
    city: str,
) -> tuple[list[dict[str, Any]], str]:
    """Fetch Google Maps leads using Apify, or demo rows when no token exists."""
    if not APIFY_API_TOKEN:
        return build_demo_businesses(keyword, area, city, max_results), "demo"

    import requests

    safe_actor_id = APIFY_ACTOR_ID.replace("/", "~")
    endpoint = f"https://api.apify.com/v2/acts/{safe_actor_id}/run-sync-get-dataset-items"
    
    params = {
        "token": APIFY_API_TOKEN,
        "timeout": APIFY_TIMEOUT_SECONDS,
        "clean": "true",
        "fields": APIFY_OUTPUT_FIELDS,
    }
    
    payload = {
        "searchStringsArray": [search_query],
        "maxCrawledPlacesPerSearch": max_results,
        "language": "en",
        "countryCode": "in",  # Must be lowercase
        "skipClosedPlaces": False, 
    }

    response = requests.post(
        endpoint,
        params=params,
        json=payload,
        timeout=APIFY_TIMEOUT_SECONDS + 30,
    )
    
    if not response.ok:
        try:
            error_details = response.json()
            # Navigate the specific Apify error structure
            error_msg = error_details.get("error", {}).get("message", response.text)
        except ValueError:
            error_msg = response.text
        raise RuntimeError(f"Apify API returned {response.status_code}: {error_msg}")

    data = response.json()
    return data, "live"



def save_raw_json(records: list[dict[str, Any]], search_query: str, mode: str) -> Path:
    """Save the raw API response for transparency and future debugging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = RAW_DATA_DIR / f"google_maps_raw_{timestamp}.json"
    payload = {
        "search_query": search_query,
        "mode": mode,
        "record_count": len(records),
        "records": records,
    }

    with raw_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return raw_file


def clean_phone_number(phone: Any) -> str:
    """Normalize phone numbers while preserving an international + prefix."""
    if phone is None or pd.isna(phone):
        return ""

    phone_text = str(phone).strip()
    if not phone_text:
        return ""

    has_plus = phone_text.startswith("+")
    digits = re.sub(r"\D", "", phone_text)

    if not digits:
        return ""
    return f"+{digits}" if has_plus else digits


def first_available(record: dict[str, Any], keys: list[str], default: Any = "") -> Any:
    """Return the first non-empty value from a list of possible API field names."""
    for key in keys:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def normalize_record(record: dict[str, Any], area: str) -> dict[str, Any]:
    """Map Apify/Google Maps fields into the final lead dataset columns."""
    category = first_available(record, ["categoryName", "category", "type"])
    if isinstance(category, list):
        category = ", ".join(str(item) for item in category)

    return {
        "Business Name": first_available(record, ["title", "name", "businessName"]),
        "Category": category,
        "Area": area,
        "Address": first_available(record, ["address", "street", "fullAddress"]),
        "Phone Number": clean_phone_number(
            first_available(record, ["phone", "phoneNumber", "contactPhone"])
        ),
        "Website": first_available(record, ["website", "webUrl"]),
        "Google Rating": first_available(record, ["totalScore", "rating", "stars"]),
        "Review Count": first_available(record, ["reviewsCount", "reviewCount", "reviews"]),
        "Google Maps URL": first_available(
            record,
            ["url", "googleMapsUrl", "placeUrl", "searchPageUrl"],
        ),
    }


def clean_leads(records: list[dict[str, Any]], area: str) -> pd.DataFrame:
    """Clean, deduplicate, and structure raw business records."""
    normalized_rows = [normalize_record(record, area) for record in records]
    df = pd.DataFrame(normalized_rows, columns=FINAL_COLUMNS)

    df = df.fillna("")
    for column in FINAL_COLUMNS:
        df[column] = df[column].astype(str).str.strip()

    df = df[df["Business Name"] != ""]
    df = df.drop_duplicates(subset=["Business Name", "Address"], keep="first")
    df = df.sort_values(by=["Business Name"], kind="stable").reset_index(drop=True)

    return df


def export_csv(df: pd.DataFrame) -> tuple[Path, Path]:
    """Export the clean dataset to both cleaned_data and output folders."""
    cleaned_file = CLEANED_DATA_DIR / "cleaned_business_leads.csv"
    output_file = OUTPUT_DIR / "business_leads.csv"

    df.to_csv(cleaned_file, index=False, encoding="utf-8-sig")
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    return cleaned_file, output_file


def run_lead_generation(
    keyword: str,
    area: str,
    city: str,
    max_results: int = MAX_RESULTS,
) -> dict[str, Any]:
    """Run the full lead generation workflow for dynamic search inputs."""
    ensure_folders()

    max_results = max(1, min(int(max_results), MAX_RESULTS_LIMIT))
    keyword = keyword.strip()
    area = area.strip()
    city = city.strip()

    if not keyword or not area or not city:
        raise ValueError("Keyword, area, and city are required.")

    search_query = build_search_query(keyword, area, city)
    records, mode = fetch_google_maps_leads(search_query, max_results, keyword, area, city)
    raw_file = save_raw_json(records, search_query, mode)

    filtered_records = filter_relevant_records(records, keyword, area, city)
    clean_df = clean_leads(filtered_records, area)
    cleaned_file, output_file = export_csv(clean_df)

    return {
        "search_query": search_query,
        "mode": mode,
        "raw_record_count": len(records),
        "filtered_out_count": len(records) - len(filtered_records),
        "record_count": len(clean_df),
        "raw_file": raw_file,
        "cleaned_file": cleaned_file,
        "output_file": output_file,
        "dataframe": clean_df,
        "leads": clean_df.to_dict("records"),
    }


def main() -> None:
    result = run_lead_generation(KEYWORD, AREA, CITY, MAX_RESULTS)

    if result["mode"] == "demo":
        print("No APIFY_API_TOKEN found. Using keyword-aware sample demo data.")

    print(f"Search query: {result['search_query']}")
    print(f"Raw JSON saved to: {result['raw_file']}")
    print(f"Cleaned CSV saved to: {result['cleaned_file']}")
    print(f"Final CSV saved to: {result['output_file']}")
    print(f"Raw records fetched: {result['raw_record_count']}")
    print(f"Filtered out: {result['filtered_out_count']}")
    print(f"Total leads exported: {result['record_count']}")


if __name__ == "__main__":
    main()
