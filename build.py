"""
build.py — Generates a fully static site in docs/ for GitHub Pages.

Usage:
    python build.py

What it does:
  1. Renders the Flask template to plain HTML using Flask's test client.
  2. Rewrites all /static/... paths to relative static/... paths.
  3. Copies the static/ folder into docs/static/.
  4. Writes docs/.nojekyll so GitHub Pages skips Jekyll processing.

After running, commit and push the docs/ folder. In your GitHub repo go to:
  Settings -> Pages -> Source: Deploy from branch -> main -> /docs -> Save
"""

import os
import shutil

from app import app

OUTPUT_DIR = "docs"


def build():
    # ── 1. Clean previous build ──────────────────────────────────────────────
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # ── 2. Render index.html via Flask test client ───────────────────────────
    with app.test_client() as client:
        response = client.get("/")
        if response.status_code != 200:
            raise RuntimeError(f"Flask returned HTTP {response.status_code}")
        html = response.data.decode("utf-8")

    # ── 3. Rewrite absolute /static/ paths -> relative static/ ───────────────
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/',  'src="static/')

    # ── 4. Write docs/index.html ─────────────────────────────────────────────
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Written  {index_path}")

    # ── 5. Copy static assets ────────────────────────────────────────────────
    dest_static = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree("static", dest_static)
    print(f"  Copied   static/ -> {dest_static}/")

    # ── 6. Create .nojekyll (prevents Jekyll from ignoring _files) ───────────
    nojekyll = os.path.join(OUTPUT_DIR, ".nojekyll")
    open(nojekyll, "w").close()
    print(f"  Created  {nojekyll}")

    print(f"\nBuild complete -> '{OUTPUT_DIR}/'")
    print("Next steps:")
    print("  git add docs/")
    print("  git commit -m 'Build static site'")
    print("  git push")


if __name__ == "__main__":
    build()
