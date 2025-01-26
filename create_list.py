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

# Hilfsfunktion zum Laden der TLDs aus der public_suffix_list.dat
def load_public_suffix_list(file_path):
    tlds = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("//"):  # Ignoriere leere Zeilen und Kommentare
                tlds.add(line)
    return tlds

# Beispiel für das Laden der Liste
tld_list = load_public_suffix_list('public_suffix_list.dat')
#print(tld_list)  # Überprüfe die geladenen TLDs

# Hilfsfunktion: Prüfen, ob ein Wort eine Domain (TLD) enthält
def contains_domain(word):
    domain_parts = word.split('.')
    if len(domain_parts) >= 2:  # Mindestens eine Subdomain und eine TLD
        tld = domain_parts[-1].split('/')[0].split('?')[0]  # Die TLD ist der letzte Teil
        return tld in tld_list
    return False

# Der Dateipfad zur Python-Datei, die das filter_regeln Array enthält
dateipfad = "filter_rules.py"

# Laden der Filterregeln
filter_regeln = lade_filter_regeln(dateipfad)

# Ziel-Tags (z. B. 'a', 'p', 'div', etc.)
tags = ["a", "p"]


# Generierte Filter
filter_liste = []

for regel in filter_regeln:
    woerter = regel[0]
    include_domains = regel[1]
    exclude_domains = regel[2]
    upward_divs = regel[3] if len(regel) > 3 and regel[3] is not None else 1  # Standardwert für upward-divs ist 1, falls nicht angegeben

    for wort in woerter:
        # Prüfen, ob das Wort eine Domain enthält
        domain_match = contains_domain(wort)

        # Standard-Filter (global)
        if not include_domains and not exclude_domains:
            tag_filters = ""
            if domain_match:  # Spezieller Filter für Domains
                tag_filters = f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs})),a:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))'
            else:  # Wenn keine Domain, dann nur allgemeine Textfilter ohne href
                tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])

            filter_liste.append(f"*##{tag_filters}")
            

        # Zusätzliche Regel für www.youtube.com
        if "www.youtube.com" not in exclude_domains:
            youtube_filter = f"www.youtube.com##.ytd-compact-video-renderer.style-scope:has-text(/\\b{wort}\\b/i)"
            filter_liste.append(youtube_filter)

        # Zusätzliche Regel für golem.de 
        if "golem.de" not in exclude_domains:
            golem_upward_divs = 1
            if domain_match:  # Wenn das Wort eine Domain ist, füge href hinzu
                golem_filter = f'golem.de##a[href~="{wort}"]:upward(li:nth-of-type({golem_upward_divs})),a:has-text(/\\b{wort}\\b/i):upward(li:nth-of-type({golem_upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(li:nth-of-type({golem_upward_divs}))'
            else:  # Kein href, nur Textfilter
                golem_filter = f'golem.de##a:has-text(/\\b{wort}\\b/i):upward(li:nth-of-type({golem_upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(li:nth-of-type({golem_upward_divs}))'
            filter_liste.append(golem_filter)
            exclude_domains.append("golem.de");
            

        # Filter für inkludierte Domains
        if include_domains:
            for domain in include_domains:
                tag_filters = ""
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(include_domains[:-1])}##{css_filters}")
                elif domain_match:  # Wenn das Wort eine Domain ist
                    tag_filters = f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs})),a:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))'
                    filter_liste.append(f"{domain}##{tag_filters}")
                else:  # Keine Domain, nur Textfilter
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}##{tag_filters}")

        # Filter für exkludierte Domains
        if exclude_domains:
            for domain in exclude_domains:
                tag_filters = ""
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(exclude_domains[:-1])}#@#{css_filters}")
                elif domain_match:  # Wenn das Wort eine Domain ist
                    tag_filters = f'a[href~="{wort}"]:upward(div:nth-of-type({upward_divs})),a:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))'
                    filter_liste.append(f"{domain}#@#{tag_filters}")
                else:  # Keine Domain, nur Textfilter
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}#@#{tag_filters}")

# Datei speichern
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filter_liste))

print("Filterliste generiert: ublock_filter.txt")
