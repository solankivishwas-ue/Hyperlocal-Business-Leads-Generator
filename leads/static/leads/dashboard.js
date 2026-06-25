/**
 * dashboard.js — Cascade dropdown logic for
 * Country → State (optional) → City → Area
 *
 * Also handles:
 * - Custom keyword row toggle
 * - Restoring dropdown state after a POST (form re-render with errors or results)
 * - Auto-scroll to results section when leads are present
 */
(function () {
    "use strict";

    // ------------------------------------------------------------------
    // Parse geography data embedded in the page
    // ------------------------------------------------------------------
    const geoEl = document.getElementById("geo-data");
    if (!geoEl) return;
    const GEO = JSON.parse(geoEl.textContent || "{}");

    // ------------------------------------------------------------------
    // Element refs
    // ------------------------------------------------------------------
    const form            = document.getElementById("lead-search-form");
    const countrySelect   = document.getElementById("country-select");
    const stateWrapper    = document.getElementById("state-field-wrapper");
    const stateSelect     = document.getElementById("state-select");
    const citySelect      = document.getElementById("city-select");
    const areaSelect      = document.getElementById("area-select");
    const keywordSelect   = document.getElementById("keyword-select");
    const customKwRow     = document.getElementById("custom-keyword-row");

    // Hidden inputs that carry the selected values to Django on submit
    const hiddenCountry   = document.getElementById("hidden-country");
    const hiddenState     = document.getElementById("hidden-state");
    const hiddenCity      = document.getElementById("hidden-city");
    const hiddenArea      = document.getElementById("hidden-area");

    if (!countrySelect || !citySelect || !areaSelect) return;

    // ------------------------------------------------------------------
    // Restore values that were submitted (available on form re-render)
    // ------------------------------------------------------------------
    const saved = {
        country : (form && form.dataset.country) || "",
        state   : (form && form.dataset.state)   || "",
        city    : (form && form.dataset.city)    || "",
        area    : (form && form.dataset.area)    || "",
    };

    // ------------------------------------------------------------------
    // Helper: populate a <select> element
    // ------------------------------------------------------------------
    function populateSelect(selectEl, options, placeholder, selectedValue) {
        selectEl.innerHTML = "";

        if (placeholder) {
            const ph = document.createElement("option");
            ph.value = "";
            ph.textContent = placeholder;
            selectEl.appendChild(ph);
        }

        options.forEach(function (val) {
            const opt = document.createElement("option");
            opt.value = val;
            opt.textContent = val;
            if (val === selectedValue) {
                opt.selected = true;
            }
            selectEl.appendChild(opt);
        });
    }

    // ------------------------------------------------------------------
    // Data helpers
    // ------------------------------------------------------------------
    function getStates(country) {
        const c = GEO[country];
        if (!c || !c.has_states) return [];
        return Object.keys(c.states || {});
    }

    function getCities(country, state) {
        const c = GEO[country];
        if (!c) return [];

        if (c.has_states) {
            const statesObj = c.states || {};
            if (state && statesObj[state]) {
                return Object.keys(statesObj[state]);
            }
            // No state selected — aggregate all cities across all states
            const all = [];
            Object.values(statesObj).forEach(function (stateCities) {
                Object.keys(stateCities).forEach(function (city) {
                    if (!all.includes(city)) all.push(city);
                });
            });
            return all.sort();
        }

        // Country with no state level
        return Object.keys(c.cities || {});
    }

    function getAreas(country, state, city) {
        const c = GEO[country];
        if (!c) return [];

        if (c.has_states) {
            const statesObj = c.states || {};
            if (state && statesObj[state] && statesObj[state][city]) {
                return statesObj[state][city];
            }
            // State not selected — search all states for this city
            for (const s of Object.keys(statesObj)) {
                if (statesObj[s][city]) return statesObj[s][city];
            }
            return [];
        }

        const citiesObj = c.cities || {};
        return citiesObj[city] || [];
    }

    // ------------------------------------------------------------------
    // Sync hidden inputs (values sent to Django)
    // ------------------------------------------------------------------
    function syncHidden() {
        if (hiddenCountry) hiddenCountry.value = countrySelect.value;
        if (hiddenState)   hiddenState.value   = stateSelect   ? stateSelect.value : "";
        if (hiddenCity)    hiddenCity.value     = citySelect.value;
        if (hiddenArea)    hiddenArea.value     = areaSelect.value;
    }

    // ------------------------------------------------------------------
    // Cascade update functions
    // ------------------------------------------------------------------
    function updateStates(preferState) {
        const country  = countrySelect.value;
        const c        = GEO[country];
        const hasStates = c && c.has_states;

        // Show/hide the state column
        if (stateWrapper) {
            stateWrapper.style.display = hasStates ? "" : "none";
        }

        if (stateSelect) {
            if (hasStates) {
                const states = getStates(country);
                populateSelect(stateSelect, states, "— All States (optional) —", preferState || "");
            } else {
                stateSelect.innerHTML = "";
                const opt = document.createElement("option");
                opt.value = "";
                opt.textContent = "— N/A —";
                stateSelect.appendChild(opt);
            }
        }
    }

    function updateCities(preferCity) {
        const country = countrySelect.value;
        const state   = stateSelect ? stateSelect.value : "";
        const cities  = getCities(country, state);
        populateSelect(citySelect, cities, "— Select City —", preferCity || "");
    }

    function updateAreas(preferArea) {
        const country = countrySelect.value;
        const state   = stateSelect ? stateSelect.value : "";
        const city    = citySelect.value;
        const areas   = getAreas(country, state, city);
        populateSelect(areaSelect, areas, "— Entire City (optional) —", preferArea || "");
    }

    // ------------------------------------------------------------------
    // Initialise dropdowns
    // ------------------------------------------------------------------
    function init() {
        // Populate country list
        const countries = Object.keys(GEO).sort();
        populateSelect(countrySelect, countries, "— Select Country —", saved.country);

        // Cascade from saved (post-submit restore)
        updateStates(saved.state);
        updateCities(saved.city);
        updateAreas(saved.area);

        syncHidden();
    }

    // ------------------------------------------------------------------
    // Event listeners
    // ------------------------------------------------------------------
    countrySelect.addEventListener("change", function () {
        updateStates("");
        updateCities("");
        updateAreas("");
        syncHidden();
    });

    if (stateSelect) {
        stateSelect.addEventListener("change", function () {
            updateCities("");
            updateAreas("");
            syncHidden();
        });
    }

    citySelect.addEventListener("change", function () {
        updateAreas("");
        syncHidden();
    });

    areaSelect.addEventListener("change", syncHidden);

    // Sync hidden inputs right before the form submits (safety net)
    if (form) {
        form.addEventListener("submit", syncHidden);
    }

    // ------------------------------------------------------------------
    // Custom keyword row toggle
    // ------------------------------------------------------------------
    if (keywordSelect && customKwRow) {
        function toggleCustomKw() {
            customKwRow.style.display = keywordSelect.value === "custom" ? "block" : "none";
        }
        keywordSelect.addEventListener("change", toggleCustomKw);
        toggleCustomKw(); // init
    }

    // ------------------------------------------------------------------
    // Auto-scroll to results if they were just loaded
    // ------------------------------------------------------------------
    const resultsSection = document.getElementById("results-section");
    if (resultsSection) {
        setTimeout(function () {
            resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 200);
    }

    // ------------------------------------------------------------------
    // Kick everything off
    // ------------------------------------------------------------------
    init();
})();
