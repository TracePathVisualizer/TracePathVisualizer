// ==================================================
// TracePathVisualizer (TPV)
// Copyright (c) 2026 NoF8
// Licensed under the MIT License
// ==================================================


// ==================================================
// Application Initialisation
// ==================================================

document.addEventListener("DOMContentLoaded", initialiseApplication);


// ==================================================
// Initialise Application
// ==================================================

function initialiseApplication() {

    console.log("TracePathVisualizer GUI initialised.");

    initialiseMap();
    registerThemeSelector();

}


// ==================================================
// Register Theme Selector
// ==================================================

function registerThemeSelector() {

    const themeSelector = document.getElementById("map-theme-select");

    if (!themeSelector) {
        console.warn("Map theme selector not found.");
        return;
    }

    themeSelector.addEventListener("change", () => {
        setMapTheme(themeSelector.value);
    });

}