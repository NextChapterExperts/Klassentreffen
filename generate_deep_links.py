import urllib.parse
import json

problem_cases = [
    {
        "name": "Fellhauer, Klaus",
        "raw_name": "Klaus Fellhauer",
        "maiden": "",
        "status": "Dringend: Keine Adresse bekannt",
        "details": "In der Klassenliste steht 'keine Anschrift bekannt'.",
        "anomalies": "Spur: Ehemaliger Inhaber von 'Omnibusverkehr & Krankentransporte Klaus Fellhauer' in Malsch (Rhein-Neckar-Kreis) bzw. ehem. Heidelberg/Nußloch. Bei StayFriends oder im Melderegister suchen.",
        "search_term": "Klaus Fellhauer",
        "city": "Leimen",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Fellhauer-Klaus-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Klaus Fellhauer"),
            "LinkedIn": "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote("Klaus Fellhauer"),
            "XING": "https://www.xing.com/search/members?keywords=" + urllib.parse.quote("Klaus Fellhauer"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Fellhauer/Rhein-Neckar-Kreis.html",
            "Trauer.de": "https://www.trauer.de/suche/Klaus%20Fellhauer",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Klaus Fellhauer" ("Leimen" OR "Malsch" OR "Nußloch" OR "Heidelberg")')
        }
    },
    {
        "name": "Treiber, Heidi",
        "raw_name": "Heidi Treiber",
        "maiden": "",
        "status": "Unvollständig: Keine Straße / Telefon",
        "details": "Nur Ort 74909 Mönchzell und E-Mail treiber.heidi@yahoo.de vorhanden.",
        "anomalies": "Yahoo-Mail kann veraltet sein. Suche nach Festnetzanschlüssen 'Treiber' in Mönchzell / Meckesheim (Vorwahl 06226) oder Facebook-Profil.",
        "search_term": "Heidi Treiber",
        "city": "Mönchzell",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Treiber-Heidi-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Heidi Treiber"),
            "LinkedIn": "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote("Heidi Treiber"),
            "XING": "https://www.xing.com/search/members?keywords=" + urllib.parse.quote("Heidi Treiber"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Treiber/Meckesheim.html",
            "Trauer.de": "https://www.trauer.de/suche/Heidi%20Treiber",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Heidi Treiber" ("Mönchzell" OR "Meckesheim" OR "Leimen")')
        }
    },
    {
        "name": "Armbruster, Bärbel",
        "raw_name": "Bärbel Armbruster",
        "maiden": "Köhler",
        "status": "Prüfen: Keine E-Mail, Adresse prüfen",
        "details": "Adam-Opel-Weg 3, 69181 Leimen, Tel. 06224/74823.",
        "anomalies": "Im aktuellen Telefonbuch ist unter Adam-Opel-Weg 3 kein Eintrag 'Armbruster' mehr. Suche nach Bärbel Armbruster (geb. Köhler) oder Bärbel Köhler.",
        "search_term": "Bärbel Armbruster Köhler",
        "city": "Leimen",
        "links": {
            "StayFriends (Armbruster)": "https://www.stayfriends.de/Personen-Suche/Armbruster-B%C3%A4rbel-P",
            "StayFriends (Köhler)": "https://www.stayfriends.de/Personen-Suche/K%C3%B6hler-B%C3%A4rbel-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Bärbel Armbruster"),
            "Facebook (Köhler)": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Bärbel Köhler"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Armbruster/Leimen.html",
            "Trauer.de": "https://www.trauer.de/suche/B%C3%A4rbel%20Armbruster",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('("Bärbel Armbruster" OR "Bärbel Köhler") ("Leimen" OR "Sandhausen" OR "Heidelberg")')
        }
    },
    {
        "name": "Mößner, Rita",
        "raw_name": "Rita Mößner",
        "maiden": "Schlegel",
        "status": "Widerspruch: Adresse Leimen, aber Vorwahl 06226",
        "details": "Hauptstr. 65, 69181 Leimen, Tel. 06226/60545, rita_moessner@web.de.",
        "anomalies": "Wichtiger Fund: 06226 ist NICHT Leimen (06224), sondern Elsenztal / Bammental / Mauer / Lobbach / Meckesheim. Eventuell wohnt sie in einer Hauptstraße im Vorwahlbereich 06226!",
        "search_term": "Rita Mößner Schlegel",
        "city": "Leimen",
        "links": {
            "StayFriends (Mößner)": "https://www.stayfriends.de/Personen-Suche/M%C3%B6%C3%9Fner-Rita-P",
            "StayFriends (Schlegel)": "https://www.stayfriends.de/Personen-Suche/Schlegel-Rita-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Rita Mößner"),
            "Das Örtliche (06226)": "https://www.dasoertliche.de/Themen/M%C3%B6%C3%9Fner/Bammental.html",
            "Trauer.de": "https://www.trauer.de/suche/Rita%20M%C3%B6%C3%9Fner",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('("Rita Mößner" OR "Rita Moessner" OR "Rita Schlegel") ("Leimen" OR "Bammental" OR "Mauer" OR "Meckesheim")')
        }
    },
    {
        "name": "Stumpf, Silvia",
        "raw_name": "Silvia Stumpf",
        "maiden": "",
        "status": "Prüfen: Keine E-Mail",
        "details": "Kurpfalz-Centrum 5, 69181 Leimen, Tel. 06224/172500.",
        "anomalies": "Kurpfalz-Centrum ist ein großes Wohn-/Gewerbezentrum. Spur: Dr. Silvia Stumpf (Forschung Uni Heidelberg / KIT).",
        "search_term": "Silvia Stumpf",
        "city": "Leimen",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Stumpf-Silvia-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Silvia Stumpf"),
            "LinkedIn": "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote("Silvia Stumpf"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Stumpf/Leimen.html",
            "Trauer.de": "https://www.trauer.de/suche/Silvia%20Stumpf",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Silvia Stumpf" ("Leimen" OR "Heidelberg")')
        }
    },
    {
        "name": "Hack, Michael",
        "raw_name": "Michael Hack",
        "maiden": "",
        "status": "E-Mail prüfen: @kabelmail.de veraltet",
        "details": "Von-Stauffenberg-Str. 15, 66839 Schmelz, Handy 0171/3337690, michael.hack@kabelmail.de.",
        "anomalies": "Vodafone/Kabelmail-Dienste wurden stark umstrukturiert. Am besten direkt per Anruf/SMS/WhatsApp auf 0171/3337690 kontaktieren.",
        "search_term": "Michael Hack",
        "city": "Schmelz",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Hack-Michael-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Michael Hack Schmelz"),
            "LinkedIn": "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote("Michael Hack"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Hack/Schmelz.html",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Michael Hack" ("Schmelz" OR "Leimen")')
        }
    },
    {
        "name": "Struwe-Kraft, Petra",
        "raw_name": "Petra Struwe-Kraft",
        "maiden": "Kraft / Struwe",
        "status": "E-Mail prüfen: AOL-Adresse",
        "details": "Lerchenweg 23, 69168 Wiesloch, Tel. 06222/381220, Psiapp@aol.com.",
        "anomalies": "AOL-Postfächer werden oft nicht mehr aktiv abgerufen. Festnetz in Wiesloch 06222/381220 anrufen oder Post schicken.",
        "search_term": "Petra Struwe-Kraft",
        "city": "Wiesloch",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Struwe-Petra-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Petra Struwe"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Struwe/Wiesloch.html",
            "Trauer.de": "https://www.trauer.de/suche/Petra%20Struwe",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('("Petra Struwe-Kraft" OR "Petra Struwe" OR "Petra Kraft") "Wiesloch"')
        }
    },
    {
        "name": "Seltmann, Jürgen",
        "raw_name": "Jürgen Seltmann",
        "maiden": "",
        "status": "Unvollständig: Kein Telefon",
        "details": "Am Schlufter 17, 99091 Neudietendorf, jseltmann@gmx.de.",
        "anomalies": "GMX-Adresse aktiv testen oder postalisch anschreiben.",
        "search_term": "Jürgen Seltmann",
        "city": "Neudietendorf",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Seltmann-J%C3%BCrgen-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Jürgen Seltmann"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Seltmann/Neudietendorf.html",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Jürgen Seltmann" ("Neudietendorf" OR "Erfurt" OR "Leimen")')
        }
    },
    {
        "name": "Lindow, Jutta",
        "raw_name": "Jutta Lindow",
        "maiden": "",
        "status": "Prüfen: Freenet-Mail & Festnetz",
        "details": "Theodor-Heuss-Str. 117, 69181 Leimen-St. Ilgen, Tel. 06224/4490, j.lindow@freenet.de.",
        "anomalies": "Adresse in St. Ilgen. Festnetz 06224/4490 anrufen.",
        "search_term": "Jutta Lindow",
        "city": "Leimen-St. Ilgen",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Lindow-Jutta-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Jutta Lindow"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Lindow/Leimen.html",
            "Trauer.de": "https://www.trauer.de/suche/Jutta%20Lindow",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Jutta Lindow" ("Leimen" OR "St. Ilgen")')
        }
    },
    {
        "name": "Harlacher, Maria",
        "raw_name": "Maria Harlacher",
        "maiden": "Himmelmann",
        "status": "Prüfen: Web.de-Mail & Festnetz",
        "details": "Passein 8, 69198 Schriesheim, Tel. 06203/4309180, maria.harlacher@web.de.",
        "anomalies": "Suche nach Maria Harlacher oder Maria Himmelmann in Schriesheim.",
        "search_term": "Maria Harlacher Himmelmann",
        "city": "Schriesheim",
        "links": {
            "StayFriends (Harlacher)": "https://www.stayfriends.de/Personen-Suche/Harlacher-Maria-P",
            "StayFriends (Himmelmann)": "https://www.stayfriends.de/Personen-Suche/Himmelmann-Maria-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Maria Harlacher"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Harlacher/Schriesheim.html",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('("Maria Harlacher" OR "Maria Himmelmann") ("Schriesheim" OR "Leimen")')
        }
    },
    {
        "name": "Metzner, Christa",
        "raw_name": "Christa Metzner",
        "maiden": "Schemenauer",
        "status": "Prüfen: Outlook-Mail & Festnetz",
        "details": "Talstr. 19, 69181 Leimen, Tel. 06224/78172, christametzner@outlook.com.",
        "anomalies": "Suche nach Christa Metzner oder Christa Schemenauer in Leimen.",
        "search_term": "Christa Metzner Schemenauer",
        "city": "Leimen",
        "links": {
            "StayFriends (Metzner)": "https://www.stayfriends.de/Personen-Suche/Metzner-Christa-P",
            "StayFriends (Schemenauer)": "https://www.stayfriends.de/Personen-Suche/Schemenauer-Christa-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Christa Metzner"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Metzner/Leimen.html",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('("Christa Metzner" OR "Christa Schemenauer") "Leimen"')
        }
    },
    {
        "name": "Wellner, Richard",
        "raw_name": "Richard Wellner",
        "maiden": "",
        "status": "Prüfen: T-Online & Festnetz",
        "details": "Siedlerstr. 5a, 69181 Leimen-St. Ilgen, Tel. 06224/55336, RichardWellner@t-online.de.",
        "anomalies": "Adresse Siedlerstr. 5a in St. Ilgen. Festnetz 06224/55336 anrufen.",
        "search_term": "Richard Wellner",
        "city": "Leimen-St. Ilgen",
        "links": {
            "StayFriends": "https://www.stayfriends.de/Personen-Suche/Wellner-Richard-P",
            "Facebook": "https://www.facebook.com/search/people/?q=" + urllib.parse.quote("Richard Wellner"),
            "Das Örtliche": "https://www.dasoertliche.de/Themen/Wellner/Leimen.html",
            "Trauer.de": "https://www.trauer.de/suche/Richard%20Wellner",
            "Google Deep": "https://www.google.com/search?q=" + urllib.parse.quote('"Richard Wellner" ("Leimen" OR "St. Ilgen")')
        }
    }
]

# Generate specialized Deep-Search HTML Cockpit
html_out = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Problemfälle & 1-Klick Recherche-Zentrale (Klassentreffen 1976)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding-bottom: 50px; }
        .hero { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 12px; padding: 25px; margin-bottom: 25px; }
        .case-card { background-color: #1e293b; border: 1px solid #334155; border-radius: 10px; margin-bottom: 20px; transition: transform 0.2s, border-color 0.2s; }
        .case-card:hover { border-color: #38bdf8; transform: translateY(-2px); }
        .case-header { background-color: #24344d; padding: 12px 18px; border-top-left-radius: 9px; border-top-right-radius: 9px; border-bottom: 1px solid #334155; }
        .btn-link-action { padding: 6px 14px; font-size: 0.82rem; font-weight: 500; border-radius: 6px; margin: 3px; display: inline-flex; align-items: center; gap: 6px; text-decoration: none; }
        .btn-stayfriends { background-color: #f97316; color: white; border: none; }
        .btn-stayfriends:hover { background-color: #ea580c; color: white; }
        .btn-facebook { background-color: #1877f2; color: white; border: none; }
        .btn-facebook:hover { background-color: #1464cc; color: white; }
        .btn-linkedin { background-color: #0a66c2; color: white; border: none; }
        .btn-linkedin:hover { background-color: #084e96; color: white; }
        .btn-xing { background-color: #006567; color: white; border: none; }
        .btn-xing:hover { background-color: #004d4f; color: white; }
        .btn-oertliche { background-color: #10b981; color: white; border: none; }
        .btn-oertliche:hover { background-color: #059669; color: white; }
        .btn-trauer { background-color: #64748b; color: white; border: none; }
        .btn-trauer:hover { background-color: #475569; color: white; }
        .btn-google { background-color: #4285f4; color: white; border: none; }
        .btn-google:hover { background-color: #2b6cb0; color: white; }
        .anomaly-box { background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; margin-top: 10px; }
        .badge-urgent { background-color: #ef4444; color: white; font-size: 0.8rem; }
        .badge-warning-custom { background-color: #f59e0b; color: black; font-size: 0.8rem; }
    </style>
</head>
<body class="p-3 p-md-4">
    <div class="container">
        <div class="hero d-flex flex-wrap justify-content-between align-items-center">
            <div>
                <h2 class="text-white mb-1"><i class="fa-solid fa-crosshairs text-primary me-2"></i>Problemfälle & 1-Klick Recherche-Zentrale</h2>
                <p class="text-slate-400 mb-0 text-muted">Direkte Such- & Login-Links für die 12 unklaren / unvollständigen Mitschüler</p>
            </div>
            <div class="mt-3 mt-md-0">
                <a href="klassentreffen_recherche_cockpit.html" class="btn btn-outline-light"><i class="fa-solid fa-arrow-left me-1"></i> Zum Gesamt-Cockpit (35)</a>
            </div>
        </div>

        <div class="alert alert-info bg-dark border-info text-light mb-4">
            <i class="fa-solid fa-info-circle text-info me-2"></i>
            <strong>Anleitung:</strong> Klicken Sie bei jedem Fall auf die farbigen Buttons (StayFriends, Facebook, Telefonbuch, etc.). Die Suchbegriffe und Mädchennamen sind exakt vorformuliert. Wenn Sie in Ihrem Browser bei Facebook oder StayFriends eingeloggt sind, landen Sie direkt in den relevanten Suchtreffern!
        </div>

        <div class="row">
'''

for c in problem_cases:
    badge = 'badge-urgent' if 'Dringend' in c['status'] or 'Keine Adresse' in c['status'] else 'badge-warning-custom'
    links_html = ''
    for title, url in c['links'].items():
        btn_cls = 'btn-google'
        icon = 'fa-brands fa-google'
        if 'StayFriends' in title:
            btn_cls = 'btn-stayfriends'
            icon = 'fa-solid fa-graduation-cap'
        elif 'Facebook' in title:
            btn_cls = 'btn-facebook'
            icon = 'fa-brands fa-facebook'
        elif 'LinkedIn' in title:
            btn_cls = 'btn-linkedin'
            icon = 'fa-brands fa-linkedin'
        elif 'XING' in title:
            btn_cls = 'btn-xing'
            icon = 'fa-brands fa-xing'
        elif 'Örtliche' in title:
            btn_cls = 'btn-oertliche'
            icon = 'fa-solid fa-address-book'
        elif 'Trauer' in title:
            btn_cls = 'btn-trauer'
            icon = 'fa-solid fa-cross'

        links_html += f'<a href="{url}" target="_blank" class="btn-link-action {btn_cls}"><i class="{icon}"></i> {title}</a>'

    html_out += f'''
            <div class="col-12 mb-3">
                <div class="case-card">
                    <div class="case-header d-flex justify-content-between align-items-center flex-wrap">
                        <div>
                            <h5 class="text-white mb-0 fw-bold">{c['name']} {f"<span class='text-info small'>(geb. {c['maiden']})</span>" if c['maiden'] else ""}</h5>
                            <span class="text-muted small"><i class="fa-solid fa-location-dot me-1"></i>{c['city']}</span>
                        </div>
                        <span class="badge {badge} px-2 py-1">{c['status']}</span>
                    </div>
                    <div class="p-3">
                        <div class="row">
                            <div class="col-md-5">
                                <div class="text-slate-300 small mb-2"><strong>Aktueller Stand in Liste:</strong><br>{c['details']}</div>
                                <div class="anomaly-box">
                                    <i class="fa-solid fa-magnifying-glass text-warning me-1"></i>
                                    <strong>Recherche-Hinweis / Spur:</strong><br>{c['anomalies']}
                                </div>
                            </div>
                            <div class="col-md-7 mt-3 mt-md-0">
                                <div class="text-slate-300 small mb-2 fw-bold">1-Klick Recherche (direkt mit Ihrem Login):</div>
                                <div class="d-flex flex-wrap">
                                    {links_html}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    '''

html_out += '''
        </div>
    </div>
</body>
</html>
'''

with open('/home/peter/Projekte/active/Klassentreffen/problemfaelle_login_cockpit.html', 'w', encoding='utf-8') as f:
    f.write(html_out)

print("Generated problemfaelle_login_cockpit.html successfully!")
