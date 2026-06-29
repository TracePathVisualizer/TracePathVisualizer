// ==================================================
// TracePathVisualizer (TPV)
// Copyright (c) 2026 NoF8
// Licensed under the MIT License
// ==================================================


// ==================================================
// Map State
// ==================================================

let tpvMap;
let activeTileLayer;


// ==================================================
// Map Themes
// ==================================================

const MAP_THEMES = {

    esriDarkGray: {
        name: "Esri Dark Gray Canvas",
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        options: {
            maxZoom: 16,
            attribution: "&copy; Esri"
        },
        sidebarClass: "theme-esri-dark"
    },

    esriLightGray: {
        name: "Esri Light Gray Canvas",
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        options: {
            maxZoom: 16,
            attribution: "&copy; Esri"
        },
        sidebarClass: "theme-esri-light"
    },

    esriOcean: {
        name: "Esri Ocean",
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
        options: {
            maxZoom: 10,
            attribution: "&copy; Esri"
        },
        sidebarClass: "theme-esri-ocean"
    }

};


// ==================================================
// Initialise Map
// ==================================================

function initialiseMap() {

    tpvMap = L.map("map", {
        zoomControl: true,
        attributionControl: true,
    }).setView([-25.2744, 133.7751], 4);

    setMapTheme("esriDarkGray");

    addTestMarkers();

    setTimeout(() => {
        tpvMap.invalidateSize();
    }, 100);

}


// ==================================================
// Set Map Theme
// ==================================================

function setMapTheme(themeKey) {

    const theme = MAP_THEMES[themeKey];

    if (!theme) {
        console.error(`Unknown map theme: ${themeKey}`);
        return;
    }

    if (activeTileLayer) {
        tpvMap.removeLayer(activeTileLayer);
    }

    activeTileLayer = L.tileLayer(theme.url, theme.options);
    activeTileLayer.addTo(tpvMap);

}


// ==================================================
// Test Markers
// ==================================================

function addTestMarkers() {

    L.marker([-27.4698, 153.0251])
        .addTo(tpvMap)
        .bindPopup("Brisbane Test Hop");

}