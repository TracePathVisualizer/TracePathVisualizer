// ==================================================
// TracePathVisualizer (TPV)
// Copyright (c) 2026 NoF8
// Licensed under the MIT License
// ==================================================


// ==================================================
// Map State
// ==================================================

let tpvMap;


// ==================================================
// Initialise Map
// ==================================================

function initialiseMap() {

    tpvMap = L.map("map", {
        zoomControl: true,
        attributionControl: true,
    }).setView([-25.2744, 133.7751], 4);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(tpvMap);

    addTestMarkers();

}


// ==================================================
// Test Markers
// ==================================================

function addTestMarkers() {

    L.marker([-27.4698, 153.0251])
        .addTo(tpvMap)
        .bindPopup("Brisbane test hop");

}