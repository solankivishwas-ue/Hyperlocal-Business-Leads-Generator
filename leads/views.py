from __future__ import annotations

from django.http import FileResponse, Http404
from django.shortcuts import render

from main import FINAL_COLUMNS, OUTPUT_DIR, run_lead_generation

from .forms import CITY_AREA_MAP, LeadSearchForm


def dashboard(request):
    form = LeadSearchForm(request.POST or None)
    context = {
        "form": form,
        "columns": FINAL_COLUMNS,
        "leads": [],
        "table_rows": [],
        "result": None,
        "error": "",
        "city_area_map": CITY_AREA_MAP,
    }

    if request.method == "POST" and form.is_valid():
        try:
            result = run_lead_generation(
                keyword=form.cleaned_data["keyword"],
                area=form.cleaned_data["area"],
                city=form.cleaned_data["city"],
                max_results=form.cleaned_data["max_results"],
            )
            context["result"] = result
            context["leads"] = result["leads"]
            context["table_rows"] = [
                [lead.get(column, "") for column in FINAL_COLUMNS]
                for lead in result["leads"]
            ]
        except Exception as exc:
            context["error"] = str(exc)

    return render(request, "leads/dashboard.html", context)


def download_csv(request):
    output_file = OUTPUT_DIR / "business_leads.csv"
    if not output_file.exists():
        raise Http404("CSV file has not been generated yet.")

    return FileResponse(
        output_file.open("rb"),
        as_attachment=True,
        filename="business_leads.csv",
    )
