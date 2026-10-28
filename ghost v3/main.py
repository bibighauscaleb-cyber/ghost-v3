from flask import Flask, jsonify, request, send_from_directory
from ddgs import DDGS
from pathlib import Path
import webbrowser
import threading
import time

# ==========================================
# GHOST V3 - WEB SEARCH
# No AI brain or paid AI API required
# ==========================================

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


@app.route("/")
def home():
    """Open Ghost's existing website."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/Ghost_logo.png")
def ghost_logo():
    """Display Ghost's logo if the image exists."""
    return send_from_directory(BASE_DIR, "Ghost_logo.png")


@app.route("/api/search", methods=["POST"])
def web_search():
    """Search the web and return clickable results."""

    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    if not isinstance(query, str):
        return jsonify({"error": "Please enter a search."}), 400

    query = query.strip()

    if not query or len(query) > 300:
        return jsonify({
            "error": "Enter a search between 1 and 300 characters."
        }), 400

    try:
        with DDGS() as search_engine:
            results = search_engine.text(
                query,
                region="us-en",
                safesearch="moderate",
                max_results=8
            )

        clean_results = []

        for result in results:
            url = result.get("href", "")

            if not url.startswith(("https://", "http://")):
                continue

            clean_results.append({
                "title": result.get("title", "Web result"),
                "url": url,
                "description": result.get("body", "")
            })

        return jsonify({"results": clean_results})

    except Exception as error:
        print("Ghost search error:", error)

        return jsonify({
            "error": (
                "Ghost couldn't complete the search. "
                "Check your internet connection and try again."
            )
        }), 502


def open_ghost():
    """Open Ghost automatically in the browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("=" * 40)
    print("          GHOST V3 ONLINE")
    print("=" * 40)
    print("Web searching: ENABLED")
    print("AI brain: NOT REQUIRED")
    print()
    print("Open Ghost at:")
    print("http://127.0.0.1:5000")
    print()
    print("Press CTRL+C to stop Ghost.")
    print("=" * 40)

    threading.Thread(
        target=open_ghost,
        daemon=True
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
