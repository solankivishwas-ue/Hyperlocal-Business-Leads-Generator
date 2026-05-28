(function () {
    const cityAreaScript = document.getElementById("city-area-data");
    const citySelect = document.getElementById("id_city");
    const areaSelect = document.getElementById("id_area");
    const keywordSelect = document.getElementById("id_keyword_choice");
    const customKeywordField = document.querySelector("[data-custom-keyword-field]");
    const customKeywordInput = document.getElementById("id_custom_keyword");
    const customCityField = document.querySelector("[data-custom-city-field]");
    const customCityInput = document.getElementById("id_custom_city");
    const customAreaField = document.querySelector("[data-custom-area-field]");
    const customAreaInput = document.getElementById("id_custom_area");

    if (!cityAreaScript || !citySelect || !areaSelect || !keywordSelect) {
        return;
    }

    const cityAreaMap = JSON.parse(cityAreaScript.textContent);
    const customKeywordValue = "__custom__";
    const customCityValue = "__custom_city__";
    const customAreaValue = "__custom_area__";

    function updateAreaOptions(preferredArea) {
        const isCustomCity = citySelect.value === customCityValue;
        const areas = isCustomCity ? [] : cityAreaMap[citySelect.value] || [];
        const wantsCustomArea = preferredArea === customAreaValue;
        const nextArea = wantsCustomArea
            ? customAreaValue
            : areas.includes(preferredArea)
                ? preferredArea
                : areas[0];

        areaSelect.innerHTML = "";
        areas.forEach((area) => {
            const option = document.createElement("option");
            option.value = area;
            option.textContent = area;
            areaSelect.appendChild(option);
        });

        const customOption = document.createElement("option");
        customOption.value = customAreaValue;
        customOption.textContent = "Custom area";
        areaSelect.appendChild(customOption);

        if (isCustomCity || wantsCustomArea) {
            areaSelect.value = customAreaValue;
        } else if (nextArea) {
            areaSelect.value = nextArea;
        } else {
            areaSelect.value = customAreaValue;
        }

        updateCustomCity();
        updateCustomArea();
    }

    function updateCustomKeyword() {
        const isCustom = keywordSelect.value === customKeywordValue;

        if (customKeywordField) {
            customKeywordField.classList.toggle("is-hidden", !isCustom);
        }

        if (customKeywordInput) {
            customKeywordInput.required = isCustom;
            if (!isCustom) {
                customKeywordInput.value = "";
            }
        }
    }

    function updateCustomCity() {
        const isCustom = citySelect.value === customCityValue;

        if (customCityField) {
            customCityField.classList.toggle("is-hidden", !isCustom);
        }

        if (customCityInput) {
            customCityInput.required = isCustom;
            if (!isCustom) {
                customCityInput.value = "";
            }
        }
    }

    function updateCustomArea() {
        const isCustom = citySelect.value === customCityValue || areaSelect.value === customAreaValue;

        if (customAreaField) {
            customAreaField.classList.toggle("is-hidden", !isCustom);
        }

        if (customAreaInput) {
            customAreaInput.required = isCustom;
            if (!isCustom) {
                customAreaInput.value = "";
            }
        }
    }

    const startingArea = areaSelect.value;
    updateAreaOptions(startingArea);
    updateCustomKeyword();

    citySelect.addEventListener("change", () => updateAreaOptions(areaSelect.value));
    areaSelect.addEventListener("change", updateCustomArea);
    keywordSelect.addEventListener("change", updateCustomKeyword);
})();
