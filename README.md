# TracePathVisualizer (TPV)

**Project Status:** Active Development – CLI V1.0.0

TracePathVisualizer (TPV) is an open-source network path analysis and visualisation utility for Windows.

TPV combines DNS resolution, connectivity testing, traceroute analysis, and network enrichment into a single tool designed to make network troubleshooting easier to understand.

The long-term goal is to provide a graphical network analysis platform that presents routing, latency, ownership, and location information in a clear and human-readable format.

---

## Current Features

### DNS Resolution

* Resolve hostnames to IP addresses
* Display all returned addresses
* Report DNS lookup failures

### Ping Diagnostics

* Verify destination reachability
* Packet loss reporting
* Average latency measurement

### Traceroute Analysis

* Discover intermediate network hops
* Display per-hop latency measurements
* Detect silent routers and route failures
* Real-time hop reporting

### Network Path Enrichment

* ASN identification
* ISP ownership lookup
* Geographic enrichment where available
* Local endpoint identification

### Network Path Summary

* Human-readable network ownership view
* Geographic route overview
* Structured hop data model

---

## Building From Source

### Requirements

* Python 3.13+
* Windows 10 or Windows 11

### Create Virtual Environment

```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

### Install Build Tools

```powershell
py -m pip install --upgrade pip
py -m pip install pyinstaller
```

### Build Executable

TPV includes a PyInstaller specification file.

```powershell
py -m PyInstaller TPV.spec
```

### Run Executable

```powershell
.\dist\TPV.exe
```

---

## Project Structure

```text
TracePathVisualizer
│
├── app
│   ├── cli.py
│   └── gui.py
│
├── core
│   ├── diagnostic.py
│   ├── dns.py
│   ├── enrichment.py
│   ├── models.py
│   ├── ping.py
│   └── traceroute.py
│
├── main.py
├── TPV.spec
├── README.md
├── DESIGN.md
└── LICENSE
```

---

## Roadmap

### V1.0.0

* DNS resolution
* Ping diagnostics
* Traceroute analysis
* IP enrichment
* Network path reporting
* Event engine
* Health assessment engine
* Enhanced route analysis
* Windows executable packaging

### V2.0.0

* Graphical user interface
* Interactive hop inspection
* Route visualisation

### Future Enhancements

* Historical route comparison
* Route change detection
* Continuous monitoring
* Exportable reports
* Geographic route mapping
* Advanced diagnostics

---

## Design Philosophy

* Open Source
* No telemetry
* No advertising
* Local-first operation
* Human-readable diagnostics
* Clear distinction between observed facts and inferred conclusions

---

## License

Released under the MIT License.

Copyright (c) 2026 NoF8
