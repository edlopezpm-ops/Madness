#!/usr/bin/env python3
"""Build a portable, Spanish job directory from the dated research snapshot.

Run with Python's standard library only. Job summaries are short paraphrases;
the linked employer or job-board page remains the application destination.
"""

from __future__ import annotations

import base64
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parent
PUBLIC_URL = "https://htmlpreview.github.io/?https://github.com/edlopezpm-ops/Madness/blob/add-woodstock-job-directory-2026-11-14/projects/woodstock-jobs/index.html"
REPOSITORY_URL = "https://github.com/edlopezpm-ops/Madness/tree/add-woodstock-job-directory-2026-11-14/projects/woodstock-jobs"
STATUS_LABELS = {
    "published": "Anuncio publicado",
    "continuous": "Contratación continua",
    "unconfirmed": "Por confirmar",
    "general": "Solicitud general",
}
EXTERNAL_ICON = '<svg class="external-icon" viewBox="0 0 16 16" aria-hidden="true" fill="none"><path d="M4 12 12 4M4 4h8v8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def esc(value):
    return html.escape(str(value or ""), quote=True)


def flat(value):
    if isinstance(value, list):
        return " · ".join(str(item) for item in value if item)
    if isinstance(value, dict):
        return " · ".join(str(item) for item in value.values() if item)
    return str(value or "")


def safe_url(value):
    if not isinstance(value, str) or urlparse(value).scheme != "https":
        raise ValueError(f"Expected an HTTPS public source: {value!r}")
    return esc(value)


def link(url, text, class_name="", label=""):
    aria = f' aria-label="{esc(label)}"' if label else ""
    visible_text = esc(text).replace('↗', EXTERNAL_ICON)
    return f'<a class="{esc(class_name)}" href="{safe_url(url)}" target="_blank" rel="noopener noreferrer"{aria}>{visible_text}</a>'


def job_row(job, location):
    status = job["status"]
    details = []
    for label, key in (("Requisitos", "requirements"), ("Sobre el anuncio", "notes")):
        value = flat(job.get(key))
        if value:
            details.append(f'<p><strong>{label}.</strong> {esc(value)}</p>')
    source = job.get("sourceUrl") or job["url"]
    if job.get('futureRoles'):
        future_links = []
        for role in job['futureRoles']:
            role_url = role.get('url') or role.get('applyUrl')
            role_title = role.get('titleEs') or role.get('title') or role.get('name')
            if role_url and role_title:
                future_links.append(link(role_url, role_title, 'text-link'))
        if future_links:
            details.append('<p><strong>Futuras oportunidades; no son vacantes actuales.</strong></p><ul>' + ''.join('<li>' + item + '</li>' for item in future_links) + '</ul>')
    details.append('<p class="source-line">' + link(source, "Consultar fuente", "text-link") +
                   f' <span>· Revisado el {esc(job.get("checked", "2026-11-14"))}</span></p>')
    search = " ".join(flat(job.get(key)) for key in ("title", "titleEs", "category", "schedule", "pay", "requirements", "notes"))
    search += " " + location["company"] + " " + location["address"]
    pay = flat(job.get("pay")) or "Pago no publicado"
    schedule = flat(job.get("schedule")) or "Jornada por confirmar"
    action = job.get('actionLabel') or ("Ver solicitud" if status == "general" else "Ver anuncio")
    travel_note = '<span class="travel-note">Puede requerir desplazamientos</span>' if job.get('travelRequired') else ''
    location_hint = f'<p class="location-hint">{esc(job["locationHint"])}</p>' if job.get('locationHint') else ''
    return f'''
      <article class="job" data-status="{esc(status)}" data-category="{esc(job['category'])}" data-search="{esc(search)}">
        <div class="job-main">
          <span class="status status-{esc(status)}">{STATUS_LABELS[status]}</span>
          <h3>{esc(job.get('titleEs') or job['title'])}</h3>
          <p class="original-title" lang="en">{esc(job['title'])}</p>
          {location_hint}
          <p class="job-meta"><span>{esc(schedule)}</span><span class="category">{esc(job['category'])}</span>{travel_note}</p>
          <details class="job-details"><summary>Requisitos y fuente</summary><div>{''.join(details)}</div></details>
        </div>
        <div class="job-action">
          <p class="pay">{esc(pay)}</p>
          {link(job['url'], action + ' ↗', 'apply-link', action + ': ' + job['title'] + ' en ' + location['company'])}
        </div>
      </article>'''


def build():
    data = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
    jobs = data["jobs"]
    locations = {item["id"]: item for item in data["locations"]}
    assert jobs and len({item["id"] for item in jobs}) == len(jobs), "Job IDs must be unique."
    for job in jobs:
        assert job["locationId"] in locations, job["id"]
        assert job["status"] in STATUS_LABELS, job["id"]
        safe_url(job["url"])
    used_locations = {job["locationId"] for job in jobs}
    for location_id in used_locations:
        location = locations[location_id]
        assert 0 <= location["distanceMiles"] <= 1, (location_id, location["distanceMiles"])
    counts = Counter(job["status"] for job in jobs)
    categories = sorted({job["category"] for job in jobs})
    sections = []
    for location in sorted((locations[key] for key in used_locations), key=lambda item: (item["distanceMiles"], item["company"])):
        local_jobs = [job for job in jobs if job["locationId"] == location["id"]]
        local_jobs.sort(key=lambda item: (list(STATUS_LABELS).index(item["status"]), item.get("titleEs", item["title"])))
        map_url = 'https://www.google.com/maps/search/?api=1&query=' + quote(location["company"] + ", " + location["address"])
        sections.append(f'''
    <section class="employer" aria-labelledby="heading-{esc(location['id'])}">
      <header class="employer-heading">
        <div><p class="employer-distance">≈ {location['distanceMiles']:.2f} mi del cruce</p><h2 id="heading-{esc(location['id'])}">{esc(location['company'])}</h2>
        <p class="address">{esc(location['address'])}</p></div>
        {link(map_url, 'Ver ubicación ↗', 'map-link', 'Ver ubicación de ' + location['company'])}
      </header>
      {''.join(job_row(job, location) for job in local_jobs)}
    </section>''')

    logo_path = ROOT.parent / "weekly-leverage" / "aekr-mark.png"
    logo_data = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    replacements = {
        "@@PUBLIC_URL@@": PUBLIC_URL,
        "@@REPOSITORY_URL@@": REPOSITORY_URL,
        "@@LOGO_DATA@@": logo_data,
        "@@JOB_COUNT@@": str(len(jobs)),
        "@@PUBLISHED_COUNT@@": str(counts["published"]),
        "@@BUSINESS_COUNT@@": str(len(used_locations)),
        "@@CATEGORY_OPTIONS@@": "".join(f'<option value="{esc(category)}">{esc(category)}</option>' for category in categories),
        "@@STATUS_OPTIONS@@": "".join(f'<option value="{status}">{esc(label)} ({counts[status]})</option>' for status, label in STATUS_LABELS.items() if counts[status]),
        "@@EMPLOYERS@@": "".join(sections),
        "@@CENTER_SOURCE@@": safe_url(data["center"]["sourceUrl"]),
    }
    for needle, value in replacements.items():
        template = template.replace(needle, value)
    template = template.replace('↗</', EXTERNAL_ICON + '</')
    assert not re.search(r"@@[A-Z_]+@@", template), "Template contains an unresolved placeholder."
    (ROOT / "index.html").write_text(template, encoding="utf-8")
    print(json.dumps({"file": str(ROOT / "index.html"), "jobs": len(jobs), "businesses": len(used_locations), "statusCounts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    build()
