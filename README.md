# Hyperlocal Business Leads Generator

A Django + Python tool that pulls real local business data from Google Maps and exports clean, sales-ready CSV files — searchable by country, city, neighbourhood, and business type.

Built as a practical portfolio project. No SaaS complexity, no database-heavy architecture, no Docker required. Just a clean dashboard you can run locally and demo instantly.

---

## ✨ Features

- 🌍 **10-country coverage** — India, USA, UK, Germany, France, Australia, Canada, Netherlands, Ireland, UAE
- 🗂️ **Cascading location dropdowns** — Country → State/Region (optional) → City → Area (optional)
- 🔍 **City-wide or neighbourhood-level search** — Area is optional; leave it blank to search the whole city
- 📋 **20+ keyword presets** — Restaurants, Gyms, Dental Clinics, Law Firms, Marketing Agencies, and more; or enter a custom keyword
- 📊 **Lead scoring** — Each result gets a score (0–100) based on rating, review count, website, and email presence
- 📧 **Email enrichment** — Optional Hunter.io + website scrape to find contact emails per business
- 📥 **One-click CSV download** — Phone numbers preserved as text (no Excel scientific-notation mangling)
- 🟡 **Demo mode** — Auto-activates when Apify credits run out or no token is set; generates realistic sample data so you can always present the tool
- 🎨 **Navy + Teal dashboard** — Clean, contrast-accessible UI (AAA text contrast throughout)

---

## 🖥️ Dashboard Preview

Select your parameters and click **Generate Leads**:

```
Country      → India
State        → Karnataka  (optional)
City         → Bengaluru
Area         → Koramangala  (optional — leave blank for full city)
Business Type → Marketing Agencies
Max Results  → 50
```

The backend builds:

```
Marketing Agencies in Koramangala, Bengaluru
```

Then it fetches, filters, scores, and exports — results appear in the dashboard table instantly.

---

## 📋 Output Columns

| Column | Description |
|--------|-------------|
| Business Name | Trading name from Google Maps |
| Category | Business type / category |
| Area | Neighbourhood — from user selection or extracted from record address |
| Address | Full street address |
| Phone Number | Cleaned, `+` prefix preserved (text-safe in Excel) |
| Website | Business website URL |
| Google Rating | Star rating (0–5) |
| Review Count | Total Google reviews |
| Google Maps URL | Direct link to the listing |
| Email | Found via Hunter.io or website scrape (if enrichment enabled) |
| Email Source | How the email was found (verified / confidence % / not found) |
| Lead Score | 0–100 quality score |

---

## 🌐 Country & Location Coverage

| Country | States/Regions | Cities | Areas |
|---------|---------------|--------|-------|
| 🇮🇳 India | 24 | 124 | 741 |
| 🇺🇸 USA | 47 | 169 | 848 |
| 🇬🇧 UK | 4 | 37 | 221 |
| 🇩🇪 Germany | 16 | 62 | 309 |
| 🇫🇷 France | 12 | 47 | 198 |
| 🇦🇺 Australia | 8 | 33 | 170 |
| 🇨🇦 Canada | 13 | 54 | 246 |
| 🇳🇱 Netherlands | — | 20 | 112 |
| 🇮🇪 Ireland | — | 15 | 82 |
| 🇦🇪 UAE | 7 | 8 | 71 |

---

## ⚙️ Tech Stack

- **Python 3.11+**
- **Django 4.2** — dashboard, form handling, file download
- **Pandas** — data cleaning, deduplication, scoring, CSV export
- **Requests** — Apify and Hunter.io API calls
- **Apify** — Google Maps Scraper actor (`compass/crawler-google-places`)
- **Hunter.io** *(optional)* — email enrichment

---

## 📁 Folder Structure

```text
Hyperlocal-Business-Leads-Generator/
│
├── leadgen_site/          # Django project settings & URLs
├── leads/
│   ├── static/leads/
│   │   └── dashboard.js   # Cascading dropdown logic (JS)
│   ├── templates/leads/
│   │   └── dashboard.html # Main UI template
│   ├── forms.py           # Search form & validation
│   ├── geo_data.py        # Geography data (10 countries, all states/cities/areas)
│   ├── urls.py
│   └── views.py           # Dashboard & CSV download views
├── raw_data/              # Raw Apify JSON responses
├── cleaned_data/          # Intermediate cleaned CSV
├── output/                # Final CSV exports (downloaded from UI)
├── screenshots/
├── main.py                # Core orchestration — fetch, filter, score, export
├── manage.py
├── requirements.txt
└── .env                   # API keys (not committed)
```

---

## 🚀 Setup

**1. Clone and create a virtual environment:**

```bash
python -m venv venv
```

**2. Activate it:**

```powershell
# Windows
venv\Scripts\activate
```

```bash
# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root:**

```env
APIFY_API_TOKEN=your_apify_api_token_here

# Optional — only needed if using a non-default actor
APIFY_ACTOR_ID=compass/crawler-google-places

# Optional — for email enrichment
HUNTER_API_KEY=your_hunter_api_key_here

# Optional — raise the results cap (default 1000)
MAX_RESULTS_LIMIT=1500
```

**5. Run the server:**

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## 🆓 Getting a Free Apify Token

Apify gives **$5 free credits per month** (≈ 1,000 leads) with no credit card required on signup:

1. Sign up at [apify.com](https://apify.com)
2. Go to **Settings → Integrations → API tokens**
3. Copy your token into `.env`

> **Note:** If your Apify credits run out, the tool automatically falls back to **Demo Mode** — no crash, no red error — so you can keep testing the UI.

---

## 🟡 Demo Mode

Demo mode activates automatically when:
- No `APIFY_API_TOKEN` is set in `.env`
- Your Apify account has hit its billing/usage limit (HTTP 402)
- Your account is rate-limited (HTTP 429)

In demo mode, realistic sample leads are generated for whatever keyword + location you enter. The `[DEMO]` tag appears on each business name so the data is clearly distinguishable from live results.

---

## 📥 CSV Export Notes

- Phone numbers are **tab-prefixed** in the CSV and exported with `QUOTE_ALL` so Excel and Google Sheets always treat them as text — no `+491234567890` → `4.91E+11` conversion
- Files are saved with a dynamic name: `leads_marketing-agencies_bengaluru_20260625.csv`
- The **Download CSV** button on the dashboard streams the latest output file directly to your browser

---

## 🖥️ CLI Mode

Run without Django for quick terminal use:

```bash
python main.py
```

Edit the defaults at the top of `main.py`:

```python
KEYWORD     = "Marketing Agencies"
AREA        = "Koramangala"
CITY        = "Bengaluru"
MAX_RESULTS = 50
```

---

## 💼 Use Cases

- Local SEO agency prospecting
- Google Business Profile audit outreach
- Website redesign lead generation
- Niche market research (gyms, clinics, law firms, etc.)
- Cold email list building for local B2B services
- Portfolio demonstration of Python + data automation skills
