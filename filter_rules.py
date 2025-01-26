# filter_regeln.py

# Diese Liste enthält alle Filterregeln. Jede Regel ist ein Array mit spezifischen Informationen.
filter_regeln = [
    # wordlists, include-domains, exclude-domains, upward(N)
   # [["Beispieltext1"], [], ["domain1.com", "domain2.com", [".cssattribute"]], 2],  # Exkludierte Domains und CSS-Attribute
   # [["Beispieltext2"], ["domain1.com", "domain2.com", [".cssattribute", ".cssattribute2"]], [], 1],  # Inkludierte Domains und CSS-Attribute
   # [["Noch ein Text", "Ein anderer Text"], [], [], 3],  # Global gültig, 3 divs nach oben
   # [["Testtext"], ["includedomain.com"], ["excludedomain.com", [".cssclass"]], ],  # Test leeres updward element; default 1
   # [["Testtext"], ["includedomain.com"], ["excludedomain.com", [".cssclass"]] ]  # Test leeres updward array; default 1

    # TEST
    [["test.co.uk/test"],[],[],],
    
    # Person
    [["trump"],[],[],],
    [["elon musk"],[],[],],
    [["putin"],[],[],],

    # Boycott
    [["AZDelivery"],[],[],],
    [["OTTO"],[],[],],

    # infatillity
    [["Worse"],[],[],],
    [["fuck"],[],[],],
    [["idioten"],[],[],],
    [["verheerend"],[],[],],
    [["Hecklers"],[],[],],
    [["wtf"],[],[],],

    # Media
    [["ard"],[],[],],
    [["zdf"],[],[],],
    [["bild"],[],[],],
    [["twitter"],[],[],],
    [["tagesschau"],[],[],],
    [["Fokus"],[],[],],
    [["Spiegel"],[],[],],
    [["computerbild"],[],[],],
    
    # Politics
    [["cdu"],[],[],],
    [["csu"],[],[],],
    [["die linke"],[],[],],
    [["die grünen"],[],[],],
    [["afd"],[],[],],
    [["fdp"],[],[],],
    [["spd"],[],[],],
    [["bundeswehr"],[],[],],
    [["panzer"],[],[],],

]
