# Local Business Leads Generator

A simple Django + Python automation project for generating local business leads from Google Maps and exporting clean CSV datasets.

This is an MVP for portfolio and demo use. It is designed to feel like a practical local lead generation service without adding SaaS complexity, authentication, Docker, cloud deployment, or a database-heavy architecture.

## What It Does

Enter:

```text
keyword dropdown = Dental Clinics
area = Ranip
city dropdown = Ahmedabad
```

The backend builds:

```text
Dental Clinics in Ranip, Ahmedabad, Gujarat
```

Then it:

- Fetches Google Maps lead data through the Apify Google Maps Scraper API
- Saves the raw response as JSON
- Cleans and structures the data with Pandas
- Removes duplicate businesses
- Filters out broad Google Maps results from other areas, cities, or unrelated business types
- Normalizes phone numbers
- Exports a professional CSV file
- Shows results in a simple Django dashboard
- Provides city and area dropdowns
- Updates areas based on the selected city
- Includes a broader preset catalog of common Indian cities and local areas
- Provides keyword presets plus a custom keyword option
- Supports custom city and custom area entries
- Supports larger lead runs up to 1000 results by default

## Output Columns

- Business Name
- Category
- Area
- Address
- Phone Number
- Website
- Google Rating
- Review Count
- Google Maps URL

## Tech Stack

- Python 3.11+
- Django
- Pandas
- Requests
- Apify Google Maps Scraper API
- CSV export

## Folder Structure

```text
local-business-leads-generator/
│
├── leadgen_site/
├── leads/
│   ├── static/leads/styles.css
│   ├── templates/leads/dashboard.html
│   ├── forms.py
│   ├── urls.py
│   └── views.py
├── raw_data/
├── cleaned_data/
├── output/
├── screenshots/
├── scripts/
├── manage.py
├── main.py
├── README.md
└── requirements.txt
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your Apify token in a `.env` file:

```text
APIFY_API_TOKEN=your_apify_api_token_here
```

If your Apify account uses a different Google Maps actor, also add:

```text
APIFY_ACTOR_ID=your_actor_id_here
```

## Run The Django App

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Use the form to search examples like:

- Dental Clinics in Ranip Ahmedabad
- Gyms in Satellite Ahmedabad
- Restaurants in Navrangpura Ahmedabad
- Salons in Bodakdev Ahmedabad
- Custom keyword in a selected city and area

The city dropdown includes a broader preset catalog of common Indian cities. The area dropdown changes automatically based on the selected city. If a city or area is not listed, choose `Custom city` or `Custom area` and type it manually.

`Max Results` supports up to 1000 rows by default. You can change the backend limit with:

```text
MAX_RESULTS_LIMIT=1500
```

in your `.env` file.

## CSV Output

After a search, the app writes:

```text
raw_data/google_maps_raw_YYYYMMDD_HHMMSS.json
cleaned_data/cleaned_business_leads.csv
output/business_leads.csv
```

The app sends a more specific city/state search query when the city is known, saves the full raw Apify response, then exports only records that pass the strict area, city, and keyword/category filter. This helps prevent large searches from leaking in nearby areas, other cities, or unrelated clinic/business types when Google Maps broadens the result set.

The dashboard includes a download button for:

```text
output/business_leads.csv
```

## CLI Option

You can also run the backend without Django:

```bash
python main.py
```

Edit these defaults in `main.py`:

```python
KEYWORD = "Dental Clinics"
AREA = "Ranip"
CITY = "Ahmedabad"
MAX_RESULTS = 250
```

## Demo Mode

If no `APIFY_API_TOKEN` is found, the project runs in demo mode and generates sample leads that still match your keyword, area, and city. This makes the project easy to present even before connecting a paid API account.

For live Apify runs, the backend requests only the fields needed for the final CSV. Reviews, images, and opening hours are disabled to keep larger searches faster and lighter.

## Business Use

This project can support:

- Local SEO outreach
- Website redesign prospecting
- Google Business Profile service leads
- Niche local market research
- Small agency lead list generation
