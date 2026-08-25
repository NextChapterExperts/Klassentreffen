import zipfile, xml.etree.ElementTree as ET
import urllib.parse
import json, os, re

file_path = '/home/peter/Projekte/active/Klassentreffen/Klassenliste 10b_1976.xlsx'

with zipfile.ZipFile(file_path) as z:
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in tree.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
            text = ''.join(t.text for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t') if t.text)
            shared_strings.append(text)
            
    tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    rows = []
    for row in tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
        row_data = {}
        for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
            r_col = c.attrib.get('r', '')
            col_letter = ''.join(filter(str.isalpha, r_col))
            t = c.attrib.get('t')
            v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            val = v.text if v is not None else ''
            if t == 's' and val.isdigit():
                val = shared_strings[int(val)]
            row_data[col_letter] = val.strip()
        if any(row_data.values()):
            rows.append(row_data)

data_rows = rows[2:]

known_insights = {
    'Fellhauer': 'Heiße Spur: Ehemaliger Inhaber von Omnibusverkehr & Krankentransporte Klaus Fellhauer (Malsch / Rhein-Neckar-Kreis) bzw. ehem. Heidelberg/Nußloch.',
    'Stegmaier': 'Bestätigt: Bezirksbeirat SPD Mannheim-Gartenstadt (Am Föhrenhof 12a). Wohnort und Person verifiziert.',
    'Meffert': 'Bestätigt: Wohnhaft in Rösrath (Köln), Senior Marketing Manager bei Gen Re (Köln), Vater von Profifußballer Jonas Meffert (TV Hoffnungsthal).',
    'Leutz (Erben)': 'Adresse bestätigt: Beethovenstr. 38, St. Ilgen im Telefonbuch unter Siegfried Leutz registriert. Festnetz 06224/53217.',
    'Fuentecilla-Perez': 'Spur: Enriqueta Fuentecilla aktiv in Darmstadt (u.a. Oxfam Buchladen Darmstadt).',
    'Prieto-Durán': 'Bestätigt: Dr. med. Salvador Prieto-Durán, Facharzt für Kinder- und Jugendpsychiatrie/-psychotherapie, Quirinsstraße 8, 60599 Frankfurt, Tel: 069/56993537 (Alte E-Mail @aol.com ersetzen).',
    'Bubenitschek': 'Bestätigt: Erster Kriminalhauptkommissar a.D., Träger des Bundesverdienstkreuzes am Bande, Landespräventionsbeauftragter WEISSER RING BaWü, Sandhausen.',
    'Schilling': 'Bestätigt: Leitender Wassermeister / technischer Betriebsleiter ZWH (Leimen/Sandhausen/Walldorf), im Nov 2024 nach 37 Jahren in den Ruhestand verabschiedet. Leimen.',
    'Schneid': 'Bestätigt: Vorstandsvorsitzender Weltladen Kraichtal e.V., ehem. Vorstand Jugendchor MeOLa & Posaunenchor Kraichtal-Menzingen (Siecherstr. 3).',
    'Burger (Sickmüller)': 'Bestätigt: Anschrift Zwischen den Wegen 45 in Wiesloch verbunden mit Fliesenleger-Fachbetrieb Burger GmbH / Familie Burger.',
    'Eustachi (Steinmann)': 'Bestätigt: Familie Karlheinz & Susanne Eustachi (Eustachi Rollladen- & Fensterbau, Nußloch).',
    'Lysowec': 'Bestätigt: Uwe Lysowec, Musiker / Bassist (SOULMATES Kurpfalz & Vintage Vibes), wohnhaft in Gaiberg.',
    'Stumpf-Schuhmacher': 'Wichtig: Langjährige Mitarbeiterin bei Familienheim Heidelberg eG, seit 10/2022 im Ruhestand (daher Firmen-Mail stillgelegt!). Privatanschrift in Eppelheim & Telefon 06221/767460 nutzen.',
    'Bögner': 'Bestätigt: Dr. med. dent. Holger Bögner, Zahnarztpraxis Darmstädter Landstraße 7-9, 60594 Frankfurt, Tel. 069/66129960. (PLZ Frankfurt ist 60594, nicht 69594).',
    'Weichert': 'Spur: Praxis für Krankengymnastik & Physiotherapie (Seegasse 15, Sandhausen) bzw. kommunalpolitisch aktiv (GAL Sandhausen).',
    'Danner': 'Akademische Spur: Medizinisches Umfeld / Immunologie-Forschung am Universitätsklinikum Heidelberg.',
    'Sauter': 'Spur: Rainer Sauter in Sandhausen (Sportverein SV Sandhausen / Busunternehmen).',
    'Stumpf': 'Spur: Silvia Stumpf (Promotion/Forschung Universität Heidelberg / KIT). Anschrift Kurpfalz-Centrum Leimen prüfen.',
    'Thomschy': 'Bereits als verstorben vermerkt († 19.10.2020).',
    'Wilhelm (Stuber)': 'Bereits als verstorben vermerkt († 23.11.2024).'
}

people = []
for r in data_rows:
    name_raw = r.get('A', '')
    vorname = r.get('B', '')
    strasse = r.get('C', '')
    plz_ort = r.get('D', '')
    telefon = r.get('E', '')
    email = r.get('F', '')
    notizen = r.get('G', '')
    
    if not name_raw or 'ohne Gewähr' in name_raw:
        continue

    maiden_name = ''
    main_name = name_raw
    m = re.search(r'([^(]+)\s*\(([^)]+)\)', name_raw)
    if m:
        main_name = m.group(1).strip()
        maiden_name = m.group(2).strip()

    plz = ''
    ort = plz_ort
    m_plz = re.match(r'(\d{5})\s+(.*)', plz_ort)
    if m_plz:
        plz = m_plz.group(1).strip()
        ort = m_plz.group(2).strip()

    status = 'Aktiv'
    badge_color = 'green'
    priority = 3

    if 'verstorben' in notizen.lower() or 'verstorben' in email.lower() or name_raw in ['Thomschy', 'Wilhelm (Stuber)']:
        status = 'Verstorben'
        badge_color = 'dark'
        priority = 99
    elif not strasse or 'keine anschrift' in strasse.lower():
        status = 'Keine Adresse'
        badge_color = 'red'
        priority = 1
    elif 'keine rückmeldung' in notizen.lower() or 'keine rückmeldung' in email.lower():
        status = 'Keine Rückmeldung (2006)'
        badge_color = 'orange'
        priority = 1
    elif not email or 'keine e-mail' in email.lower() or '@' not in email:
        status = 'Keine E-Mail'
        badge_color = 'yellow'
        priority = 2
    elif any(d in email.lower() for d in ['@aol.com', '@kabelmail.de', '@uni-heidelberg.de', '@familienheim']):
        status = 'E-Mail prüfen'
        badge_color = 'blue'
        priority = 2

    # Precision Search URLs
    search_terms = f'"{vorname} {main_name}"'
    if maiden_name:
        search_terms += f' OR "{vorname} {maiden_name}"'
    if ort:
        search_terms += f' ("{ort.split("-")[0]}" OR "Leimen" OR "Heidelberg")'
    else:
        search_terms += ' ("Leimen" OR "Heidelberg" OR "Rhein-Neckar")'
    google_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(search_terms)}'

    oertliche_url = f'https://www.dasoertliche.de/Themen/{urllib.parse.quote_plus(main_name)}/{urllib.parse.quote_plus(ort.split("-")[0] if ort else "Leimen")}.html'
    fb_dork = f'site:facebook.com ("{vorname} {main_name}"'
    if maiden_name:
        fb_dork += f' OR "{vorname} {maiden_name}"'
    fb_dork += f') ("{ort.split("-")[0] if ort else "Leimen"}" OR "Heidelberg" OR "Rhein-Neckar")'
    fb_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(fb_dork)}'

    prof_q = f'(site:linkedin.com/in/ OR site:xing.com/profile/) "{vorname} {main_name}"'
    prof_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(prof_q)}'

    trauer_q = f'(site:trauer.de OR site:gedenken.de OR site:trauerundgedenken.de OR site:rnz.de) "{vorname} {main_name}"'
    trauer_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(trauer_q)}'

    north_url = f'https://www.northdata.de/{urllib.parse.quote_plus(f"{vorname} {main_name}")}'
    stayfriends_url = f'https://www.stayfriends.de/Personen-Suche/{urllib.parse.quote_plus(main_name)}-{urllib.parse.quote_plus(vorname)}-P'

    insight = known_insights.get(name_raw, known_insights.get(main_name, ''))

    people.append({
        'name_raw': name_raw,
        'main_name': main_name,
        'maiden_name': maiden_name,
        'vorname': vorname,
        'strasse': strasse,
        'plz': plz,
        'ort': ort,
        'telefon': telefon,
        'email': email,
        'notizen': notizen,
        'status': status,
        'badge_color': badge_color,
        'priority': priority,
        'google_search_url': google_search_url,
        'oertliche_url': oertliche_url,
        'fb_search_url': fb_search_url,
        'prof_search_url': prof_search_url,
        'trauer_search_url': trauer_search_url,
        'north_url': north_url,
        'stayfriends_url': stayfriends_url,
        'insight': insight
    })

people.sort(key=lambda x: (x['priority'], x['main_name']))

with open('/home/peter/Projekte/active/Klassentreffen/Einladungsschreiben_Vorlage.md', 'r', encoding='utf-8') as f:
    einladung_text = f.read()

with open('/home/peter/Projekte/active/Klassentreffen/Antrag_Melderegisterauskunft_Vorlage.md', 'r', encoding='utf-8') as f:
    antrag_text = f.read()

rows_html = ""
for p in people:
    badge_cls = f"badge-{p['badge_color']}"
    maiden_str = f"<br><small class='text-muted'>geb. {p['maiden_name']}</small>" if p['maiden_name'] else ""
    insight_html = f"<div class='insight-box'><i class='fa-solid fa-lightbulb text-primary me-1'></i><strong>Fund:</strong> {p['insight']}</div>" if p['insight'] else ""
    notiz_html = f"<small class='text-danger d-block mt-1'><strong>Notiz:</strong> {p['notizen']}</small>" if p['notizen'] else ""
    prio_class = f"prio-{p['priority']}" if p['priority'] <= 3 else "prio-verstorben"

    email_display = p['email']
    if 'keine' in email_display.lower() or not email_display:
        email_display = f"<span class='text-muted fst-italic'>{email_display or 'keine E-Mail'}</span>"
    else:
        email_display = f"<a href='mailto:{email_display}'>{email_display}</a>"

    tel_display = f"<a href='tel:{p['telefon'].replace(' ', '')}' class='text-decoration-none text-dark fw-bold'>{p['telefon']}</a>" if p['telefon'] else "<span class='text-muted'>-</span>"

    rows_html += f"""
        <tr class="person-row {prio_class}" data-status="{p['status']}" data-search="{p['name_raw']} {p['vorname']} {p['ort']} {p['strasse']} {p['notizen']} {p['insight']}">
            <td><span class="badge {badge_cls} w-100 py-1">{p['status']}</span></td>
            <td>
                <strong>{p['main_name']}</strong>, {p['vorname']}
                {maiden_str}
            </td>
            <td>
                <div>{p['strasse'] or '<em class="text-muted">keine Straße</em>'}</div>
                <div class="text-muted small">{p['plz']} {p['ort']}</div>
            </td>
            <td>
                <div><i class="fa-solid fa-phone text-secondary me-1"></i>{tel_display}</div>
                <div><i class="fa-solid fa-envelope text-secondary me-1"></i>{email_display}</div>
            </td>
            <td>
                {insight_html}
                {notiz_html}
            </td>
            <td class="text-center">
                <a href="{p['google_search_url']}" target="_blank" class="btn btn-outline-primary btn-action" title="Google Websuche"><i class="fa-brands fa-google"></i> Google</a>
                <a href="{p['oertliche_url']}" target="_blank" class="btn btn-outline-success btn-action" title="Das Örtliche"><i class="fa-solid fa-address-book"></i> Telefon</a>
                <a href="{p['fb_search_url']}" target="_blank" class="btn btn-outline-info btn-action" title="Facebook Regions-Dork"><i class="fa-brands fa-facebook"></i> FB</a>
                <a href="{p['prof_search_url']}" target="_blank" class="btn btn-outline-secondary btn-action" title="LinkedIn & XING"><i class="fa-brands fa-linkedin"></i> Job</a>
                <a href="{p['trauer_search_url']}" target="_blank" class="btn btn-outline-dark btn-action" title="Trauerportale"><i class="fa-solid fa-cross"></i> Trauer</a>
                <a href="{p['north_url']}" target="_blank" class="btn btn-outline-warning btn-action" title="North Data"><i class="fa-solid fa-building"></i> Firma</a>
            </td>
        </tr>
    """

problem_cards_html = ""
problem_list = [p for p in people if p['priority'] <= 2]
for p in problem_list:
    badge_cls = f"badge-{p['badge_color']}"
    maiden_info = f"<span class='text-muted small'>(geb. {p['maiden_name']})</span>" if p['maiden_name'] else ""
    problem_cards_html += f"""
        <div class="col-md-6 col-lg-4 mb-3">
            <div class="problem-card h-100 d-flex flex-column justify-content-between">
                <div>
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="fw-bold mb-0 text-primary">{p['main_name']}, {p['vorname']} {maiden_info}</h6>
                        <span class="badge {badge_cls}">{p['status']}</span>
                    </div>
                    <div class="text-muted small mb-2"><i class="fa-solid fa-location-dot me-1"></i>{p['strasse'] or 'Keine Straße'}, {p['plz']} {p['ort']}</div>
                    <div class="insight-box mb-3">
                        <strong>Hinweis:</strong> {p['insight'] or p['notizen'] or 'Kontaktdaten prüfen'}
                    </div>
                </div>
                <div class="d-flex flex-wrap gap-1">
                    <a href="{p['stayfriends_url']}" target="_blank" class="btn btn-warning btn-sm btn-action text-dark"><i class="fa-solid fa-graduation-cap"></i> StayFriends</a>
                    <a href="{p['fb_search_url']}" target="_blank" class="btn btn-primary btn-sm btn-action"><i class="fa-brands fa-facebook"></i> FB Region</a>
                    <a href="{p['oertliche_url']}" target="_blank" class="btn btn-success btn-sm btn-action"><i class="fa-solid fa-phone"></i> Telefon</a>
                    <a href="{p['trauer_search_url']}" target="_blank" class="btn btn-secondary btn-sm btn-action"><i class="fa-solid fa-cross"></i> Trauer</a>
                </div>
            </div>
        </div>
    """

prio3_count = len([p for p in people if p['priority'] == 3])
prio2_count = len([p for p in people if p['priority'] == 2])
prio1_count = len([p for p in people if p['priority'] == 1])

html_template = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>50 Jahre Klassentreffen (1976–2026) – Klasse 10b</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #1e3a8a;
            --primary-dark: #0f172a;
            --accent: #38bdf8;
            --bg-light: #f8fafc;
            --card-border: #e2e8f0;
        }
        body { background-color: var(--bg-light); color: #1e293b; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .navbar-custom { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); padding: 16px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
        .nav-tabs .nav-link { color: #64748b; font-weight: 500; border: none; border-bottom: 3px solid transparent; padding: 12px 20px; }
        .nav-tabs .nav-link.active { color: #1e3a8a; font-weight: 700; border-bottom: 3px solid #1e3a8a; background: transparent; }
        .stat-card { background: white; border-radius: 12px; padding: 18px; border: 1px solid var(--card-border); box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s; }
        .stat-card:hover { transform: translateY(-2px); }
        .card-custom { background: white; border-radius: 12px; border: 1px solid var(--card-border); box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .badge-red { background-color: #ef4444; color: white; }
        .badge-orange { background-color: #f97316; color: white; }
        .badge-yellow { background-color: #f59e0b; color: #1e293b; }
        .badge-blue { background-color: #0284c7; color: white; }
        .badge-green { background-color: #10b981; color: white; }
        .badge-dark { background-color: #64748b; color: white; }
        .btn-action { padding: 4px 9px; font-size: 0.76rem; margin: 1px; border-radius: 5px; text-decoration: none; font-weight: 500; }
        .insight-box { background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 6px 10px; font-size: 0.82rem; margin-top: 4px; border-radius: 4px; }
        .problem-card { background: white; border: 1px solid #cbd5e1; border-radius: 10px; padding: 16px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
        .problem-card:hover { border-color: #0284c7; }
        .template-box { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; font-family: monospace; white-space: pre-wrap; font-size: 0.85rem; max-height: 500px; overflow-y: auto; }
        th { background-color: #0f172a !important; color: white !important; font-size: 0.85rem; vertical-align: middle; }
        td { font-size: 0.85rem; vertical-align: middle; }
    </style>
</head>
<body>

    <!-- Header Navigation -->
    <nav class="navbar navbar-dark navbar-custom mb-4">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <i class="fa-solid fa-graduation-cap text-warning fs-3 me-3"></i>
                <div>
                    <h5 class="text-white mb-0 fw-bold">50 Jahre Klassentreffen 1976 – 2026 (Klasse 10b)</h5>
                    <small class="text-white-50">Schulort Leimen / Rhein-Neckar | 35 Mitschüler | Recherche & Organisation</small>
                </div>
            </div>
            <div>
                <span class="badge bg-warning text-dark px-3 py-2 fw-bold"><i class="fa-solid fa-calendar-check me-1"></i> Jubiläumsjahr 2026</span>
            </div>
        </div>
    </nav>

    <div class="container-fluid px-md-4">

        <!-- Statistiken -->
        <div class="row g-3 mb-4">
            <div class="col-6 col-md-3">
                <div class="stat-card border-start border-primary border-4">
                    <div class="text-muted small fw-bold">Gesamtzahl</div>
                    <div class="fs-4 fw-bold text-primary">35 Mitschüler</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-card border-start border-success border-4">
                    <div class="text-muted small fw-bold">Prio 3: Vollständig</div>
                    <div class="fs-4 fw-bold text-success">__PRIO3__ Personen</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-card border-start border-warning border-4">
                    <div class="text-muted small fw-bold">Prio 2: Validierung / Mail</div>
                    <div class="fs-4 fw-bold text-warning">__PRIO2__ Personen</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-card border-start border-danger border-4">
                    <div class="text-muted small fw-bold">Prio 1: Problemfälle</div>
                    <div class="fs-4 fw-bold text-danger">__PRIO1__ Personen</div>
                </div>
            </div>
        </div>

        <!-- Haupt-Tabs -->
        <ul class="nav nav-tabs mb-4" id="mainTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="cockpit-tab" data-bs-toggle="tab" data-bs-target="#cockpit" type="button" role="tab"><i class="fa-solid fa-table-list me-2"></i>Klassenliste & Cockpit (35)</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="problems-tab" data-bs-toggle="tab" data-bs-target="#problems" type="button" role="tab"><i class="fa-solid fa-crosshairs me-2"></i>Präzisions-Recherche (Problemfälle)</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="templates-tab" data-bs-toggle="tab" data-bs-target="#templates" type="button" role="tab"><i class="fa-solid fa-envelope-open-text me-2"></i>Einladung & Behördenvorlage</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="report-tab" data-bs-toggle="tab" data-bs-target="#report" type="button" role="tab"><i class="fa-solid fa-file-lines me-2"></i>Recherche-Bericht & Spuren</button>
            </li>
        </ul>

        <!-- Tab Content -->
        <div class="tab-content" id="mainTabContent">

            <!-- TAB 1: COCKPIT -->
            <div class="tab-pane fade show active" id="cockpit" role="tabpanel">
                <div class="card card-custom p-3 mb-3">
                    <div class="row g-2 align-items-center">
                        <div class="col-md-5">
                            <div class="input-group">
                                <span class="input-group-text bg-light"><i class="fa-solid fa-search text-secondary"></i></span>
                                <input type="text" id="searchInput" class="form-control" placeholder="Schnellsuche nach Name, Mädchenname, Ort, Telefon...">
                            </div>
                        </div>
                        <div class="col-md-7 text-md-end">
                            <div class="btn-group flex-wrap" role="group">
                                <button type="button" class="btn btn-outline-secondary btn-sm filter-btn active" onclick="filterStatus('all', event)">Alle (35)</button>
                                <button type="button" class="btn btn-outline-danger btn-sm filter-btn" onclick="filterStatus('prio1', event)">Prio 1: Problemfälle</button>
                                <button type="button" class="btn btn-outline-warning btn-sm filter-btn" onclick="filterStatus('prio2', event)">Prio 2: Mail prüfen</button>
                                <button type="button" class="btn btn-outline-success btn-sm filter-btn" onclick="filterStatus('prio3', event)">Prio 3: Vollständig</button>
                                <button type="button" class="btn btn-outline-dark btn-sm filter-btn" onclick="filterStatus('verstorben', event)">Verstorben</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="table-responsive card card-custom mb-5">
                    <table class="table table-hover align-middle mb-0" id="peopleTable">
                        <thead>
                            <tr>
                                <th style="width: 130px;">Status</th>
                                <th>Name</th>
                                <th>Adresse / Ort</th>
                                <th>Telefon / E-Mail</th>
                                <th>Recherche-Fundstücke & Hinweise</th>
                                <th style="min-width: 250px;" class="text-center">1-Klick Recherche</th>
                            </tr>
                        </thead>
                        <tbody>
                            __ROWS__
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- TAB 2: PRÄZISIONS-RECHERCHE PROBLEM FÄLLE -->
            <div class="tab-pane fade" id="problems" role="tabpanel">
                <div class="alert alert-info border-0 shadow-sm mb-4">
                    <i class="fa-solid fa-shield-halved text-primary me-2 fs-5"></i>
                    <strong>Gefilterte Präzisions-Suche:</strong> Um Facebook-Spam zu vermeiden, nutzen diese Buttons vorkonfigurierte Regions-Filter (Leimen, Heidelberg, etc.), StayFriends-Schulsuche und Vorwahl-Abfragen.
                </div>

                <div class="row">
                    __PROBLEM_CARDS__
                </div>
            </div>

            <!-- TAB 3: VORLAGEN -->
            <div class="tab-pane fade" id="templates" role="tabpanel">
                <div class="row g-4 mb-5">
                    <div class="col-lg-6">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0"><i class="fa-solid fa-envelope me-2 text-primary"></i>Einladungsschreiben (50 Jahre)</h5>
                                <button class="btn btn-outline-primary btn-sm" onclick="copyTemplate('einladungText')"><i class="fa-solid fa-copy me-1"></i> Text kopieren</button>
                            </div>
                            <p class="text-muted small">Fertige Vorlage für Brief, E-Mail oder WhatsApp-Nachricht an die Mitschüler.</p>
                            <div class="template-box" id="einladungText">__EINLADUNG__</div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="fw-bold mb-0"><i class="fa-solid fa-building-columns me-2 text-primary"></i>Antrag Melderegisterauskunft (§ 44 BMG)</h5>
                                <button class="btn btn-outline-primary btn-sm" onclick="copyTemplate('antragText')"><i class="fa-solid fa-copy me-1"></i> Text kopieren</button>
                            </div>
                            <p class="text-muted small">Offizieller Antrag für das Bürgeramt Leimen (z. B. für Klaus Fellhauer).</p>
                            <div class="template-box" id="antragText">__ANTRAG__</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 4: BERICHT -->
            <div class="tab-pane fade" id="report" role="tabpanel">
                <div class="card card-custom p-4 mb-5">
                    <h4 class="fw-bold text-primary mb-3"><i class="fa-solid fa-chart-line me-2"></i>Ergebnisse der automatisierten Tiefen-Recherche</h4>
                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="p-3 bg-light rounded border">
                                <h6 class="fw-bold text-success"><i class="fa-solid fa-circle-check me-2"></i>Bestätigte Profile & Durchbrüche:</h6>
                                <ul class="small mb-0 ps-3">
                                    <li><strong>Peter Stegmaier:</strong> Als SPD-Bezirksbeirat in Mannheim-Gartenstadt aktiv.</li>
                                    <li><strong>Ralf Meffert:</strong> Senior Marketing Manager bei Gen Re (Köln), wohnhaft in Rösrath.</li>
                                    <li><strong>Dr. Holger Bögner:</strong> Zahnarztpraxis Frankfurt-Sachsenhausen (Darmstädter Landstr. 7–9, PLZ 60594).</li>
                                    <li><strong>Dr. Salvador Prieto-Durán:</strong> Facharzt Kinder- & Jugendpsychiatrie Frankfurt (Quirinsstr. 8).</li>
                                    <li><strong>Günther Bubenitschek:</strong> Erster Kriminalhauptkommissar a.D., Bundesverdienstkreuz, Sandhausen.</li>
                                    <li><strong>Hans-Peter Schilling:</strong> Leitender Wassermeister ZWH, Nov 2024 in den Ruhestand.</li>
                                    <li><strong>Bernhard Schneid:</strong> Vorstandsvorsitzender Weltladen Kraichtal e.V., Kraichtal.</li>
                                    <li><strong>Inge Stumpf-Schuhmacher:</strong> Ehem. Familienheim Heidelberg, seit 10/2022 im Ruhestand (Privatkontakt nutzen).</li>
                                    <li><strong>Uwe Lysowec:</strong> Musiker & Bassist (SOULMATES Kurpfalz), Gaiberg.</li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 bg-light rounded border">
                                <h6 class="fw-bold text-danger"><i class="fa-solid fa-triangle-exclamation me-2"></i>Wichtige Handlungs-Hinweise:</h6>
                                <ul class="small mb-0 ps-3">
                                    <li><strong>Rita Mößner (Schlegel):</strong> Vorwahl 06226 weist auf Hauptstraße in Mauer/Bammental/Meckesheim hin!</li>
                                    <li><strong>Michael Hack:</strong> Veraltete @kabelmail.de-Adresse bitte per Handynummer 0171/3337690 kontaktieren.</li>
                                    <li><strong>Klaus Fellhauer:</strong> Ehemalige Malscher Busunternehmer-Spur oder Melderegister Leimen nutzen.</li>
                                    <li><strong>Verstorbene Mitschüler:</strong> Klaus Thomschy († 2020), Inge Wilhelm geb. Stuber († 2024).</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function filterStatus(type, event) {
            var btns = document.querySelectorAll('.filter-btn');
            for (var i = 0; i < btns.length; i++) {
                btns[i].classList.remove('active');
            }
            if (event && event.target) {
                event.target.classList.add('active');
            }

            var rows = document.querySelectorAll('.person-row');
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                if (type === 'all') {
                    row.style.display = '';
                } else if (type === 'prio1') {
                    row.style.display = row.classList.contains('prio-1') ? '' : 'none';
                } else if (type === 'prio2') {
                    row.style.display = row.classList.contains('prio-2') ? '' : 'none';
                } else if (type === 'prio3') {
                    row.style.display = row.classList.contains('prio-3') ? '' : 'none';
                } else if (type === 'verstorben') {
                    row.style.display = row.classList.contains('prio-verstorben') ? '' : 'none';
                }
            }
        }

        document.getElementById('searchInput').addEventListener('keyup', function() {
            var term = this.value.toLowerCase();
            var rows = document.querySelectorAll('.person-row');
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                var text = (row.getAttribute('data-search') || '').toLowerCase();
                row.style.display = text.indexOf(term) > -1 ? '' : 'none';
            }
        });

        function copyTemplate(elemId) {
            var text = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(text).then(function() {
                alert('Text erfolgreich in die Zwischenablage kopiert!');
            });
        }
    </script>
</body>
</html>
"""

final_html = html_template.replace("__ROWS__", rows_html)
final_html = final_html.replace("__PROBLEM_CARDS__", problem_cards_html)
final_html = final_html.replace("__PRIO3__", str(prio3_count))
final_html = final_html.replace("__PRIO2__", str(prio2_count))
final_html = final_html.replace("__PRIO1__", str(prio1_count))
final_html = final_html.replace("__EINLADUNG__", einladung_text)
final_html = final_html.replace("__ANTRAG__", antrag_text)

with open('/home/peter/Projekte/active/Klassentreffen/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("index.html created successfully!")
