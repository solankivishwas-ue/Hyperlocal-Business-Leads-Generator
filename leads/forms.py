from __future__ import annotations

from django import forms


CUSTOM_KEYWORD_VALUE = "__custom__"
CUSTOM_CITY_VALUE = "__custom_city__"
CUSTOM_AREA_VALUE = "__custom_area__"

KEYWORD_PRESETS = [
    "Dental Clinics",
    "Gyms",
    "Restaurants",
    "Salons",
    "Doctors",
    "Hospitals",
    "Real Estate Agents",
    "Interior Designers",
    "Cafes",
    "Coaching Classes",
    "Car Repair Shops",
    "Law Firms",
    "Chartered Accountants",
    "Pet Clinics",
    "Boutiques",
    "Schools",
    "Colleges",
    "Pharmacies",
    "Diagnostic Labs",
    "Physiotherapy Clinics",
    "Event Planners",
    "Packers and Movers",
    "Digital Marketing Agencies",
]

CITY_AREA_MAP = {
    "Ahmedabad": [
        "Ranip",
        "Paldi",
        "Satellite",
        "Navrangpura",
        "Bodakdev",
        "Maninagar",
        "Vastrapur",
        "Thaltej",
        "Naranpura",
        "Bopal",
        "Prahlad Nagar",
        "Chandkheda",
        "Gota",
        "Memnagar",
        "Ambawadi",
        "Shahibaug",
        "Nikol",
        "Naroda",
    ],
    "Surat": [
        "Adajan",
        "Vesu",
        "Varachha",
        "City Light",
        "Katargam",
        "Piplod",
        "Rander",
        "Athwa",
        "Udhna",
        "Pal",
        "Althan",
        "Nanpura",
    ],
    "Vadodara": [
        "Alkapuri",
        "Gotri",
        "Manjalpur",
        "Fatehgunj",
        "Akota",
        "Karelibaug",
        "Sayajigunj",
        "Waghodia Road",
        "Vasna Road",
        "Subhanpura",
    ],
    "Rajkot": [
        "Kalawad Road",
        "Yagnik Road",
        "150 Feet Ring Road",
        "Raiya Road",
        "University Road",
        "Gondal Road",
        "Mavdi",
        "Kotecha Nagar",
    ],
    "Gandhinagar": [
        "Sector 11",
        "Sector 21",
        "Sector 26",
        "Kudasan",
        "Sargasan",
        "Raysan",
        "Infocity",
        "Pethapur",
    ],
    "Mumbai": [
        "Andheri",
        "Bandra",
        "Borivali",
        "Dadar",
        "Ghatkopar",
        "Powai",
        "Thane",
        "Vashi",
        "Malad",
        "Chembur",
        "Lower Parel",
        "Mulund",
        "Kandivali",
    ],
    "Pune": [
        "Kothrud",
        "Baner",
        "Wakad",
        "Hinjewadi",
        "Viman Nagar",
        "Koregaon Park",
        "Hadapsar",
        "Aundh",
        "Shivaji Nagar",
        "Kharadi",
        "Magarpatta",
    ],
    "Delhi": [
        "Connaught Place",
        "Karol Bagh",
        "Lajpat Nagar",
        "Rohini",
        "Saket",
        "Dwarka",
        "Janakpuri",
        "Hauz Khas",
        "Pitampura",
        "Greater Kailash",
    ],
    "Bengaluru": [
        "Indiranagar",
        "Koramangala",
        "Whitefield",
        "Jayanagar",
        "HSR Layout",
        "Marathahalli",
        "Electronic City",
        "BTM Layout",
        "Hebbal",
        "Yelahanka",
        "Rajajinagar",
    ],
    "Hyderabad": [
        "Banjara Hills",
        "Jubilee Hills",
        "Madhapur",
        "Hitech City",
        "Gachibowli",
        "Kondapur",
        "Secunderabad",
        "Kukatpally",
        "Ameerpet",
        "Begumpet",
    ],
    "Chennai": [
        "T Nagar",
        "Anna Nagar",
        "Adyar",
        "Velachery",
        "Porur",
        "Mylapore",
        "OMR",
        "Tambaram",
        "Nungambakkam",
        "Guindy",
    ],
    "Kolkata": [
        "Salt Lake",
        "Park Street",
        "Ballygunge",
        "New Town",
        "Howrah",
        "Dum Dum",
        "Garia",
        "Behala",
        "Rajarhat",
    ],
    "Jaipur": [
        "Malviya Nagar",
        "Vaishali Nagar",
        "Mansarovar",
        "C Scheme",
        "Raja Park",
        "Tonk Road",
        "Jagatpura",
        "Sodala",
    ],
    "Lucknow": [
        "Gomti Nagar",
        "Hazratganj",
        "Aliganj",
        "Indira Nagar",
        "Aminabad",
        "Mahanagar",
        "Vikas Nagar",
    ],
    "Indore": [
        "Vijay Nagar",
        "Palasia",
        "Bhawarkuan",
        "Rau",
        "MG Road",
        "Sapna Sangeeta",
        "Scheme 78",
    ],
    "Bhopal": [
        "MP Nagar",
        "Arera Colony",
        "Kolar Road",
        "New Market",
        "Bairagarh",
        "Gulmohar Colony",
        "Hoshangabad Road",
    ],
    "Nagpur": [
        "Dharampeth",
        "Sitabuldi",
        "Manish Nagar",
        "Sadar",
        "Ramdaspeth",
        "Wardha Road",
        "Hingna",
    ],
    "Nashik": [
        "Gangapur Road",
        "College Road",
        "Panchavati",
        "Indira Nagar",
        "Satpur",
        "Cidco",
        "Nashik Road",
    ],
    "Chandigarh": [
        "Sector 17",
        "Sector 22",
        "Sector 35",
        "Sector 43",
        "Manimajra",
        "Zirakpur",
        "Mohali",
    ],
    "Noida": [
        "Sector 18",
        "Sector 62",
        "Sector 63",
        "Sector 75",
        "Sector 137",
        "Greater Noida",
        "Noida Extension",
    ],
    "Gurugram": [
        "Cyber City",
        "MG Road",
        "Sector 14",
        "Sector 29",
        "Golf Course Road",
        "Sohna Road",
        "DLF Phase 1",
        "DLF Phase 3",
    ],
    "Kochi": [
        "Edappally",
        "Kakkanad",
        "MG Road",
        "Panampilly Nagar",
        "Vyttila",
        "Fort Kochi",
        "Kaloor",
    ],
    "Coimbatore": [
        "RS Puram",
        "Gandhipuram",
        "Peelamedu",
        "Saibaba Colony",
        "Singanallur",
        "Race Course",
        "Saravanampatti",
    ],
    "Visakhapatnam": [
        "MVP Colony",
        "Dwaraka Nagar",
        "Gajuwaka",
        "Madhurawada",
        "Beach Road",
        "Seethammadhara",
        "Akkayyapalem",
    ],
}


def city_choices() -> list[tuple[str, str]]:
    return [(city, city) for city in CITY_AREA_MAP] + [
        (CUSTOM_CITY_VALUE, "Custom city")
    ]


def area_choices_for_city(city: str) -> list[tuple[str, str]]:
    areas = CITY_AREA_MAP.get(city, [])
    return [(area, area) for area in areas] + [(CUSTOM_AREA_VALUE, "Custom area")]


class LeadSearchForm(forms.Form):
    keyword_choice = forms.ChoiceField(
        label="Keyword",
        choices=[(keyword, keyword) for keyword in KEYWORD_PRESETS]
        + [(CUSTOM_KEYWORD_VALUE, "Custom keyword")],
        initial="Dental Clinics",
        widget=forms.Select,
    )
    custom_keyword = forms.CharField(
        label="Custom Keyword",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: Pediatric Dentists",
                "autocomplete": "off",
            }
        ),
    )
    city = forms.ChoiceField(
        label="City",
        choices=city_choices(),
        initial="Ahmedabad",
        widget=forms.Select,
    )
    custom_city = forms.CharField(
        label="Custom City",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: Udaipur",
                "autocomplete": "off",
            }
        ),
    )
    area = forms.ChoiceField(
        label="Area",
        choices=[],
        initial="Ranip",
        widget=forms.Select,
    )
    custom_area = forms.CharField(
        label="Custom Area",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: Hiran Magri",
                "autocomplete": "off",
            }
        ),
    )
    max_results = forms.IntegerField(
        label="Max Results",
        min_value=1,
        max_value=1000,
        initial=100,
        widget=forms.NumberInput(attrs={"step": "1"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_city = "Ahmedabad"
        if self.is_bound:
            selected_city = self.data.get("city", selected_city)
        elif self.initial.get("city"):
            selected_city = self.initial["city"]

        self.fields["area"].choices = area_choices_for_city(selected_city)

    def clean(self):
        cleaned_data = super().clean()
        keyword_choice = cleaned_data.get("keyword_choice")
        custom_keyword = (cleaned_data.get("custom_keyword") or "").strip()
        city_choice = cleaned_data.get("city")
        custom_city = (cleaned_data.get("custom_city") or "").strip()
        area_choice = cleaned_data.get("area")
        custom_area = (cleaned_data.get("custom_area") or "").strip()

        if keyword_choice == CUSTOM_KEYWORD_VALUE:
            if not custom_keyword:
                self.add_error("custom_keyword", "Enter a custom keyword.")
            else:
                cleaned_data["keyword"] = custom_keyword
        else:
            cleaned_data["keyword"] = keyword_choice

        if city_choice == CUSTOM_CITY_VALUE:
            if not custom_city:
                self.add_error("custom_city", "Enter a custom city.")
            else:
                cleaned_data["city"] = custom_city
        else:
            cleaned_data["city"] = city_choice

        if city_choice == CUSTOM_CITY_VALUE or area_choice == CUSTOM_AREA_VALUE:
            if not custom_area:
                self.add_error("custom_area", "Enter a custom area.")
            else:
                cleaned_data["area"] = custom_area
        else:
            cleaned_data["area"] = area_choice

        return cleaned_data
