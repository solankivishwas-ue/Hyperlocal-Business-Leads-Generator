"""Django forms for the lead generation dashboard.

Cascading location dropdowns: Country → State (optional) → City → Area (optional).
State and Area are intentionally not required — users may want to search an
entire city without narrowing to a specific neighbourhood.
"""

from django import forms

# ---------------------------------------------------------------------------
# Keyword presets
# ---------------------------------------------------------------------------

KEYWORD_CHOICES = [
    ("", "— Select or type a keyword —"),
    # General
    ("Restaurants", "Restaurants"),
    ("Cafes", "Cafes"),
    ("Gyms", "Gyms"),
    ("Salons", "Salons"),
    ("Boutiques", "Boutiques"),
    # Professional
    ("Dental Clinics", "Dental Clinics"),
    ("Doctors", "Doctors"),
    ("Hospitals", "Hospitals"),
    ("Pet Clinics", "Pet Clinics"),
    ("Law Firms", "Law Firms"),
    ("Chartered Accountants", "Chartered Accountants"),
    ("Accounting Firms", "Accounting Firms"),
    ("Real Estate Agents", "Real Estate Agents"),
    ("Interior Designers", "Interior Designers"),
    # Trade
    ("Car Repair Shops", "Car Repair Shops"),
    ("Plumbers", "Plumbers"),
    ("Electricians", "Electricians"),
    # B2B / SaaS targets
    ("Marketing Agencies", "Marketing Agencies"),
    ("Software Companies", "Software Companies"),
    ("Coaching Classes", "Coaching Classes"),
    # Custom
    ("custom", "Custom keyword…"),
]


class LeadSearchForm(forms.Form):
    """Lead search form with Country / State / City / Area cascade dropdowns."""

    keyword = forms.ChoiceField(
        choices=KEYWORD_CHOICES,
        required=False,
        label="Business Type",
        widget=forms.Select(attrs={"class": "form-select", "id": "keyword-select"}),
    )

    custom_keyword = forms.CharField(
        required=False,
        label="Custom keyword",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. Yoga Studios",
            "id": "custom-keyword",
        }),
    )

    # ----------------------------------------------------------------
    # Location cascade — rendered as <select> elements by dashboard.js.
    # Django treats these as plain text values after form submission.
    # ----------------------------------------------------------------
    country = forms.CharField(
        required=True,
        label="Country",
        max_length=100,
        widget=forms.HiddenInput(),   # actual <select> rendered manually in template
    )

    state = forms.CharField(
        required=False,               # optional — not all countries have states
        label="State / Region",
        max_length=100,
        widget=forms.HiddenInput(),
    )

    city = forms.CharField(
        required=True,
        label="City",
        max_length=120,
        widget=forms.HiddenInput(),
    )

    area = forms.CharField(
        required=False,               # optional — search whole city if left blank
        label="Area / Neighborhood",
        max_length=100,
        widget=forms.HiddenInput(),
    )

    max_results = forms.IntegerField(
        required=False,
        label="Max Results",
        initial=50,
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "1",
            "max": "1000",
        }),
    )

    # P1: optional email enrichment toggle
    include_email = forms.BooleanField(
        required=False,
        initial=True,
        label="Include email enrichment (Hunter.io / website scrape)",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean(self):
        cleaned = super().clean()
        keyword = cleaned.get("keyword", "").strip()
        custom_keyword = cleaned.get("custom_keyword", "").strip()

        # Resolve final keyword
        if keyword == "custom":
            if not custom_keyword:
                self.add_error("custom_keyword", "Please enter a custom keyword.")
            else:
                cleaned["resolved_keyword"] = custom_keyword
        elif keyword:
            cleaned["resolved_keyword"] = keyword
        else:
            self.add_error("keyword", "Please select or enter a business type keyword.")

        # Validate required location fields
        country = cleaned.get("country", "").strip()
        city = cleaned.get("city", "").strip()
        area = cleaned.get("area", "").strip()

        if not country:
            self.add_error("country", "Please select a country.")
        if not city:
            self.add_error("city", "Please select a city.")
        # area is optional — empty means search the entire city

        max_results = cleaned.get("max_results")
        if max_results is None:
            cleaned["max_results"] = 50

        return cleaned
