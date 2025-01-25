#https://github.com/gorhill/uBlock/wiki/Static-filter-syntax

# Filterregeln: Jedes Element ist ein Array mit [Wörter, inkludierte Domains, exkludierte Domains, upward-divs]
filter_regeln = [
    [["Beispieltext1"], [], ["domain1.com", "domain2.com", [".cssattribute"]], 2],  # Exkludierte Domains und CSS-Attribute
    [["Beispieltext2"], ["domain1.com", "domain2.com", [".cssattribute", ".cssattribute2"]], [], 1],  # Inkludierte Domains und CSS-Attribute
    [["Noch ein Text", "Ein anderer Text"], [], [], 3],  # Global gültig, 3 divs nach oben
    [["Testtext"], ["includedomain.com"], ["excludedomain.com", [".cssclass"]], ],  # Test leeres updward element; default 1
    [["Testtext"], ["includedomain.com"], ["excludedomain.com", [".cssclass"]] ]  # Test leeres updward array; default 1
]

# Ziel-Tags (z. B. 'a', 'p', 'div', etc.)
tags = ["a", "p"]

# Generiere Filter
filter_liste = []
global_filter_liste = []

for regel in filter_regeln:
    woerter = regel[0]  # Wörter, die gefiltert werden sollen
    include_domains = regel[1]  # Inkludierte Domains
    exclude_domains = regel[2]  # Exkludierte Domains
    upward_divs = regel[3] if len(regel) > 3 and regel[3] is not None else 1  # Standardwert für upward-divs ist 1, falls nicht angegeben

    for wort in woerter:
        # Die Anpassung für :upward(div, N) mit nth-of-type()
        # Wenn upward_divs > 1, wird nth-of-type(N) genutzt
        upward_filter = f":upward(div:nth-of-type({upward_divs}))" if upward_divs > 1 else ":upward(div)"

        tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i){upward_filter}" for tag in tags])

        # Funktion für das Anwenden von CSS-Attributen auf Domains
        def apply_css_attributes(domains, tag_filters, is_include):
            filter_strings = []
            domain_string = ",".join([domain for domain in domains if isinstance(domain, str)])  # Domains in Komma-Notation
            css_attributes = [domain for domain in domains if isinstance(domain, list)]  # CSS-Attribute extrahieren
            
            if domain_string:  # Falls es Domains gibt
                if is_include:
                    filter_strings.append(f"{domain_string}##{tag_filters}")  # Für include-Domains
                else:
                    filter_strings.append(f"{domain_string}#@#{tag_filters}")  # Für exclude-Domains

            # CSS-Attribute an Domain hinzufügen
            if css_attributes:
                for css_attr in css_attributes[0]:
                    if is_include:
                        filter_strings.append(f"{domain_string}##{css_attr}:has-text(/\\b{wort}\\b/i){upward_filter}")
                    else:
                        filter_strings.append(f"{domain_string}#@#{css_attr}:has-text(/\\b{wort}\\b/i){upward_filter}")
            
            return filter_strings

        # **Globale Filter sollen immer vor den anderen kommen, auch wenn keine include oder exclude Domains vorhanden sind**
        if not include_domains and not exclude_domains:
            global_filter_liste.append(f"##{tag_filters}")

        # Falls exkludierte Domains definiert sind
        if exclude_domains:
            # Globalen Filter immer vor den exkludierten Domains
            filter_liste.append(f"##{tag_filters}")  # Füge globalen Filter hinzu

            filter_strings = apply_css_attributes(exclude_domains, tag_filters, is_include=False)
            filter_liste.extend(filter_strings)

        # Falls inkludierte Domains definiert sind
        elif include_domains:
            filter_strings = apply_css_attributes(include_domains, tag_filters, is_include=True)
            filter_liste.extend(filter_strings)

        # Falls keine CSS-Attribute gesetzt sind, werden die Tags für a, p hinzugefügt
        if not any(isinstance(domain, list) for domain in include_domains + exclude_domains):
            # Wenn keine CSS-Attribute gesetzt wurden, füge Tags wie a, p hinzu
            if include_domains:
                filter_liste.append(f"{','.join(include_domains)}##{','.join(tags)}:has-text(/\\b{wort}\\b/i){upward_filter}")
            if exclude_domains:
                filter_liste.append(f"{','.join(exclude_domains)}#@#{','.join(tags)}:has-text(/\\b{wort}\\b/i){upward_filter}")

# Füge alle globalen Filter an den Anfang der Liste
filter_liste = global_filter_liste + filter_liste

# Speichere die Filter in einer Datei
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filter_liste))

print("Filterliste generiert: ublock_filter.txt")
