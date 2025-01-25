# Filterregeln: Jedes Element ist ein Array mit [Wörter, inkludierte Domains, exkludierte Domains, upward-divs]
filter_regeln = [
    [["Beispieltext1"], ["example.com", "another-examplea.com"], [], 2],  # Inkludierte Domains, 2 divs nach oben
    [["Beispieltext2"], [], ["testseite.de", "noch-eine-seite.de"], 1],  # Exkludierte Domains, 1 div nach oben
    [["Noch ein Text", "Ein anderer Text"], [], [], 3],  # Global gültig, 3 divs nach oben
    [["Noch ein Text", "Ein anderer Text"], [], []],  # Kein upward-divs angegeben, Standardwert 1
    [["Noch ein Text", "Ein anderer Text"], [], []],  # Noch ein Beispiel ohne upward-divs
]

# Ziel-Tags (z. B. 'a', 'p', 'div', etc.)
tags = ["a", "p"]

# Generiere Filter
filter_liste = []
for regel in filter_regeln:
    woerter = regel[0]  # Wörter, die gefiltert werden sollen
    include_domains = regel[1]  # Inkludierte Domains
    exclude_domains = regel[2]  # Exkludierte Domains
    upward_divs = regel[3] if len(regel) > 3 and regel[3] is not None else 1  # Standardwert für upward-divs ist 1, falls nicht angegeben oder leer

    for wort in woerter:
        # Die Anpassung für :upward(div, N) mit nth-of-type()
        tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
        
        # Standard: Gilt für alle Seiten (zuerst prüfen, um Gewichtung der Regeln zu beachten)
        #if not include_domains and not exclude_domains:
        if not include_domains:
            filter_liste.append(f"##{tag_filters}")
        
        # Falls exkludierte Domains definiert sind
        elif exclude_domains:
            exclude_filter = f"{','.join(exclude_domains)}#@#{tag_filters}"
            filter_liste.append(exclude_filter)
        
        # Falls inkludierte Domains definiert sind
        elif include_domains:
            for domain in include_domains:
                filter_liste.append(f"{domain}##{tag_filters}")

# Speichere die Filter in einer Datei
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filter_liste))

print("Filterliste generiert: ublock_filter.txt")
