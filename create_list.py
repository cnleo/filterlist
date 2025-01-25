import os
import importlib.util
import re  # Für das Erkennen von Domains

# Funktion zum Laden der Filterregeln aus einer Python-Datei
def lade_filter_regeln(dateipfad):
    if os.path.exists(dateipfad):
        spec = importlib.util.spec_from_file_location("filter_regeln", dateipfad)
        filter_regeln_modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(filter_regeln_modul)
        return filter_regeln_modul.filter_regeln  # Gibt die filter_regeln-Variable aus der Datei zurück
    else:
        print(f"Die Datei {dateipfad} wurde nicht gefunden.")
        return []

# Der Dateipfad zur Python-Datei, die das filter_regeln Array enthält
dateipfad = "filter_rules.py"

# Laden der Filterregeln
filter_regeln = lade_filter_regeln(dateipfad)

# Ziel-Tags (z. B. 'a', 'p', 'div', etc.)
tags = ["a", "p"]

# Generiere Filter
filter_liste = []
global_filter_liste = []

# Funktion zum Erkennen von Domains in einem Wort
def contains_domain(word):
    # Regex zum Erkennen von Domainmustern (z.B. meinedomain.com, beispiel.org, etc.)
    domain_pattern = re.compile(r"\b[A-Za-z0-9.-]+\.[a-zA-Z]{2,}\b")
    return bool(domain_pattern.search(word))

for regel in filter_regeln:
    woerter = regel[0]  # Wörter, die gefiltert werden sollen
    include_domains = regel[1]  # Inkludierte Domains
    exclude_domains = regel[2]  # Exkludierte Domains
    upward_divs = regel[3] if len(regel) > 3 and regel[3] is not None else 1  # Standardwert für upward-divs ist 1, falls nicht angegeben

    for wort in woerter:
        # Prüfen, ob das Wort eine Domain enthält
        domain_match = contains_domain(wort)

        # Standard-Filter (global)
        if not include_domains and not exclude_domains:
            if domain_match:  # Spezieller Filter für Domains
                tag_filters = ",".join([f'a[href~="{wort}"]:upward(div)' if upward_divs == 1 else f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs}))'])
                filter_liste.append(f"##{tag_filters}")
            else:
                tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                filter_liste.append(f"##{tag_filters}")

        # Filter für inkludierte Domains
        if include_domains:
            for domain in include_domains:
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(include_domains[:-1])}##{css_filters}")
                elif domain_match:  # Wenn Domain im Wort
                    tag_filters = ",".join([f'a[href~="{wort}"]:upward(div)' if upward_divs == 1 else f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs}))'])
                    filter_liste.append(f"{domain}##{tag_filters}")
                else:
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}##{tag_filters}")

        # Filter für exkludierte Domains
        if exclude_domains:
            for domain in exclude_domains:
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(exclude_domains[:-1])}#@#{css_filters}")
                elif domain_match:  # Wenn Domain im Wort
                    tag_filters = ",".join([f'a[href~="{wort}"]:upward(div)' if upward_divs == 1 else f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs}))'])
                    filter_liste.append(f"{domain}#@#{tag_filters}")
                else:
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}#@#{tag_filters}")

# Speichere die Filter in einer Datei
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filter_liste))

print("Filterliste generiert: ublock_filter.txt")
