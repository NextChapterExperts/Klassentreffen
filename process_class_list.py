import zipfile, xml.etree.ElementTree as ET
import urllib.parse
import json, os, socket, re, csv

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

    # Extract maiden / alternative name in brackets
    maiden_name = ''
    main_name = name_raw
    m = re.search(r'([^(]+)\s*\(([^)]+)\)', name_raw)
    if m:
        main_name = m.group(1).strip()
        maiden_name = m.group(2).strip()

    # Extract PLZ and Ort
    plz = ''
    ort = plz_ort
    m_plz = re.match(r'(\d{5})\s+(.*)', plz_ort)
    if m_plz:
        plz = m_plz.group(1).strip()
        ort = m_plz.group(2).strip()

    # Determine status & priority
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

    # Search Query Construction
    search_terms = f'"{vorname} {main_name}"'
    if maiden_name:
        search_terms += f' OR "{vorname} {maiden_name}"'
    if ort:
        search_terms += f' ("{ort.split("-")[0]}" OR "Leimen" OR "Heidelberg")'
    else:
        search_terms += ' ("Leimen" OR "Heidelberg" OR "Rhein-Neckar")'
    google_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(search_terms)}'

    oertliche_url = f'https://www.dasoertliche.de/Themen/{urllib.parse.quote_plus(main_name)}/{urllib.parse.quote_plus(ort.split("-")[0] if ort else "Leimen")}.html'
    fb_q = f'site:facebook.com "{vorname} {main_name}"'
    if maiden_name:
        fb_q += f' OR "{vorname} {maiden_name}"'
    fb_search_url = f'https://www.google.com/search?q={urllib.parse.quote_plus(fb_q)}'

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

# Export CSV
csv_path = '/home/peter/Projekte/active/Klassentreffen/Klassenliste_10b_Recherche_Erweitert.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Status', 'Prioritaet', 'Nachname', 'Geburtsname', 'Vorname', 'Strasse', 'PLZ', 'Ort', 'Telefon', 'E-Mail', 'Bestehende Notizen', 'Recherche-Erkenntnisse', 'Google Search Link', 'Das Oertliche Link', 'Facebook Suche', 'Trauerportale Suche', 'North Data'])
    for p in people:
        writer.writerow([
            p['status'],
            p['priority'],
            p['main_name'],
            p['maiden_name'],
            p['vorname'],
            p['strasse'],
            p['plz'],
            p['ort'],
            p['telefon'],
            p['email'],
            p['notizen'],
            p['insight'],
            p['google_search_url'],
            p['oertliche_url'],
            p['fb_search_url'],
            p['trauer_search_url'],
            p['north_url']
        ])

# Export HTML Cockpit Dashboard
html_content = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Klassentreffen 50 Jahre (1976–2026) – Recherche Cockpit</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{ background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        .header-box {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .card-custom {{ border-radius: 10px; border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        .table-responsive {{ border-radius: 8px; overflow: hidden; background: white; }}
        .badge-red {{ background-color: #dc3545; color: white; }}
        .badge-orange {{ background-color: #fd7e14; color: white; }}
        .badge-yellow {{ background-color: #ffc107; color: #212529; }}
        .badge-blue {{ background-color: #0dcaf0; color: #212529; }}
        .badge-green {{ background-color: #198754; color: white; }}
        .badge-dark {{ background-color: #6c757d; color: white; }}
        .btn-action {{ padding: 3px 8px; font-size: 0.75rem; margin: 1px; border-radius: 4px; }}
        .insight-box {{ background-color: #e8f4fd; border-left: 3px solid #0d6efd; padding: 5px 8px; font-size: 0.82rem; margin-top: 4px; border-radius: 3px; }}
        .filter-btn.active {{ font-weight: bold; background-color: #0d6efd; color: white !important; }}
        th {{ background-color: #212529 !important; color: white !important; font-size: 0.85rem; vertical-align: middle; }}
        td {{ font-size: 0.85rem; vertical-align: middle; }}
    </style>
</head>
<body class="p-3 p-md-4">
    <div class="container-fluid">
        <div class="header-box d-flex flex-wrap justify-content-between align-items-center">
            <div>
                <h2 class="mb-1"><i class="fa-solid fa-graduation-cap me-2"></i>Klassentreffen Klasse 10b (1976) – Recherche Cockpit</h2>
                <p class="mb-0 text-white-50">50-jähriges Jubiläum | 35 Mitschüler | Automatisierte Recherche & Schnellzugriff</p>
            </div>
            <div class="text-end mt-2 mt-md-0">
                <span class="badge bg-light text-dark px-3 py-2 fs-6"><i class="fa-solid fa-users me-1"></i> 35 Einträge</span>
            </div>
        </div>

        <!-- Schnellstatistiken -->
        <div class="row g-3 mb-4">
            <div class="col-6 col-md-3">
                <div class="card card-custom p-3 text-center border-start border-danger border-4">
                    <div class="text-muted small">Prio 1: Dringend / Ohne Daten</div>
                    <div class="fs-4 fw-bold text-danger">{len([p for p in people if p['priority'] == 1])}</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="card card-custom p-3 text-center border-start border-warning border-4">
                    <div class="text-muted small">Prio 2: Validierung / Mail fehlt</div>
                    <div class="fs-4 fw-bold text-warning">{len([p for p in people if p['priority'] == 2])}</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="card card-custom p-3 text-center border-start border-success border-4">
                    <div class="text-muted small">Prio 3: Daten vorhanden</div>
                    <div class="fs-4 fw-bold text-success">{len([p for p in people if p['priority'] == 3])}</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="card card-custom p-3 text-center border-start border-secondary border-4">
                    <div class="text-muted small">Verstorben bekannt</div>
                    <div class="fs-4 fw-bold text-secondary">{len([p for p in people if p['priority'] == 99])}</div>
                </div>
            </div>
        </div>

        <!-- Filter & Suchleiste -->
        <div class="card card-custom p-3 mb-3">
            <div class="row g-2 align-items-center">
                <div class="col-md-5">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fa-solid fa-search"></i></span>
                        <input type="text" id="searchInput" class="form-control" placeholder="Tippen zum Suchen nach Name, Ort, Notiz...">
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

        <!-- Tabelle -->
        <div class="table-responsive card card-custom">
            <table class="table table-hover align-middle mb-0" id="peopleTable">
                <thead>
                    <tr>
                        <th style="width: 140px;">Status</th>
                        <th>Name</th>
                        <th>Adresse / Ort</th>
                        <th>Telefon / E-Mail</th>
                        <th>Recherche-Hinweise & Fundstücke</th>
                        <th style="min-width: 240px;" class="text-center">1-Klick Recherche</th>
                    </tr>
                </thead>
                <tbody>
'''

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

    html_content += f'''
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
                            <a href="{p['fb_search_url']}" target="_blank" class="btn btn-outline-info btn-action" title="Facebook Profile"><i class="fa-brands fa-facebook"></i> FB</a>
                            <a href="{p['prof_search_url']}" target="_blank" class="btn btn-outline-secondary btn-action" title="LinkedIn & XING"><i class="fa-brands fa-linkedin"></i> Job</a>
                            <a href="{p['trauer_search_url']}" target="_blank" class="btn btn-outline-dark btn-action" title="Trauerportale"><i class="fa-solid fa-cross"></i> Trauer</a>
                            <a href="{p['north_url']}" target="_blank" class="btn btn-outline-warning btn-action" title="North Data"><i class="fa-solid fa-building"></i> Firma</a>
                        </td>
                    </tr>
    '''

html_content += '''
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function filterStatus(type, event) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');

            const rows = document.querySelectorAll('.person-row');
            rows.forEach(row => {
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
            });
        }

        document.getElementById('searchInput').addEventListener('keyup', function() {
            const term = this.value.toLowerCase();
            document.querySelectorAll('.person-row').forEach(row => {
                const text = row.getAttribute('data-search').toLowerCase();
                row.style.display = text.includes(term) ? '' : 'none';
            });
        });
    </script>
</body>
</html>
'''

html_path = '/home/peter/Projekte/active/Klassentreffen/klassentreffen_recherche_cockpit.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Full 35-person batch update completed!')
