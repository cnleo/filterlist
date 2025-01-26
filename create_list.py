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
filter_liste = set()  # Set statt Liste verwenden, um doppelte Einträge zu vermeiden

for regel in filter_regeln:
    woerter = regel[0]
    include_domains = regel[1]
    exclude_domains = regel[2]
    upward_divs = regel[3] if len(regel) > 3 and regel[3] is not None else 1  # Standardwert für upward-divs ist 1, falls nicht angegeben

    for wort in woerter:
        domain_match = contains_domain(wort)

        # Standard-Filter (global)
        if not include_domains and not exclude_domains:
            for tag in tags:
                if domain_match:  # Spezieller Filter für Domains
                    filter_liste.add(f'*##a[href~="{wort}"]:upward(div)')
                filter_liste.add(f'*##{tag}:has-text(/\\b{wort}\'?s?\\b/i):upward(div)')

        # Filter für YouTube
        if "www.youtube.com" not in exclude_domains:
            filter_liste.add(f"www.youtube.com##.ytd-compact-video-renderer.style-scope:has-text(/\\b{wort}\'?s?\\b/i)")

        # Filter für Golem
        if "golem.de" not in exclude_domains:
            for tag in tags:
                if domain_match:
                    filter_liste.add(f'golem.de##a[href~="{wort}"]:upward(li)')
                filter_liste.add(f'golem.de##{tag}:has-text(/\\b{wort}\'?s?\\b/i):upward(li)')
            exclude_domains.append("golem.de")

        # Filter für inkludierte Domains
        if include_domains:
            for domain in include_domains:
                for tag in tags:
                    if domain_match:
                        filter_liste.add(f"{domain}##a[href~='{wort}']:upward(div)")
                    filter_liste.add(f"{domain}##{tag}:has-text(/\\b{wort}\'?s?\\b/i):upward(div)")

        # Filter für exkludierte Domains
        if exclude_domains:
            for domain in exclude_domains:
                for tag in tags:
                    if domain_match:
                        filter_liste.add(f"{domain}#@#a[href~='{wort}']:upward(div)")
                    filter_liste.add(f"{domain}#@#{tag}:has-text(/\\b{wort}\'?s?\\b/i):upward(div)")

# Datei speichern
with open("ublock_filter.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(sorted(filter_liste)))

print("Filterliste generiert: ublock_filter.txt")
