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

# Hilfsfunktion: Prüfen, ob ein Wort eine Domain (TLD) enthält
def contains_domain(word):
    # TLDs: einfache Prüfung auf typische Domain-Endungen
    tld_pattern = r"\b[\w-]+\.(com|org|net|de|io|info|co|ru|uk)\b"
    return re.match(tld_pattern, word)

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
    upward_divs = regel[3] if len(regel) > 3 else 1

    for wort in woerter:
        # Prüfen, ob das Wort eine Domain enthält
        domain_match = contains_domain(wort)

        # Standard-Filter (global)
        if not include_domains and not exclude_domains:
            tag_filters = ""
            if domain_match:  # Spezieller Filter für Domains
                tag_filters = f'a[href~="{wort}"]:upward(div),a:has-text(/\\b{wort}\\b/i):upward(div),p:has-text(/\\b{wort}\\b/i):upward(div)'
            else:  # Wenn keine Domain, dann nur allgemeine Textfilter ohne href
                tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])

            filter_liste.append(f"*##{tag_filters}")

        # Zusätzliche Regel für www.youtube.com
        if "www.youtube.com" not in exclude_domains:
            youtube_filter = f"www.youtube.com##.ytd-compact-video-renderer.style-scope:has-text(/\\b{wort}\\b/i)"
            filter_liste.append(youtube_filter)

        # Zusätzliche Regel für golem.de (mit default upward_divs = 2)
        if "golem.de" not in exclude_domains:
            golem_upward_divs = 2
            if domain_match:  # Wenn das Wort eine Domain ist, füge href hinzu
                golem_filter = f'golem.de##a[href~="{wort}"]:upward(div:nth-of-type({golem_upward_divs})),a:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({golem_upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({golem_upward_divs}))'
            else:  # Kein href, nur Textfilter
                golem_filter = f'golem.de##a:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({golem_upward_divs})),p:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({golem_upward_divs}))'
            filter_liste.append(golem_filter)

        # Filter für inkludierte Domains
        if include_domains:
            for domain in include_domains:
                tag_filters = ""
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(include_domains[:-1])}##{css_filters}")
                elif domain_match:  # Wenn das Wort eine Domain ist
                    tag_filters = f'a[href~="{wort}"]:upward(div),a:has-text(/\\b{wort}\\b/i):upward(div),p:has-text(/\\b{wort}\\b/i):upward(div)'
                    filter_liste.append(f"{domain}##{tag_filters}")
                else:  # Keine Domain, nur Textfilter
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}##{tag_filters}")

        # Filter für exkludierte Domains
        if exclude_domains:
            for domain in exclude_domains:
                tag_filters = ""
                if isinstance(domain, list):  # CSS-Attribute
                    css_filters = ",".join([f"{css}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{css}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for css in domain])
                    filter_liste.append(f"{','.join(exclude_domains[:-1])}#@#{css_filters}")
                elif domain_match:  # Wenn das Wort eine Domain ist
                    tag_filters = f'a[href~="{wort}"]:upward(div),a:has-text(/\\b{wort}\\b/i):upward(div),p:has-text(/\\b{wort}\\b/i):upward(div)'
                    filter_liste.append(f"{domain}#@#{tag_filters}")
                else:  # Keine Domain, nur Textfilter
                    tag_filters = ",".join([f"{tag}:has-text(/\\b{wort}\\b/i):upward(div)" if upward_divs == 1 else f"{tag}:has-text(/\\b{wort}\\b/i):upward(div:nth-of-type({upward_divs}))" for tag in tags])
                    filter_liste.append(f"{domain}#@#{tag_filters}")

# Datei speichern
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filter_liste))

print("Filterliste generiert: ublock_filter.txt")
