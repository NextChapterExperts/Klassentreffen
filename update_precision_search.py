import urllib.parse
import json

problem_cases = [
    {
        "name": "Fellhauer, Klaus",
        "raw_name": "Klaus Fellhauer",
        "maiden": "",
        "status": "Dringend: Keine Adresse bekannt",
        "details": "In der Klassenliste steht 'keine Anschrift bekannt'.",
        "anomalies": "Spur: Ehemaliger Inhaber von 'Omnibusverkehr & Krankentransporte Klaus Fellhauer' in Malsch (Rhein-Neckar) bzw. ehem. Heidelberg/Nußloch.",
        "search_term": "Klaus Fellhauer",
        "city": "Leimen / Malsch / Heidelberg",
        "links": {
            "StayFriends Schule": "https://www.stayfriends.de/Schulen/Baden-Wuerttemberg/Leimen/Realschule/Otto-Graf-Realschule-S-7CG3-S",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com "Klaus Fellhauer" ("Leimen" OR "Malsch" OR "Nußloch" OR "Heidelberg" OR "Rhein-Neckar")'),
            "RNZ & Lokalpresse": "https://www.google.com/search?q=" + urllib.parse.quote('("Klaus Fellhauer" OR "Fellhauer") ("Malsch" OR "Nußloch" OR "Leimen") (site:rnz.de OR site:leimenblog.de OR site:morgenweb.de)'),
            "Das Örtliche (Rhein-Neckar)": "https://www.dasoertliche.de/Themen/Fellhauer/Rhein-Neckar-Kreis.html",
            "North Data Firmen": "https://www.northdata.de/" + urllib.parse.quote("Klaus Fellhauer"),
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('"Klaus Fellhauer" (site:trauer.de OR site:gedenken.de OR site:trauerundgedenken.de OR site:rnz.de)')
        }
    },
    {
        "name": "Treiber, Heidi",
        "raw_name": "Heidi Treiber",
        "maiden": "",
        "status": "Unvollständig: Keine Straße / Telefon",
        "details": "Nur Ort 74909 Mönchzell und E-Mail treiber.heidi@yahoo.de vorhanden.",
        "anomalies": "Mönchzell/Meckesheim hat Vorwahl 06226. Suche nach Verwandten oder Festnetzanschlüssen 'Treiber' vor Ort.",
        "search_term": "Heidi Treiber",
        "city": "Mönchzell / Meckesheim (06226)",
        "links": {
            "StayFriends Schule": "https://www.stayfriends.de/Schulen/Baden-Wuerttemberg/Leimen/Realschule/Otto-Graf-Realschule-S-7CG3-S",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com "Heidi Treiber" ("Mönchzell" OR "Meckesheim" OR "Leimen" OR "Heidelberg" OR "74909")'),
            "Das Örtliche (Meckesheim)": "https://www.dasoertliche.de/Themen/Treiber/Meckesheim.html",
            "Lokalpresse Elsenztal": "https://www.google.com/search?q=" + urllib.parse.quote('"Heidi Treiber" ("Mönchzell" OR "Meckesheim" OR "Leimen") (site:rnz.de OR site:morgenweb.de)'),
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('"Heidi Treiber" (site:trauer.de OR site:gedenken.de OR site:trauerundgedenken.de)')
        }
    },
    {
        "name": "Armbruster, Bärbel",
        "raw_name": "Bärbel Armbruster",
        "maiden": "Köhler",
        "status": "Prüfen: Keine E-Mail, Adresse prüfen",
        "details": "Adam-Opel-Weg 3, 69181 Leimen, Tel. 06224/74823.",
        "anomalies": "Am Adam-Opel-Weg 3 nicht mehr gelistet. Unbedingt auch mit Mädchenname 'Bärbel Köhler' oder 'Köhler Leimen' suchen.",
        "search_term": "Bärbel Armbruster Köhler",
        "city": "Leimen / Sandhausen (06224)",
        "links": {
            "StayFriends (Armbruster)": "https://www.stayfriends.de/Personen-Suche/Armbruster-B%C3%A4rbel-P",
            "StayFriends (Köhler)": "https://www.stayfriends.de/Personen-Suche/K%C3%B6hler-B%C3%A4rbel-P",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com ("Bärbel Armbruster" OR "Bärbel Köhler") ("Leimen" OR "Sandhausen" OR "Heidelberg" OR "Nußloch")'),
            "Das Örtliche (Leimen)": "https://www.dasoertliche.de/Themen/Armbruster/Leimen.html",
            "Das Örtliche (Köhler Leimen)": "https://www.dasoertliche.de/Themen/K%C3%B6hler/Leimen.html",
            "Lokalpresse Leimen": "https://www.google.com/search?q=" + urllib.parse.quote('("Bärbel Armbruster" OR "Bärbel Köhler") (site:leimenblog.de OR site:rnz.de)'),
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('("Bärbel Armbruster" OR "Bärbel Köhler") (site:trauer.de OR site:gedenken.de OR site:rnz.de)')
        }
    },
    {
        "name": "Mößner, Rita",
        "raw_name": "Rita Mößner",
        "maiden": "Schlegel",
        "status": "Widerspruch: Adresse Leimen, aber Vorwahl 06226",
        "details": "Hauptstr. 65, 69181 Leimen, Tel. 06226/60545, rita_moessner@web.de.",
        "anomalies": "Vorwahl 06226 gehört zu Bammental, Mauer, Meckesheim, Lobbach. Vermutlich Adresse in einer Hauptstraße im Vorwahlbereich 06226!",
        "search_term": "Rita Mößner Schlegel",
        "city": "Elsenztal (06226) / Leimen",
        "links": {
            "StayFriends (Schlegel)": "https://www.stayfriends.de/Personen-Suche/Schlegel-Rita-P",
            "StayFriends (Mößner)": "https://www.stayfriends.de/Personen-Suche/M%C3%B6%C3%9Fner-Rita-P",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com ("Rita Mößner" OR "Rita Moessner" OR "Rita Schlegel") ("Leimen" OR "Bammental" OR "Mauer" OR "Meckesheim" OR "Lobbach")'),
            "Das Örtliche (06226 Elsenztal)": "https://www.dasoertliche.de/Themen/M%C3%B6%C3%9Fner/Bammental.html",
            "Das Örtliche (Schlegel 06226)": "https://www.dasoertliche.de/Themen/Schlegel/Bammental.html",
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('("Rita Mößner" OR "Rita Moessner" OR "Rita Schlegel") (site:trauer.de OR site:gedenken.de OR site:rnz.de)')
        }
    },
    {
        "name": "Stumpf, Silvia",
        "raw_name": "Silvia Stumpf",
        "maiden": "",
        "status": "Prüfen: Keine E-Mail",
        "details": "Kurpfalz-Centrum 5, 69181 Leimen, Tel. 06224/172500.",
        "anomalies": "Kurpfalz-Centrum ist ein großes Ärzte- und Wohnzentrum in Leimen. Spur: Dr. Silvia Stumpf (Forschung Uni Heidelberg / KIT).",
        "search_term": "Silvia Stumpf",
        "city": "Leimen / Heidelberg",
        "links": {
            "StayFriends Schule": "https://www.stayfriends.de/Schulen/Baden-Wuerttemberg/Leimen/Realschule/Otto-Graf-Realschule-S-7CG3-S",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com "Silvia Stumpf" ("Leimen" OR "Heidelberg" OR "Sandhausen" OR "Nußloch")'),
            "LinkedIn Profile": "https://www.linkedin.com/search/results/people/?keywords=" + urllib.parse.quote("Silvia Stumpf Heidelberg"),
            "Das Örtliche (Leimen)": "https://www.dasoertliche.de/Themen/Stumpf/Leimen.html",
            "Lokalpresse Leimen": "https://www.google.com/search?q=" + urllib.parse.quote('"Silvia Stumpf" (site:leimenblog.de OR site:rnz.de)'),
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('"Silvia Stumpf" (site:trauer.de OR site:gedenken.de OR site:rnz.de)')
        }
    },
    {
        "name": "Hack, Michael",
        "raw_name": "Michael Hack",
        "maiden": "",
        "status": "E-Mail prüfen: @kabelmail.de veraltet",
        "details": "Von-Stauffenberg-Str. 15, 66839 Schmelz, Handy 0171/3337690, michael.hack@kabelmail.de.",
        "anomalies": "Mobilfunknummer 0171/3337690 ist vorhanden. Direkt per Anruf oder WhatsApp kontaktieren.",
        "search_term": "Michael Hack",
        "city": "Schmelz (Saarland)",
        "links": {
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com "Michael Hack" ("Schmelz" OR "Saarland" OR "Lebach" OR "Leimen")'),
            "Das Örtliche (Schmelz)": "https://www.dasoertliche.de/Themen/Hack/Schmelz.html",
            "WhatsApp Web Chat": "https://wa.me/491713337690",
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('"Michael Hack" "Schmelz" (site:trauer.de OR site:saarbruecker-zeitung.trauer.de)')
        }
    },
    {
        "name": "Struwe-Kraft, Petra",
        "raw_name": "Petra Struwe-Kraft",
        "maiden": "Kraft / Struwe",
        "status": "E-Mail prüfen: AOL-Adresse",
        "details": "Lerchenweg 23, 69168 Wiesloch, Tel. 06222/381220, Psiapp@aol.com.",
        "anomalies": "Festnetzanschluss 06222/381220 und Postanschrift Lerchenweg 23 in Wiesloch nutzen.",
        "search_term": "Petra Struwe-Kraft",
        "city": "Wiesloch (06222)",
        "links": {
            "StayFriends (Struwe)": "https://www.stayfriends.de/Personen-Suche/Struwe-Petra-P",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com ("Petra Struwe" OR "Petra Kraft" OR "Petra Struwe-Kraft") ("Wiesloch" OR "Walldorf" OR "Leimen")'),
            "Das Örtliche (Wiesloch)": "https://www.dasoertliche.de/Themen/Struwe/Wiesloch.html",
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('("Petra Struwe" OR "Petra Kraft") (site:trauer.de OR site:gedenken.de OR site:rnz.de)')
        }
    },
    {
        "name": "Seltmann, Jürgen",
        "raw_name": "Jürgen Seltmann",
        "maiden": "",
        "status": "Unvollständig: Kein Telefon",
        "details": "Am Schlufter 17, 99091 Neudietendorf, jseltmann@gmx.de.",
        "anomalies": "Anschrift in Thüringen (Neudietendorf bei Erfurt).",
        "search_term": "Jürgen Seltmann",
        "city": "Neudietendorf / Erfurt",
        "links": {
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com "Jürgen Seltmann" ("Neudietendorf" OR "Erfurt" OR "Gotha" OR "Leimen")'),
            "Das Örtliche (Neudietendorf)": "https://www.dasoertliche.de/Themen/Seltmann/Neudietendorf.html",
            "Trauer & Gedenken": "https://www.google.com/search?q=" + urllib.parse.quote('"Jürgen Seltmann" ("Neudietendorf" OR "Erfurt") (site:trauer.de OR site:gedenken.de)')
        }
    },
    {
        "name": "Harlacher, Maria",
        "raw_name": "Maria Harlacher",
        "maiden": "Himmelmann",
        "status": "Prüfen: Web.de-Mail & Festnetz",
        "details": "Passein 8, 69198 Schriesheim, Tel. 06203/4309180, maria.harlacher@web.de.",
        "anomalies": "Suche nach Maria Harlacher und Maria Himmelmann in Schriesheim.",
        "search_term": "Maria Harlacher Himmelmann",
        "city": "Schriesheim (06203)",
        "links": {
            "StayFriends (Himmelmann)": "https://www.stayfriends.de/Personen-Suche/Himmelmann-Maria-P",
            "StayFriends (Harlacher)": "https://www.stayfriends.de/Personen-Suche/Harlacher-Maria-P",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com ("Maria Harlacher" OR "Maria Himmelmann") ("Schriesheim" OR "Heidelberg" OR "Leimen")'),
            "Das Örtliche (Schriesheim)": "https://www.dasoertliche.de/Themen/Harlacher/Schriesheim.html",
            "Lokalpresse Schriesheim/RNZ": "https://www.google.com/search?q=" + urllib.parse.quote('("Maria Harlacher" OR "Maria Himmelmann") (site:rnz.de OR site:morgenweb.de)')
        }
    },
    {
        "name": "Metzner, Christa",
        "raw_name": "Christa Metzner",
        "maiden": "Schemenauer",
        "status": "Prüfen: Outlook-Mail & Festnetz",
        "details": "Talstr. 19, 69181 Leimen, Tel. 06224/78172, christametzner@outlook.com.",
        "anomalies": "Suche nach Christa Metzner und Mädchenname Christa Schemenauer in Leimen.",
        "search_term": "Christa Metzner Schemenauer",
        "city": "Leimen (06224)",
        "links": {
            "StayFriends (Schemenauer)": "https://www.stayfriends.de/Personen-Suche/Schemenauer-Christa-P",
            "StayFriends (Metzner)": "https://www.stayfriends.de/Personen-Suche/Metzner-Christa-P",
            "FB Präzise (Google Dork)": "https://www.google.com/search?q=" + urllib.parse.quote('site:facebook.com ("Christa Metzner" OR "Christa Schemenauer") ("Leimen" OR "Heidelberg" OR "Nußloch")'),
            "Das Örtliche (Leimen)": "https://www.dasoertliche.de/Themen/Metzner/Leimen.html",
            "Das Örtliche (Schemenauer Leimen)": "https://www.dasoertliche.de/Themen/Schemenauer/Leimen.html"
        }
    }
]

html_out = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Präzisions-Recherche & Login-Zentrale (Ohne Facebook-Müll)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0b132b; color: #e0e6ed; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding-bottom: 60px; }
        .hero { background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%); border: 1px solid #3a506b; border-radius: 12px; padding: 25px; margin-bottom: 25px; }
        .case-card { background-color: #1c2541; border: 1px solid #3a506b; border-radius: 10px; margin-bottom: 20px; transition: transform 0.2s, border-color 0.2s; }
        .case-card:hover { border-color: #48cae4; transform: translateY(-2px); }
        .case-header { background-color: #24344d; padding: 12px 18px; border-top-left-radius: 9px; border-top-right-radius: 9px; border-bottom: 1px solid #3a506b; }
        .btn-link-action { padding: 6px 13px; font-size: 0.82rem; font-weight: 500; border-radius: 6px; margin: 3px; display: inline-flex; align-items: center; gap: 6px; text-decoration: none; }
        
        .btn-stayfriends { background-color: #f97316; color: white; border: none; }
        .btn-stayfriends:hover { background-color: #ea580c; color: white; }
        
        .btn-fb-dork { background-color: #1877f2; color: white; border: none; }
        .btn-fb-dork:hover { background-color: #0d6efd; color: white; }
        
        .btn-oertliche { background-color: #10b981; color: white; border: none; }
        .btn-oertliche:hover { background-color: #059669; color: white; }
        
        .btn-presse { background-color: #8b5cf6; color: white; border: none; }
        .btn-presse:hover { background-color: #7c3aed; color: white; }

        .btn-trauer { background-color: #64748b; color: white; border: none; }
        .btn-trauer:hover { background-color: #475569; color: white; }

        .btn-whatsapp { background-color: #25d366; color: white; border: none; }
        .btn-whatsapp:hover { background-color: #128c7e; color: white; }

        .btn-firma { background-color: #f59e0b; color: black; border: none; }
        .btn-firma:hover { background-color: #d97706; color: black; }

        .anomaly-box { background-color: #141c30; border-left: 4px solid #48cae4; padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; margin-top: 10px; }
        .badge-urgent { background-color: #ef4444; color: white; font-size: 0.8rem; }
        .badge-warning-custom { background-color: #f59e0b; color: black; font-size: 0.8rem; }
        .tip-banner { background-color: #14213d; border-left: 4px solid #fca311; padding: 14px; border-radius: 6px; margin-bottom: 25px; }
    </style>
</head>
<body class="p-3 p-md-4">
    <div class="container">
        <div class="hero d-flex flex-wrap justify-content-between align-items-center">
            <div>
                <h2 class="text-white mb-1"><i class="fa-solid fa-crosshairs text-info me-2"></i>Präzisions-Recherche (Gefiltert nach Region & Schule)</h2>
                <p class="text-muted mb-0">Kein Facebook-Spam: Gezielte Regions-Dorks, StayFriends-Schulsuche, Lokalpresse-Archive & Vorwahl-Abfragen</p>
            </div>
            <div class="mt-3 mt-md-0">
                <a href="klassentreffen_recherche_cockpit.html" class="btn btn-outline-light"><i class="fa-solid fa-arrow-left me-1"></i> Gesamtübersicht (35)</a>
            </div>
        </div>

        <div class="tip-banner">
            <h6 class="fw-bold text-warning mb-1"><i class="fa-solid fa-shield-halved me-2"></i>Warum die normale Facebook-Suche scheitert – und wie wir es gelöst haben:</h6>
            <div class="small text-light">
                Die interne Facebook-Suche zeigt hunderte irrelevante Personen aus ganz Deutschland/Welt. Wir nutzen daher <strong>Regions-Dorks</strong>: Die Buttons <code>FB Präzise</code> zwingen Google, Facebook <strong>nur</strong> nach Profilen mit Bezug zu <em>Leimen, Heidelberg, Nußloch, Sandhausen, Wiesloch</em> etc. zu durchsuchen.
            </div>
        </div>

        <div class="row">
'''

for c in problem_cases:
    badge = 'badge-urgent' if 'Dringend' in c['status'] or 'Keine Adresse' in c['status'] else 'badge-warning-custom'
    links_html = ''
    for title, url in c['links'].items():
        btn_cls = 'btn-presse'
        icon = 'fa-solid fa-newspaper'
        if 'StayFriends' in title:
            btn_cls = 'btn-stayfriends'
            icon = 'fa-solid fa-graduation-cap'
        elif 'FB' in title:
            btn_cls = 'btn-fb-dork'
            icon = 'fa-brands fa-facebook'
        elif 'Örtliche' in title:
            btn_cls = 'btn-oertliche'
            icon = 'fa-solid fa-address-book'
        elif 'Trauer' in title:
            btn_cls = 'btn-trauer'
            icon = 'fa-solid fa-cross'
        elif 'WhatsApp' in title:
            btn_cls = 'btn-whatsapp'
            icon = 'fa-brands fa-whatsapp'
        elif 'Firma' in title or 'North' in title:
            btn_cls = 'btn-firma'
            icon = 'fa-solid fa-building'

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
                                    <i class="fa-solid fa-lightbulb text-info me-1"></i>
                                    <strong>Such-Spur & Anomalie:</strong><br>{c['anomalies']}
                                </div>
                            </div>
                            <div class="col-md-7 mt-3 mt-md-0">
                                <div class="text-slate-300 small mb-2 fw-bold">Gefilterte 1-Klick Recherche:</div>
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

print("Precision search cockpit generated successfully!")
