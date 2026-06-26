# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

from pathlib import Path

import webview


class TPVApi:
    def ping_backend(self) -> dict:
        return {
            "status": "ok",
            "message": "Python backend is connected.",
        }


def run_gui() -> None:
    root_dir = Path(__file__).resolve().parent.parent
    html_path = root_dir / "ui" / "index.html"

    api = TPVApi()

    webview.create_window(
        title="TracePathVisualizer",
        url=html_path.as_uri(),
        js_api=api,
        width=1200,
        height=800,
    )

    webview.start(debug=True)