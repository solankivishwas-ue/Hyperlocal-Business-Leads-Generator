"""Django views for the lead generation dashboard.

Upgrades:
  P1 — passes include_email flag to run_lead_generation
  P2 — city/area received from cascade dropdowns, geo_data_json passed to template
  P4 — passes summary stats to template; handles dynamic filename for download
"""

import json
import os
from pathlib import Path

from django.http import FileResponse, Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import LeadSearchForm
from .geo_data import GEO_DATA

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

# Pre-serialise once at import time (avoids repeated json.dumps on every request)
_GEO_DATA_JSON: str = json.dumps(GEO_DATA)


def dashboard(request: HttpRequest) -> HttpResponse:
    """Main lead generation dashboard view."""
    form = LeadSearchForm()
    leads = []
    error_message = None
    result_meta = None
    stats = None
    output_filename = None

    if request.method == "POST":
        form = LeadSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            keyword = data.get("resolved_keyword", "")
            city = data.get("city", "").strip()
            area = data.get("area", "").strip()
            max_results = data.get("max_results") or 50
            include_email = data.get("include_email", True)

            try:
                # Import here so Django startup doesn't require Apify deps
                from main import run_lead_generation

                result = run_lead_generation(
                    keyword=keyword,
                    area=area,
                    city=city,
                    max_results=max_results,
                    include_email=include_email,
                )
                # Normalise keys: "Business Name" → "Business_Name" for template dot-notation
                raw_leads = result.get("leads", [])
                leads = [
                    {k.replace(" ", "_"): v for k, v in row.items()}
                    for row in raw_leads
                ]
                stats = result.get("stats", {})
                output_filename = result.get("output_filename", "business_leads.csv")

                result_meta = {
                    "search_query": result["search_query"],
                    "mode": result["mode"],
                    "raw_record_count": result["raw_record_count"],
                    "filtered_out_count": result["filtered_out_count"],
                    "record_count": result["record_count"],
                    "output_filename": output_filename,
                }

            except ValueError as exc:
                # P4 — clear validation error
                error_message = str(exc)
            except Exception as exc:
                error_message = f"Lead generation failed: {exc}"

    return render(
        request,
        "leads/dashboard.html",
        {
            "form": form,
            "leads": leads,
            "error_message": error_message,
            "result_meta": result_meta,
            "stats": stats,
            "output_filename": output_filename,
            # Geography cascade data for JS dropdowns
            "geo_data_json": _GEO_DATA_JSON,
        },
    )


def download_leads(request: HttpRequest) -> FileResponse:
    """Stream the most recent output CSV to the browser."""
    filename = request.GET.get("filename", "business_leads.csv")

    # Security: only allow simple filenames (no path traversal)
    safe_name = Path(filename).name
    if not safe_name.endswith(".csv"):
        raise Http404("Only CSV files can be downloaded.")

    file_path = OUTPUT_DIR / safe_name
    if not file_path.exists():
        # Fallback to the static-name file for backward compat
        file_path = OUTPUT_DIR / "business_leads.csv"

    if not file_path.exists():
        raise Http404("No leads file found. Run a search first.")

    response = FileResponse(
        open(file_path, "rb"),
        content_type="text/csv",
        as_attachment=True,
        filename=safe_name,
    )
    return response


def areas_for_city(request: HttpRequest) -> JsonResponse:
    """Legacy AJAX endpoint — kept so existing bookmarks don't 404."""
    return JsonResponse({"areas": [], "message": "Areas are now driven by geo_data.py cascade dropdowns."})
