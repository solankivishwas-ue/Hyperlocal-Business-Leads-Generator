"""Local Business Leads Generator backend — US/Europe Edition.

Upgrades over original:
  P1 – Email enrichment via Hunter.io (falls back to website scrape, then demo)
  P2 – Global geography: free-text city/area, no India-only restrictions
  P3 – Lead quality scoring (0-100), sorted descending in output
  P4 – Dynamic filename, summary stats, input validation

CLI:
    python main.py

Django:
    from main import run_lead_generation
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
CLEANED_DATA_DIR = BASE_DIR / "cleaned_data"
OUTPUT_DIR = BASE_DIR / "output"

# ---------------------------------------------------------------------------
# Output columns (P1 adds Email + Email Source; P3 adds Lead Score)
# ---------------------------------------------------------------------------

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
    "Email",
    "Email Source",
    "Lead Score",
]

# ---------------------------------------------------------------------------
# CLI defaults (Django sends these dynamically)
# ---------------------------------------------------------------------------

KEYWORD = "Marketing Agencies"
AREA = "Downtown"
CITY = "Austin, Texas"
MAX_RESULTS = 50

# ---------------------------------------------------------------------------
# P3 — Lead scoring weights (tune these constants to adjust formula)
# ---------------------------------------------------------------------------

SCORE_WEIGHT_RATING = 30          # 0-30 pts: Google rating contribution
SCORE_WEIGHT_REVIEWS = 25         # 0-25 pts: log-scaled review count
SCORE_WEIGHT_WEBSITE = 20         # 0/20 pts: has a website URL
SCORE_WEIGHT_EMAIL = 25           # 0/25 pts: email found and verified

SCORE_REVIEW_SCALE = 500          # review count at which log score is maximised
SCORE_MAX_RATING = 5.0            # max possible Google rating

"""
Lead Score formula (0–100):
  rating_score  = (rating / MAX_RATING)  * WEIGHT_RATING          [0–30]
  review_score  = (log(reviews+1) / log(SCALE+1)) * WEIGHT_REVIEWS [0–25]
  website_score = WEIGHT_WEBSITE if website else 0                 [0–20]
  email_score   = WEIGHT_EMAIL   if email found else 0             [0–25]
  total         = sum of above, clipped to [0, 100]

Clients can be told: "Scores reflect rating quality, social proof (log-
scaled so 50 reviews isn't worthless next to 5000), digital presence
(website), and contact reachability (email)."
"""

# ---------------------------------------------------------------------------
# Environment / config
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def load_environment_file() -> None:
    """Load KEY=value pairs from .env — always overrides stale environment values."""
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
        os.environ[key] = value   # always override — ensures new .env token is used


load_environment_file()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "").strip()
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "compass/crawler-google-places")
APIFY_TIMEOUT_SECONDS = 180
MAX_RESULTS_LIMIT = int(os.getenv("MAX_RESULTS_LIMIT", "1000"))

# P1 — Hunter.io
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "").strip()
HUNTER_BASE_URL = "https://api.hunter.io/v2"
HUNTER_RATE_LIMIT_DELAY = 1.2   # seconds between Hunter calls (free tier ~10/min)

APIFY_OUTPUT_FIELDS = ",".join([
    "title", "name", "businessName",
    "categoryName", "category", "type",
    "address", "street", "fullAddress",
    "phone", "phoneNumber", "contactPhone",
    "website", "webUrl",
    "totalScore", "rating", "stars",
    "reviewsCount", "reviewCount",
    "url", "googleMapsUrl", "placeUrl", "searchPageUrl",
])

# ---------------------------------------------------------------------------
# P2 — Global geography helpers (no hardcoded India state map)
# ---------------------------------------------------------------------------

# Kept for backward-compat if Django dropdown still uses Indian presets.
CITY_STATE_MAP: dict[str, str] = {
    "Ahmedabad": "Gujarat", "Surat": "Gujarat", "Vadodara": "Gujarat",
    "Rajkot": "Gujarat", "Gandhinagar": "Gujarat", "Mumbai": "Maharashtra",
    "Pune": "Maharashtra", "Nagpur": "Maharashtra", "Nashik": "Maharashtra",
    "Delhi": "Delhi", "Noida": "Uttar Pradesh", "Gurugram": "Haryana",
    "Bengaluru": "Karnataka", "Hyderabad": "Telangana", "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal", "Jaipur": "Rajasthan", "Lucknow": "Uttar Pradesh",
    "Indore": "Madhya Pradesh", "Bhopal": "Madhya Pradesh",
    "Chandigarh": "Chandigarh", "Kochi": "Kerala", "Coimbatore": "Tamil Nadu",
    "Visakhapatnam": "Andhra Pradesh",
}

GENERIC_KEYWORD_WORDS = {
    "a", "an", "and", "best", "business", "center", "centre", "clinic",
    "clinics", "company", "near", "service", "services", "shop", "shops",
    "store", "stores", "the",
}

KEYWORD_MATCH_TERMS: dict[str, list[str]] = {
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
    "marketing agencies": ["marketing", "agency", "advertising", "digital", "branding"],
    "software companies": ["software", "tech", "technology", "it company", "developer"],
    "accounting firms": ["accounting", "accountant", "cpa", "bookkeep", "audit"],
    "plumbers": ["plumb", "pipe", "drain"],
    "electricians": ["electric", "wiring", "electrical"],
}

LOCATION_KEYS = [
    "address", "street", "fullAddress", "neighborhood",
    "city", "state", "postalCode", "locatedIn",
]
TYPE_KEYS = [
    "title", "name", "businessName", "categoryName", "category", "type",
    "categories", "types",
]

# ---------------------------------------------------------------------------
# Query building (P2 — works for any world city)
# ---------------------------------------------------------------------------


def build_search_query(keyword: str, area: str, city: str) -> str:
    """Build a hyper-local Google Maps search query for any city worldwide.

    Area is optional — if empty the query searches the whole city.
    For known Indian cities the state is appended for precision.
    """
    clean_area = area.strip()
    clean_city = city.strip()

    state = CITY_STATE_MAP.get(clean_city)
    location = f"{clean_area}, {clean_city}" if clean_area else clean_city
    if state and state.lower() not in clean_city.lower():
        location = f"{location}, {state}"

    return f"{keyword.strip()} in {location}".strip()


# ---------------------------------------------------------------------------
# Text normalisation helpers (unchanged)
# ---------------------------------------------------------------------------


def normalize_search_text(value: Any) -> str:
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
    return normalize_search_text([record.get(key, "") for key in keys])


def contains_term(text: str, term: str) -> bool:
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


# ---------------------------------------------------------------------------
# P2 — Location filtering works the same for US/UK cities
# ---------------------------------------------------------------------------


def record_matches_location(record: dict[str, Any], area: str, city: str) -> bool:
    """Keep only records local to the requested city (and area if provided).

    Area is optional — when empty only the city is checked so the search
    covers the entire city without neighbourhood filtering.
    """
    location_text = build_record_text(record, LOCATION_KEYS)
    title_text = build_record_text(record, ["title", "name", "businessName"])
    combined_text = f"{location_text} {title_text}".strip()

    # Always check city match
    city_tokens = [t.strip() for t in city.split(",") if t.strip()]
    city_match = any(contains_term(combined_text, tok) for tok in city_tokens)

    # Only check area when one was specified
    if area.strip():
        area_match = contains_term(combined_text, area)
        return area_match and city_match

    return city_match


def record_matches_keyword(record: dict[str, Any], keyword: str) -> bool:
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
    return [
        record for record in records
        if record_matches_location(record, area, city)
        and record_matches_keyword(record, keyword)
    ]


# ---------------------------------------------------------------------------
# Folder helpers
# ---------------------------------------------------------------------------


def ensure_folders() -> None:
    RAW_DATA_DIR.mkdir(exist_ok=True)
    CLEANED_DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# P2 — Demo mode: works for any city (not India-specific)
# ---------------------------------------------------------------------------


def build_demo_businesses(
    keyword: str, area: str, city: str, max_results: int
) -> list[dict[str, Any]]:
    """Create realistic demo rows for any world city."""
    clean_keyword = keyword.strip() or "Businesses"
    clean_area = area.strip() or "Downtown"
    clean_city = city.strip() or "Austin, Texas"
    base_query = quote_plus(f"{clean_keyword} {clean_area} {clean_city}")

    name_patterns = [
        "{area} {keyword} Group",
        "Premier {keyword} {city}",
        "{city} {keyword} Studio",
        "Trusted {keyword} Partners",
        "Local {keyword} Experts",
        "Urban {keyword} Co.",
        "NextGen {keyword}",
        "{area} Business Hub",
        "Elite {keyword} Services",
        "Metro {keyword} Works",
        "{keyword} Solutions {area}",
        "Innovative {keyword} Agency",
    ]

    demo_rows = []
    for index in range(1, max_results + 1):
        pattern = name_patterns[(index - 1) % len(name_patterns)]
        name = pattern.format(
            keyword=clean_keyword, area=clean_area, city=clean_city.split(",")[0]
        )
        if index > len(name_patterns):
            name = f"{name} {index}"
        name = f"{name} [DEMO]"

        rating = round(3.5 + (index % 15) * 0.1, 1)
        reviews = 20 + index * 17

        demo_rows.append({
            "title": name,
            "categoryName": clean_keyword,
            "address": f"{index * 10 + 100} Main St, {clean_area}, {clean_city}",
            "phone": f"+1 512-{500 + index:03d}-{1000 + index:04d}",
            "website": f"https://example-{index}.com",
            "totalScore": rating,
            "reviewsCount": reviews,
            "url": f"https://www.google.com/maps/search/?api=1&query={base_query}&idx={index}",
            # Pre-populate demo email fields
            "_demo_email": f"info@example-{index}.com" if index % 3 != 0 else "",
            "_demo_email_source": "Hunter.io verified" if index % 3 == 1 else (
                "website scrape" if index % 3 == 2 else "not found"
            ),
        })

    return demo_rows


# ---------------------------------------------------------------------------
# Apify fetch
# ---------------------------------------------------------------------------


def fetch_google_maps_leads(
    search_query: str,
    max_results: int,
    keyword: str,
    area: str,
    city: str,
) -> tuple[list[dict[str, Any]], str]:
    if not APIFY_API_TOKEN:
        return build_demo_businesses(keyword, area, city, max_results), "demo"

    safe_actor_id = APIFY_ACTOR_ID.replace("/", "~")
    endpoint = (
        f"https://api.apify.com/v2/acts/{safe_actor_id}/run-sync-get-dataset-items"
    )

    params = {
        "token": APIFY_API_TOKEN,
        "timeout": APIFY_TIMEOUT_SECONDS,
        "clean": "true",
        "fields": APIFY_OUTPUT_FIELDS,
    }

    # P2: do NOT hardcode countryCode="in" — let the search query specify location
    payload = {
        "searchStringsArray": [search_query],
        "maxCrawledPlacesPerSearch": max_results,
        "language": "en",
        "skipClosedPlaces": False,
    }

    response = requests.post(
        endpoint, params=params, json=payload,
        timeout=APIFY_TIMEOUT_SECONDS + 30,
    )

    if not response.ok:
        try:
            error_details = response.json()
            error_msg = error_details.get("error", {}).get("message", response.text)
        except ValueError:
            error_msg = response.text

        # 402 = billing limit exceeded, 429 = rate limited → fall back to demo
        if response.status_code in (402, 429):
            log.warning(
                "Apify returned %s (%s) — falling back to demo mode.",
                response.status_code, error_msg,
            )
            return build_demo_businesses(keyword, area, city, max_results), "demo"

        raise RuntimeError(f"Apify API returned {response.status_code}: {error_msg}")

    return response.json(), "live"


# ---------------------------------------------------------------------------
# P1 — Email enrichment
# ---------------------------------------------------------------------------


def extract_domain(url: str) -> str:
    """Parse a business website URL and return the bare domain."""
    if not url:
        return ""
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        domain = parsed.netloc or parsed.path
        domain = domain.lower().lstrip("www.").split("/")[0]
        return domain
    except Exception:
        return ""


def hunter_domain_search(domain: str) -> tuple[str, str]:
    """Call Hunter.io Domain Search API and return (email, source_label).

    Prefers role-based emails (info@, contact@, hello@) over personal ones.
    Returns ("", "not found") on failure or missing key.
    """
    if not HUNTER_API_KEY or not domain:
        return "", "not found"

    try:
        resp = requests.get(
            f"{HUNTER_BASE_URL}/domain-search",
            params={"domain": domain, "api_key": HUNTER_API_KEY},
            timeout=10,
        )
        if not resp.ok:
            log.warning("Hunter domain-search %s → HTTP %s", domain, resp.status_code)
            return "", "not found"

        data = resp.json().get("data", {})
        emails = data.get("emails", [])
        if not emails:
            return "", "not found"

        # Prefer role-based / generic inboxes
        role_prefixes = ("info", "contact", "hello", "sales", "admin", "support")
        for entry in emails:
            addr = entry.get("value", "")
            prefix = addr.split("@")[0].lower()
            if prefix in role_prefixes:
                confidence = entry.get("confidence", 0)
                verified = entry.get("verification", {}).get("status") == "valid"
                label = "Hunter.io verified" if verified else f"Hunter.io ({confidence}% confidence)"
                return addr, label

        # Fall back to first email Hunter found
        first = emails[0]
        addr = first.get("value", "")
        confidence = first.get("confidence", 0)
        verified = first.get("verification", {}).get("status") == "valid"
        label = "Hunter.io verified" if verified else f"Hunter.io ({confidence}% confidence)"
        return addr, label

    except Exception as exc:
        log.warning("Hunter domain-search error for %s: %s", domain, exc)
        return "", "not found"


def scrape_website_email(url: str) -> tuple[str, str]:
    """Scrape a business contact page for a mailto: or visible email address.

    This is the fallback when Hunter.io is not configured or returns nothing.
    """
    if not url:
        return "", "not found"

    targets = [url.rstrip("/")]
    for suffix in ("/contact", "/contact-us", "/about"):
        targets.append(url.rstrip("/") + suffix)

    email_pattern = re.compile(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    )

    for target in targets:
        try:
            resp = requests.get(
                target, timeout=8,
                headers={"User-Agent": "Mozilla/5.0 (compatible; LeadBot/1.0)"},
            )
            if not resp.ok:
                continue
            matches = email_pattern.findall(resp.text)
            # Filter out image/script noise
            clean = [
                m for m in matches
                if not any(m.lower().endswith(ext) for ext in (".png", ".jpg", ".gif", ".js", ".css"))
            ]
            if clean:
                return clean[0], "website scrape"
        except Exception:
            pass

    return "", "not found"


def enrich_email(website: str, is_demo: bool = False,
                 demo_email: str = "", demo_source: str = "") -> tuple[str, str]:
    """Return (email, source) for a lead, using Hunter → scrape → not found."""
    if is_demo:
        return demo_email, demo_source

    if not website:
        return "", "not found"

    domain = extract_domain(website)

    # Path 1: Hunter.io
    if HUNTER_API_KEY and domain:
        email, source = hunter_domain_search(domain)
        if email:
            time.sleep(HUNTER_RATE_LIMIT_DELAY)
            return email, source

    # Path 2: website scrape
    email, source = scrape_website_email(website)
    if email:
        return email, source

    return "", "not found"


def enrich_batch(
    records: list[dict[str, Any]],
    is_demo: bool,
    include_email: bool = True,
) -> list[dict[str, Any]]:
    """Add Email / Email Source to each record dict."""
    if not include_email:
        for rec in records:
            rec["_email"] = ""
            rec["_email_source"] = "skipped"
        return records

    for i, rec in enumerate(records):
        website = rec.get("website") or rec.get("webUrl") or ""
        demo_email = rec.get("_demo_email", "")
        demo_source = rec.get("_demo_email_source", "not found")

        email, source = enrich_email(
            website, is_demo=is_demo,
            demo_email=demo_email, demo_source=demo_source,
        )
        rec["_email"] = email
        rec["_email_source"] = source

        if (i + 1) % 10 == 0:
            log.info("Email enrichment: %d / %d done", i + 1, len(records))

    return records


# ---------------------------------------------------------------------------
# P3 — Lead scoring
# ---------------------------------------------------------------------------


def compute_lead_score(
    rating: float,
    review_count: int,
    has_website: bool,
    has_email: bool,
) -> int:
    """Compute a 0-100 lead quality score.

    rating_score  = (rating / MAX_RATING) * WEIGHT_RATING
    review_score  = log(reviews+1) / log(SCALE+1) * WEIGHT_REVIEWS
    website_score = WEIGHT_WEBSITE if website present
    email_score   = WEIGHT_EMAIL   if email found
    """
    try:
        rating_f = max(0.0, min(float(rating), SCORE_MAX_RATING))
    except (TypeError, ValueError):
        rating_f = 0.0

    try:
        reviews_i = max(0, int(review_count))
    except (TypeError, ValueError):
        reviews_i = 0

    rating_score = (rating_f / SCORE_MAX_RATING) * SCORE_WEIGHT_RATING
    review_score = (
        math.log(reviews_i + 1) / math.log(SCORE_REVIEW_SCALE + 1)
    ) * SCORE_WEIGHT_REVIEWS
    website_score = SCORE_WEIGHT_WEBSITE if has_website else 0
    email_score = SCORE_WEIGHT_EMAIL if has_email else 0

    total = rating_score + review_score + website_score + email_score
    return int(round(min(100, max(0, total))))


# ---------------------------------------------------------------------------
# JSON / CSV helpers
# ---------------------------------------------------------------------------


def save_raw_json(records: list[dict[str, Any]], search_query: str, mode: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = RAW_DATA_DIR / f"google_maps_raw_{timestamp}.json"
    payload = {
        "search_query": search_query,
        "mode": mode,
        "record_count": len(records),
        "records": records,
    }
    with raw_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return raw_file


def clean_phone_number(phone: Any) -> str:
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
    for key in keys:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def _extract_area_from_record(record: dict[str, Any]) -> str:
    """Extract a neighbourhood/area name from a Google Maps record.

    Tries dedicated fields first (neighborhood, locatedIn), then falls back
    to parsing the second comma-separated token of the full address, which
    Apify typically populates with the suburb/district name.
    Returns an empty string if nothing useful is found.
    """
    # Direct neighbourhood fields returned by Apify / Google Maps
    for key in ("neighborhood", "neighbourhood", "locatedIn", "district", "subLocality"):
        val = record.get(key, "")
        if val and isinstance(val, str) and val.strip():
            return val.strip()

    # Fall back to second token of the address  e.g. "12 Main St, Koramangala, Bengaluru"
    address = first_available(record, ["fullAddress", "address", "street"])
    if address and isinstance(address, str):
        parts = [p.strip() for p in address.split(",")]
        # parts[0] = street, parts[1] = neighbourhood (usually), parts[-1] = country
        if len(parts) >= 3:          # at least street + area + city
            return parts[1]
        if len(parts) == 2:          # street + city — not specific enough, skip
            return ""

    return ""


def normalize_record(record: dict[str, Any], area: str) -> dict[str, Any]:
    """Map Apify/Google Maps + enrichment fields into the final lead columns."""
    category = first_available(record, ["categoryName", "category", "type"])
    if isinstance(category, list):
        category = ", ".join(str(item) for item in category)

    website = first_available(record, ["website", "webUrl"])
    rating = first_available(record, ["totalScore", "rating", "stars"])
    reviews = first_available(record, ["reviewsCount", "reviewCount", "reviews"])
    email = record.get("_email", "")
    email_source = record.get("_email_source", "not found")

    # P3 — score
    try:
        rating_f = float(rating)
    except (TypeError, ValueError):
        rating_f = 0.0
    try:
        reviews_i = int(reviews)
    except (TypeError, ValueError):
        reviews_i = 0

    score = compute_lead_score(
        rating=rating_f,
        review_count=reviews_i,
        has_website=bool(website),
        has_email=bool(email),
    )

    return {
        "Business Name": first_available(record, ["title", "name", "businessName"]),
        "Category": category,
        "Area": area or _extract_area_from_record(record),
        "Address": first_available(record, ["address", "street", "fullAddress"]),
        "Phone Number": clean_phone_number(
            first_available(record, ["phone", "phoneNumber", "contactPhone"])
        ),
        "Website": website,
        "Google Rating": rating,
        "Review Count": reviews,
        "Google Maps URL": first_available(
            record, ["url", "googleMapsUrl", "placeUrl", "searchPageUrl"]
        ),
        "Email": email,
        "Email Source": email_source,
        "Lead Score": score,
    }


def clean_leads(records: list[dict[str, Any]], area: str) -> pd.DataFrame:
    """Clean, deduplicate, score, and sort business records."""
    normalized_rows = [normalize_record(record, area) for record in records]
    df = pd.DataFrame(normalized_rows, columns=FINAL_COLUMNS)
    df = df.fillna("")
    for column in FINAL_COLUMNS:
        if column not in ("Google Rating", "Review Count", "Lead Score"):
            df[column] = df[column].astype(str).str.strip()

    df = df[df["Business Name"] != ""]
    df = df.drop_duplicates(subset=["Business Name", "Address"], keep="first")

    # P3 — sort by Lead Score descending
    df = df.sort_values(by="Lead Score", ascending=False, kind="stable").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# P4 — Dynamic filename + export
# ---------------------------------------------------------------------------


def make_filename(keyword: str, city: str) -> str:
    """Return a clean filename slug like leads_marketing-agencies_austin_20260623."""
    date_str = datetime.now().strftime("%Y%m%d")
    slug = re.sub(r"[^a-z0-9]+", "-", keyword.lower().strip()).strip("-")
    city_slug = re.sub(r"[^a-z0-9]+", "-", city.lower().split(",")[0].strip()).strip("-")
    return f"leads_{slug}_{city_slug}_{date_str}.csv"


def export_csv(df: pd.DataFrame, keyword: str, city: str) -> tuple[Path, Path]:
    """Export to cleaned_data (fixed name) and output (dynamic name).

    Phone numbers are prefixed with a tab character so Excel/Sheets treats them
    as text and never strips the leading '+' or converts to scientific notation.
    QUOTE_ALL ensures every field is quoted in the CSV for maximum compatibility.
    """
    import csv

    cleaned_file = CLEANED_DATA_DIR / "cleaned_business_leads.csv"
    output_filename = make_filename(keyword, city)
    output_file = OUTPUT_DIR / output_filename

    # Force phone number column to string and prefix with tab so Excel
    # treats it as text (prevents +49... → 4.9E+10 scientific notation).
    export_df = df.copy()
    if "Phone Number" in export_df.columns:
        export_df["Phone Number"] = (
            export_df["Phone Number"]
            .astype(str)
            .apply(lambda v: "\t" + v if v and v != "nan" else v)
        )

    export_df.to_csv(
        cleaned_file, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL
    )
    export_df.to_csv(
        output_file, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL
    )
    return cleaned_file, output_file


# ---------------------------------------------------------------------------
# P4 — Summary stats
# ---------------------------------------------------------------------------


def compute_summary_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Return a dict of quality stats for the dashboard summary panel."""
    total = len(df)
    if total == 0:
        return {
            "total_leads": 0,
            "pct_with_email": 0,
            "pct_with_website": 0,
            "avg_rating": 0,
            "avg_score": 0,
        }

    has_email = df["Email"].astype(str).str.strip().ne("").sum()
    has_website = df["Website"].astype(str).str.strip().ne("").sum()

    try:
        ratings = pd.to_numeric(df["Google Rating"], errors="coerce").dropna()
        avg_rating = round(float(ratings.mean()), 2) if len(ratings) else 0
    except Exception:
        avg_rating = 0

    try:
        avg_score = round(float(df["Lead Score"].mean()), 1)
    except Exception:
        avg_score = 0

    return {
        "total_leads": total,
        "pct_with_email": round(has_email / total * 100, 1),
        "pct_with_website": round(has_website / total * 100, 1),
        "avg_rating": avg_rating,
        "avg_score": avg_score,
    }


# ---------------------------------------------------------------------------
# P4 — Input validation
# ---------------------------------------------------------------------------


def validate_inputs(keyword: str, area: str, city: str, max_results: int) -> None:
    """Raise ValueError with a clear message if any required input is bad.

    Area is optional — an empty string means search the whole city.
    """
    errors = []
    if not keyword or not keyword.strip():
        errors.append("Keyword is required (e.g. 'Marketing Agencies').")
    if not city or not city.strip():
        errors.append("City is required (e.g. 'Austin, Texas').")
    if not isinstance(max_results, int) or max_results < 1:
        errors.append("Max results must be a positive integer.")
    if errors:
        raise ValueError(" | ".join(errors))


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def run_lead_generation(
    keyword: str,
    area: str,
    city: str,
    max_results: int = MAX_RESULTS,
    include_email: bool = True,
) -> dict[str, Any]:
    """Run the full lead generation workflow.

    Parameters
    ----------
    keyword       : business type (e.g. 'Marketing Agencies')
    area          : neighbourhood / district (e.g. 'Downtown')
    city          : city, optionally with state/country (e.g. 'Austin, Texas')
    max_results   : how many places to request from Apify
    include_email : whether to run email enrichment (P1, adds cost + time)
    """
    ensure_folders()

    # P4 — validate inputs
    max_results = max(1, min(int(max_results), MAX_RESULTS_LIMIT))
    validate_inputs(keyword, area, city, max_results)

    keyword = keyword.strip()
    area = area.strip()
    city = city.strip()

    # Fetch
    search_query = build_search_query(keyword, area, city)
    records, mode = fetch_google_maps_leads(search_query, max_results, keyword, area, city)
    raw_file = save_raw_json(records, search_query, mode)

    # P2 — filter (works for any world city)
    filtered_records = filter_relevant_records(records, keyword, area, city)

    # P1 — email enrichment
    is_demo = (mode == "demo")
    enriched_records = enrich_batch(filtered_records, is_demo=is_demo, include_email=include_email)

    # Clean + score + sort
    clean_df = clean_leads(enriched_records, area)

    # P4 — export with dynamic filename
    cleaned_file, output_file = export_csv(clean_df, keyword, city)

    # P4 — summary stats
    stats = compute_summary_stats(clean_df)

    return {
        "search_query": search_query,
        "mode": mode,
        "raw_record_count": len(records),
        "filtered_out_count": len(records) - len(filtered_records),
        "record_count": len(clean_df),
        "raw_file": raw_file,
        "cleaned_file": cleaned_file,
        "output_file": output_file,
        "output_filename": output_file.name,
        "dataframe": clean_df,
        "leads": clean_df.to_dict("records"),
        "stats": stats,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    result = run_lead_generation(KEYWORD, AREA, CITY, MAX_RESULTS, include_email=True)
    mode = result["mode"]

    if mode == "demo":
        print("\n[DEMO MODE] No APIFY_API_TOKEN found — using sample data.\n")

    print(f"Search query : {result['search_query']}")
    print(f"Mode         : {mode}")
    print(f"Raw records  : {result['raw_record_count']}")
    print(f"Filtered out : {result['filtered_out_count']}")
    print(f"Leads saved  : {result['record_count']}")
    print(f"Raw JSON     : {result['raw_file']}")
    print(f"Cleaned CSV  : {result['cleaned_file']}")
    print(f"Output CSV   : {result['output_file']}")

    stats = result["stats"]
    print("\n--- Summary Stats ---")
    print(f"  Total leads       : {stats['total_leads']}")
    print(f"  With email        : {stats['pct_with_email']}%")
    print(f"  With website      : {stats['pct_with_website']}%")
    print(f"  Avg Google Rating : {stats['avg_rating']}")
    print(f"  Avg Lead Score    : {stats['avg_score']}/100")


if __name__ == "__main__":
    main()
