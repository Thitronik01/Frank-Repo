"""Quelltexte der Fachbegriff-Artikel (wiki/concepts/). Vom LLM gepflegt.

Jeder Eintrag: slug -> (Titel, Kurzdefinition, Erläuterung (Markdown), [verwandte Slugs], [tags])
build.py erzeugt daraus die Seiten und ergänzt automatisch die Liste der Fahrzeuge, die den Begriff verwenden.
"""

KATEGORIEN = {
    "Batterie & Kapazität": ["traktionsbatterie", "lithium-ionen-akku", "kilowattstunde", "bruttokapazitaet",
                             "nettokapazitaet", "batteriepuffer", "software-lock", "zellformat",
                             "nmc-zellchemie", "lfp-zellchemie", "batteriemanagementsystem"],
    "Batteriezustand & Diagnose": ["state-of-charge", "state-of-health", "batteriealterung", "batteriecheck"],
    "Laden & Energie": ["ac-laden", "dc-schnellladen", "800-volt-architektur", "rekuperation", "wltp", "range-extender"],
    "Antrieb": ["bev", "elektromotor", "frontantrieb", "hinterradantrieb", "allradantrieb"],
    "Plattformen": ["plattform-meb", "plattform-ppe", "plattform-j1", "plattform-e-gmp", "plattform-stellantis",
                    "konversionsfahrzeug", "plattform-geschwister"],
    "Modelle & Bezeichnungen": ["typbezeichnungen", "karosserieformen", "modellpflege", "elektro-transporter"],
}

C = {}

C["traktionsbatterie"] = (
    "Traktionsbatterie", "Der Hochvolt-Energiespeicher, der den Elektromotor eines Elektroautos versorgt.",
    """Die Traktionsbatterie (auch Hochvolt- oder Antriebsbatterie) ist das teuerste Einzelbauteil eines [[bev|Elektroautos]]. Sie besteht aus vielen einzelnen Zellen, die zu Modulen und schließlich zu einem Batteriepack verschaltet werden. In heutigen Pkw arbeitet sie mit Systemspannungen von etwa 350–400 Volt, bei neueren Modellen auch mit rund 800 Volt (siehe [[800-volt-architektur]]).

Zu unterscheiden ist sie von der 12-Volt-Bordnetzbatterie, die Steuergeräte, Licht und Komfortfunktionen versorgt. Wenn in diesem Wiki von Kapazität die Rede ist, ist immer die Traktionsbatterie gemeint.

Wichtige Kenngrößen sind die [[bruttokapazitaet|Brutto-]] und die [[nettokapazitaet|Nettokapazität]] in [[kilowattstunde|kWh]], die [[nmc-zellchemie|Zellchemie]] und der Gesundheitszustand ([[state-of-health]]). Überwacht wird sie vom [[batteriemanagementsystem]].""",
    ["lithium-ionen-akku", "batteriemanagementsystem", "bruttokapazitaet", "state-of-health"], ["batterie"])

C["lithium-ionen-akku"] = (
    "Lithium-Ionen-Akku", "Wiederaufladbare Batterietechnik, bei der Lithium-Ionen zwischen Anode und Kathode wandern – Standard in allen Fahrzeugen dieses Wikis.",
    """Alle Fahrzeuge im Bestand nutzen Lithium-Ionen-Zellen. Beim Laden wandern Lithium-Ionen von der Kathode durch den Elektrolyten in die Anode (meist Graphit), beim Entladen zurück. Die Kathodenchemie bestimmt Energiedichte, Kosten, Lebensdauer und Sicherheit maßgeblich – die zwei wichtigsten Familien sind [[nmc-zellchemie|NMC]] und [[lfp-zellchemie|LFP]].

Lithium-Ionen-Zellen altern sowohl mit der Zeit als auch mit der Nutzung (siehe [[batteriealterung]]). Sie mögen weder Tiefentladung noch dauerhaft 100 % Ladung bei hoher Temperatur – deshalb halten Hersteller einen [[batteriepuffer]] vor.""",
    ["nmc-zellchemie", "lfp-zellchemie", "zellformat", "batteriealterung"], ["batterie", "chemie"])

C["kilowattstunde"] = (
    "Kilowattstunde (kWh)", "Einheit der Energiemenge: 1 kWh ist die Energie, die bei einer Leistung von 1 kW in einer Stunde umgesetzt wird.",
    """Batteriekapazitäten von Elektroautos werden in kWh angegeben. Genau genommen ist das eine Energie-, keine Ladungsmenge (die wäre in Amperestunden, Ah). Die Energie ergibt sich aus Ladungsmenge × Nennspannung: Eine Batterie mit 200 Ah bei 400 V Nennspannung speichert rund 80 kWh.

**Nicht verwechseln mit kW:** kW (Kilowatt) ist eine *Leistung* – etwa die Motorleistung oder die Ladeleistung ([[dc-schnellladen]]). kWh ist die gespeicherte *Energiemenge*.

Faustregel für die Praxis: Ein Kompaktwagen verbraucht grob 15–20 kWh pro 100 km. Aus 60 kWh [[nettokapazitaet]] ergeben sich damit etwa 300–400 km Reichweite (stark abhängig von Tempo, Temperatur und Fahrzeug).""",
    ["bruttokapazitaet", "nettokapazitaet", "wltp"], ["einheit"])

C["bruttokapazitaet"] = (
    "Bruttokapazität", "Die gesamte, physikalisch in der Batterie verbaute Energiemenge – inklusive der Reserven, die der Fahrer nie nutzen kann.",
    """Die Bruttokapazität (auch *installierte* oder *Nennkapazität*) ist die Summe der Energie aller verbauten Zellen. Hersteller nennen in Prospekten mal diesen, mal den Nettowert – was Vergleiche erschwert. Die Rohquelle [[tn-batterycheck-alle-daten]] führt deshalb beide Werte getrennt.

Nutzbar ist davon nur die [[nettokapazitaet]]. Die Differenz ist der [[batteriepuffer]].

**Beispiele aus dem Bestand** ([[tn-batterycheck-alle-daten]]):

| Fahrzeug | Brutto | Netto |
|---|---|---|
| [[audi-e-tron|Audi e-tron 55]] | 95 kWh | 83,6–89,0 kWh |
| [[tesla-model-s|Tesla Model S 60]] | 75 kWh | 62,0 kWh |
| [[ford-f-150-lightning|Ford F-150 Lightning ER]] | 143,4 kWh | 131,0 kWh |

Beim Audi e-tron 55 ist bei gleicher Bruttokapazität die Nettokapazität per Software-Update angehoben worden – deshalb stehen drei Nettowerte im Bestand (siehe [[software-lock]] und [[modellpflege]]).""",
    ["nettokapazitaet", "batteriepuffer", "kilowattstunde", "software-lock"], ["batterie", "kennzahl"])

C["nettokapazitaet"] = (
    "Nettokapazität", "Der Teil der Batteriekapazität, den der Fahrer tatsächlich nutzen kann – Grundlage für Reichweite und Batterietests.",
    """Die Nettokapazität (auch *nutzbare Kapazität*, *usable capacity*) ist das Energiefenster zwischen 0 % und 100 % der Ladeanzeige ([[state-of-charge]]). Das [[batteriemanagementsystem]] sperrt oberhalb und unterhalb dieses Fensters einen Teil der [[bruttokapazitaet]] als [[batteriepuffer]].

Für die Bewertung einer gebrauchten Batterie ist die Nettokapazität der relevante Bezugswert: Ein [[batteriecheck]] misst, wie viel der ursprünglichen Nettokapazität heute noch verfügbar ist, und drückt das als [[state-of-health]] aus.

In der Rohquelle [[tn-batterycheck-alle-daten]] ist die Nettokapazität je Variante angegeben. Einzelne Werte sind als „ca." gekennzeichnet (z. B. [[mercedes-esprinter|Mercedes eSprinter LFP]]), und in einem Fall ist netto größer als brutto ([[cupra-born]]) – das ist physikalisch unmöglich und deutet auf einen Datenfehler hin.""",
    ["bruttokapazitaet", "batteriepuffer", "state-of-health"], ["batterie", "kennzahl"])

C["batteriepuffer"] = (
    "Batteriepuffer", "Differenz zwischen Brutto- und Nettokapazität – eine Reserve, die die Batterie schont und Alterung ausgleicht.",
    """Hersteller geben nie die ganze [[bruttokapazitaet]] frei. Ein Teil wird oben (gegen Überladung und Stress bei Voll-Ladung) und unten (gegen Tiefentladung) reserviert. Das schont die Zellen, verlangsamt die [[batteriealterung]] und stellt sicher, dass auch bei „0 %" noch eine Notreserve bleibt.

**Berechnung:** Puffer = Brutto − Netto; relativ: (Brutto − Netto) / Brutto.

Die Puffergrößen im Bestand reichen von unter 1 % (z. B. [[citroen-e-c3|Citroën ë-C3]] 44 → 43,8 kWh, [[lfp-zellchemie|LFP-Zellen]]) bis rund 18 % ([[tesla-model-s|Model S 60]] mit 75 kWh brutto als [[software-lock]]; [[vw-id-3|VW ID.3 Pure]] 55 → 45 kWh laut Quelle, Bruttowert fraglich – siehe [[datenqualitaet]]). Eine vollständige Auswertung steht unter [[puffer-analyse]].

Manche Hersteller nutzen den oberen Puffer, um Alterung zu kaschieren: Das BMS gibt mit der Zeit einen Teil der Reserve frei, sodass die angezeigte Reichweite länger stabil bleibt. Das erschwert die Messung des echten [[state-of-health]].""",
    ["bruttokapazitaet", "nettokapazitaet", "software-lock", "batteriealterung"], ["batterie", "kennzahl"])

C["software-lock"] = (
    "Software-Lock (softwarebegrenzte Kapazität)", "Eine physikalisch größere Batterie wird per Software auf eine kleinere nutzbare Kapazität begrenzt.",
    """Manche Hersteller bauen aus Kostengründen (Stückzahl, einheitliche Fertigung) eine größere Batterie ein, als die Ausstattungsvariante nutzen darf. Die Differenz ist per Software gesperrt und lässt sich teils gegen Aufpreis freischalten.

**Bekanntestes Beispiel im Bestand:** [[tesla-model-s|Tesla Model S 60/60D]] und [[tesla-model-x|Model X 60D]] – brutto 75 kWh, netto nur 62 kWh ([[tn-batterycheck-alle-daten]]). Gleiches gilt für den Model S 70 in einer Ausführung mit 75-kWh-Pack.

Auch nachträgliche *Erweiterungen* des Nutzfensters per Update kommen vor: Beim [[audi-e-tron|Audi e-tron 55]] stehen bei 95 kWh brutto drei verschiedene Nettowerte (83,6 / 86,5 / 89,0 kWh) im Bestand.

Für einen [[batteriecheck]] ist wichtig zu wissen, welche Freigabe aktiv ist – sonst wird der [[state-of-health]] falsch berechnet.""",
    ["batteriepuffer", "bruttokapazitaet", "nettokapazitaet"], ["batterie", "software"])

C["zellformat"] = (
    "Zellformat", "Bauform der einzelnen Batteriezellen: zylindrische Rundzelle, prismatische Zelle oder Pouch-Zelle.",
    """- **Rundzellen** (z. B. 18650, 2170, 4680) – in großen Stückzahlen günstig, robust, gute Kühlung. Typisch für [[tesla-model-s|Tesla]]; zunehmend auch bei anderen Herstellern (BMW „Neue Klasse").
- **Prismatische Zellen** – rechteckige Hartschalen-Gehäuse, gute Raumausnutzung; verbreitet z. B. bei BMW, VW-Konzern, vielen [[lfp-zellchemie|LFP]]-Batterien.
- **Pouch-Zellen** – flexible Folienbeutel, leicht und platzsparend, brauchen aber Stützstruktur; z. B. bei Hyundai/Kia ([[plattform-e-gmp|E-GMP]]), Renault, Mercedes.

Bei **Cell-to-Pack** (CTP) entfallen die Module, die Zellen sitzen direkt im Pack – mehr Energie auf gleichem Raum.""",
    ["lithium-ionen-akku", "traktionsbatterie"], ["batterie", "technik"])

C["nmc-zellchemie"] = (
    "NMC-Zellchemie", "Lithium-Ionen-Zellen mit Kathode aus Nickel, Mangan und Kobalt – hohe Energiedichte, Standard in den meisten Fahrzeugen des Bestands.",
    """NMC (Lithium-Nickel-Mangan-Kobalt-Oxid) ist die meistverbreitete Kathodenchemie in europäischen und koreanischen Elektroautos. Die Zahlen hinter „NMC" (z. B. 622, 811) nennen das Verhältnis Nickel:Mangan:Kobalt; mehr Nickel bedeutet mehr Energiedichte und weniger teures Kobalt, aber anspruchsvolleres Thermomanagement. Eng verwandt ist NCA (Nickel-Kobalt-Aluminium), das Tesla in vielen Model S/X/3 nutzt.

**Stärken:** hohe Energiedichte (Reichweite), gute Leistung bei Kälte.
**Schwächen:** teurer als [[lfp-zellchemie|LFP]], empfindlicher gegen dauerhaft 100 % Ladung – Empfehlung im Alltag meist 80 %.

NMC-Batterien haben meist einen spürbaren [[batteriepuffer]], und der Ladezustand lässt sich über die Spannungskurve relativ gut bestimmen ([[state-of-charge]]).""",
    ["lfp-zellchemie", "lithium-ionen-akku", "batteriealterung"], ["batterie", "chemie"])

C["lfp-zellchemie"] = (
    "LFP-Zellchemie", "Lithium-Eisenphosphat-Zellen – kobaltfrei, günstig, sehr langlebig, aber mit geringerer Energiedichte.",
    """LFP (Lithium-Eisenphosphat, LiFePO₄) verzichtet auf Nickel und Kobalt. Die Zellen sind günstiger, thermisch stabiler und vertragen deutlich mehr Ladezyklen als [[nmc-zellchemie|NMC]]. Hersteller empfehlen oft, regelmäßig auf 100 % zu laden – das braucht das [[batteriemanagementsystem]] zur Kalibrierung, weil die Spannungskurve von LFP sehr flach ist und der [[state-of-charge]] sonst schwer zu schätzen ist.

**Im Bestand** ([[tn-batterycheck-alle-daten]]): ausdrücklich als LFP bezeichnet ist der [[mercedes-esprinter|Mercedes eSprinter LFP]]. Auch bei [[tesla-model-3|Tesla Model 3]] / [[tesla-model-y|Model Y]] RWD mit 60 kWh brutto (in Europa verbreitet), dem [[citroen-e-c3|Citroën ë-C3]] und [[citroen-e-c3-aircross|ë-C3 Aircross]] kommen LFP-Zellen zum Einsatz – der auffallend kleine [[batteriepuffer]] dieser Modelle ist typisch.

**Nachteile:** geringere Energiedichte (mehr Gewicht pro kWh), schwächere Ladeleistung bei Kälte.""",
    ["nmc-zellchemie", "lithium-ionen-akku", "state-of-charge"], ["batterie", "chemie"])

C["batteriemanagementsystem"] = (
    "Batteriemanagementsystem (BMS)", "Elektronik und Software, die jede Zelle der Traktionsbatterie überwacht, schützt und den Ladezustand berechnet.",
    """Das BMS misst laufend Spannung, Strom und Temperatur der Zellen bzw. Zellblöcke. Daraus berechnet es den Ladezustand ([[state-of-charge]]) und schätzt den Gesundheitszustand ([[state-of-health]]). Es verhindert Über- und Tiefentladung, begrenzt die Lade- und Entladeleistung bei Kälte oder Hitze, gleicht Spannungsunterschiede zwischen Zellen aus (*Balancing*) und steuert das Thermomanagement.

Das BMS legt auch fest, wie viel der [[bruttokapazitaet]] nutzbar ist ([[batteriepuffer]], [[software-lock]]).

Ein [[batteriecheck]] liest in der Regel Daten aus dem BMS über die Diagnoseschnittstelle (OBD) aus oder wertet einen kontrollierten Lade- bzw. Entladevorgang aus.""",
    ["state-of-charge", "state-of-health", "batteriecheck"], ["batterie", "elektronik"])

C["state-of-charge"] = (
    "State of Charge (SoC)", "Der aktuelle Ladezustand der Batterie in Prozent der Nettokapazität – die „Tankanzeige“.",
    """Der SoC gibt an, wie voll die Batterie gerade ist. 100 % bedeutet: [[nettokapazitaet]] vollständig verfügbar; 0 %: nutzbares Fenster erschöpft (der untere [[batteriepuffer]] ist dann noch vorhanden).

Der SoC wird vom [[batteriemanagementsystem]] geschätzt – aus Spannung, gezähltem Strom (Coulomb Counting) und Modellen. Bei [[lfp-zellchemie|LFP]] ist die Schätzung schwieriger, weil die Spannung über weite Bereiche kaum schwankt.

**Abgrenzung:** SoC = *wie voll* ist die Batterie gerade. [[state-of-health|SoH]] = *wie groß* ist sie noch im Vergleich zum Neuzustand.""",
    ["state-of-health", "nettokapazitaet", "batteriemanagementsystem"], ["batterie", "diagnose"])

C["state-of-health"] = (
    "State of Health (SoH)", "Gesundheitszustand der Batterie: verbleibende Kapazität im Verhältnis zur Neu-Kapazität, in Prozent.",
    """Der SoH ist die zentrale Kennzahl beim Kauf oder Verkauf eines gebrauchten Elektroautos. Ein SoH von 90 % heißt: Die Batterie speichert noch 90 % der Energie, die sie neu gespeichert hat.

**Berechnung:** SoH = gemessene nutzbare Kapazität / [[nettokapazitaet|Netto-Neukapazität]] × 100 %. Genau dafür braucht es verlässliche Referenzwerte je Variante – wie sie die Rohquelle [[tn-batterycheck-alle-daten]] liefert. Wird fälschlich die [[bruttokapazitaet]] als Referenz genommen, erscheint der SoH zu niedrig.

**Orientierung:** Viele Hersteller garantieren 70 % SoH nach 8 Jahren bzw. 160.000 km. Typische Alterung liegt in den ersten Jahren bei wenigen Prozent und flacht dann ab ([[batteriealterung]]).

Fallstricke: nachträgliche Freigabe von Pufferkapazität ([[software-lock]], [[batteriepuffer]]), Temperatur bei der Messung, uneinheitliche BMS-Anzeigen der Hersteller.""",
    ["state-of-charge", "batteriecheck", "batteriealterung", "nettokapazitaet"], ["batterie", "diagnose"])

C["batteriealterung"] = (
    "Batteriealterung (Degradation)", "Allmählicher Kapazitäts- und Leistungsverlust einer Lithium-Ionen-Batterie über Zeit und Nutzung.",
    """Man unterscheidet:

- **Kalendarische Alterung** – findet auch im Stand statt; beschleunigt durch hohe Temperatur und hohen [[state-of-charge|Ladezustand]] über lange Zeit.
- **Zyklische Alterung** – durch Laden und Entladen; beschleunigt durch große Entladetiefen, hohe Ströme (häufiges [[dc-schnellladen]]) und Laden bei Kälte.

Typisch ist ein etwas stärkerer Verlust in den ersten ein bis zwei Jahren, danach ein flacherer Verlauf. [[lfp-zellchemie|LFP]] altert zyklisch deutlich langsamer als [[nmc-zellchemie|NMC]].

Messbar wird Alterung als sinkender [[state-of-health]]. Der [[batteriepuffer]] und das [[batteriemanagementsystem]] mildern sie ab.""",
    ["state-of-health", "batteriepuffer", "dc-schnellladen"], ["batterie", "diagnose"])

C["batteriecheck"] = (
    "Batteriecheck (Batteriezertifikat)", "Standardisierte Prüfung des Gesundheitszustands der Traktionsbatterie, meist für den Gebrauchtwagenhandel.",
    """Ein Batteriecheck ermittelt den [[state-of-health]] der [[traktionsbatterie]] und dokumentiert ihn in einem Zertifikat. Verbreitete Verfahren:

1. **BMS-Auslesung** über die OBD-Schnittstelle – schnell, aber abhängig davon, was der Hersteller preisgibt.
2. **Messung bei Lade-/Entladevorgang** – die tatsächlich geladene oder entnommene Energie wird mit der Referenz-[[nettokapazitaet]] verglichen.
3. **Kurztest mit Lastprofil** – Auswertung des Spannungsverhaltens unter definierter Last, Hochrechnung per Modell.

Voraussetzung ist in jedem Fall eine saubere Referenztabelle mit Brutto- und Nettokapazität je Modellvariante. Genau das ist die Rohquelle dieses Wikis: [[tn-batterycheck-alle-daten]] (469 Varianten, 19 Marken).""",
    ["state-of-health", "nettokapazitaet", "batteriemanagementsystem"], ["diagnose", "gebrauchtwagen"])

C["ac-laden"] = (
    "AC-Laden", "Laden mit Wechselstrom an Haushaltssteckdose oder Wallbox; der Bordlader im Auto wandelt in Gleichstrom um.",
    """Beim AC-Laden liefert die Ladestation Wechselstrom, und der *On-Board-Charger* (OBC) im Fahrzeug richtet ihn für die Batterie gleich. Die Ladeleistung wird deshalb durch den OBC begrenzt – typisch 7,4 kW (einphasig), 11 kW oder 22 kW (dreiphasig). In Europa ist der Stecker **Typ 2** Standard.

Eine 60-kWh-Batterie ([[nettokapazitaet]]) braucht an 11 kW also rund 6 Stunden von leer bis voll. AC-Laden ist batterieschonend und ideal über Nacht; für die Langstrecke gibt es [[dc-schnellladen]].""",
    ["dc-schnellladen", "kilowattstunde"], ["laden"])

C["dc-schnellladen"] = (
    "DC-Schnellladen", "Laden mit Gleichstrom direkt in die Batterie, ohne Umweg über den Bordlader – mit 50 bis über 300 kW.",
    """Beim DC-Laden sitzt der Gleichrichter in der Ladesäule, und die Energie fließt direkt in die [[traktionsbatterie]]. In Europa ist der Stecker **CCS2** Standard; ältere japanische/französische Modelle (z. B. [[citroen-c-zero]], [[peugeot-ion]]) nutzen CHAdeMO.

Die Ladeleistung folgt einer **Ladekurve**: hoch bei niedrigem [[state-of-charge|SoC]], abfallend oberhalb von etwa 50–80 %. Fahrzeuge mit [[800-volt-architektur]] erreichen höhere Leistungen bei geringeren Strömen.

Häufiges Schnellladen, besonders bei Hitze oder Kälte, kann die [[batteriealterung]] beschleunigen – moderne Thermomanagement-Systeme mildern das stark ab.""",
    ["ac-laden", "800-volt-architektur", "batteriealterung"], ["laden"])

C["800-volt-architektur"] = (
    "800-Volt-Architektur", "Hochvoltsystem mit etwa doppelter Spannung gegenüber üblichen 400 Volt – ermöglicht schnelleres Laden und leichtere Kabel.",
    """Da Leistung = Spannung × Strom, lässt sich bei doppelter Spannung dieselbe Leistung mit halbem Strom übertragen. Das reduziert Wärmeverluste, erlaubt dünnere Kabel und vor allem höhere [[dc-schnellladen|DC-Ladeleistungen]] (teils über 250 kW).

**Im Bestand:** [[porsche-taycan]] und [[audi-e-tron-gt]] ([[plattform-j1]]), [[porsche-macan-electric]] und [[audi-q6-e-tron]] ([[plattform-ppe]]), Hyundai [[hyundai-ioniq-5|IONIQ 5]]/[[hyundai-ioniq-6|6]]/[[hyundai-ioniq-9|9]] und Kia [[kia-ev6|EV6]]/[[kia-ev9|EV9]] ([[plattform-e-gmp]]).

An 400-Volt-Säulen brauchen 800-Volt-Fahrzeuge einen Wandler (Booster) oder schalten Batteriehälften um.""",
    ["dc-schnellladen", "plattform-e-gmp", "plattform-ppe", "plattform-j1"], ["laden", "technik"])

C["rekuperation"] = (
    "Rekuperation", "Rückgewinnung von Bewegungsenergie beim Bremsen: der Elektromotor arbeitet als Generator und lädt die Batterie.",
    """Beim Verzögern wird der [[elektromotor]] zum Generator. Die Energie fließt zurück in die [[traktionsbatterie]], statt in den Bremsscheiben als Wärme verloren zu gehen. Das spart im Stadtverkehr spürbar Energie und schont die mechanischen Bremsen.

Viele Fahrzeuge bieten einstellbare Stufen bis zum *One-Pedal-Driving*. Die Rekuperationsleistung ist bei voller Batterie (hoher [[state-of-charge|SoC]]) und bei Kälte eingeschränkt – dann kann die Batterie keine hohen Ladeströme aufnehmen.""",
    ["elektromotor", "state-of-charge"], ["antrieb", "energie"])

C["wltp"] = (
    "WLTP", "Worldwide Harmonized Light Vehicles Test Procedure – seit 2017/2018 der EU-Normzyklus für Verbrauch und Reichweite.",
    """Der WLTP ersetzte den unrealistischen NEFZ. Für Elektroautos liefert er Stromverbrauch (kWh/100 km) und Reichweite. Auch WLTP-Werte liegen meist über der Alltagsreichweite, besonders auf der Autobahn und im Winter.

Die Reichweite hängt direkt an der [[nettokapazitaet]]. Eine gealterte Batterie ([[state-of-health]] 85 %) liefert entsprechend rund 15 % weniger Reichweite als neu.""",
    ["nettokapazitaet", "kilowattstunde"], ["norm"])

C["range-extender"] = (
    "Range Extender (REx)", "Kleiner Verbrennungsmotor als Generator, der bei leerer Batterie Strom erzeugt und so die Reichweite verlängert.",
    """Beim Range Extender treibt der Verbrenner nicht die Räder an, sondern nur einen Generator. Das Fahrzeug fährt immer elektrisch – anders als ein Plug-in-Hybrid.

**Im Bestand:** [[bmw-i3|BMW i3 (Range Extender)]] und i3s REx mit einem 647-cm³-Zweizylinder und kleinem Benzintank ([[tn-batterycheck-alle-daten]]). Die Batterie ist identisch zur rein elektrischen Version – deshalb stehen im Bestand dieselben Brutto-/Nettowerte.

Formal ist ein REx-Fahrzeug kein reines [[bev]], sondern ein serieller Hybrid bzw. REEV.""",
    ["bev", "traktionsbatterie"], ["antrieb"])

C["bev"] = (
    "BEV (batterieelektrisches Fahrzeug)", "Battery Electric Vehicle – Fahrzeug, das ausschließlich mit Strom aus einer Traktionsbatterie fährt.",
    """Ein BEV hat keinen Verbrennungsmotor. Es wird über [[ac-laden|AC]] oder [[dc-schnellladen|DC]] geladen und fährt mit einem oder mehreren [[elektromotor|Elektromotoren]].

**Abgrenzung:**
- **PHEV** (Plug-in-Hybrid) – Verbrenner + kleine Batterie, extern ladbar.
- **HEV** (Vollhybrid) – nicht extern ladbar.
- **REEV** – BEV mit [[range-extender]] als Generator.

Fast alle Fahrzeuge in diesem Wiki sind BEV; Ausnahme ist der [[bmw-i3]] mit Range Extender.""",
    ["range-extender", "elektromotor", "traktionsbatterie"], ["antrieb", "grundlagen"])

C["elektromotor"] = (
    "Elektromotor (PSM / ASM / FSM)", "Antriebsmaschine eines Elektroautos; verbreitet sind permanenterregte Synchron-, Asynchron- und fremderregte Synchronmotoren.",
    """- **PSM** (permanenterregte Synchronmaschine) – hoher Wirkungsgrad, kompakt; braucht Magnete mit Seltenen Erden. Am weitesten verbreitet.
- **ASM** (Asynchronmaschine) – robust, günstig, ohne Magnete; verursacht im Leerlauf kaum Verluste. Deshalb oft als *zweiter* Motor an der Achse, die nur bei Bedarf zugeschaltet wird (z. B. [[vw-id-4|ID.4 GTX]], [[audi-e-tron|Audi e-tron]], frühe [[tesla-model-s|Model S]]).
- **FSM** (fremderregte Synchronmaschine) – ohne Seltene Erden, gute Effizienz; Renault ([[renault-zoe]], [[renault-scenic-e-tech]]) und BMW (ab Gen5, z. B. [[bmw-ix]], [[bmw-i4]]).

Die Anzahl der Motoren bestimmt die Antriebsart: [[frontantrieb]], [[hinterradantrieb]] oder [[allradantrieb]]. Beim Bremsen arbeitet der Motor als Generator ([[rekuperation]]).""",
    ["allradantrieb", "rekuperation"], ["antrieb", "technik"])

C["frontantrieb"] = (
    "Frontantrieb (FWD)", "Der Elektromotor treibt die Vorderräder an – typisch für Kleinwagen und Konversionsfahrzeuge.",
    """Frontantrieb ist platzsparend und günstig. Er ist die Regel bei Fahrzeugen, die von Verbrenner-Plattformen abgeleitet sind ([[konversionsfahrzeug]]), etwa [[peugeot-e-208]], [[renault-zoe]], [[hyundai-kona-electric]], [[mercedes-eqa|Mercedes EQA 250]] und [[vw-e-golf]].

Nachteil: Bei starker Beschleunigung verlagert sich das Gewicht nach hinten, die Vorderräder verlieren Traktion. Viele reine Elektroplattformen setzen daher auf [[hinterradantrieb]].""",
    ["hinterradantrieb", "allradantrieb", "konversionsfahrzeug"], ["antrieb"])

C["hinterradantrieb"] = (
    "Hinterradantrieb (RWD)", "Der Elektromotor treibt die Hinterräder an – Standard auf vielen reinen Elektroplattformen.",
    """Rear-Wheel Drive (RWD, bei Hyundai/Kia „2WD") ist bei [[plattform-meb|MEB]], [[plattform-e-gmp|E-GMP]], Tesla und BMW verbreitet. Vorteile: bessere Traktion beim Beschleunigen, größerer Lenkeinschlag (kleiner Wendekreis), weil vorne keine Antriebswellen stören.

**Bezeichnungen im Bestand:** „RWD" (Tesla, Ford, Hyundai IONIQ 9), „2WD" (Hyundai/Kia), „eDrive" (BMW), „Single Motor" (Volvo – Achtung: bei frühen Volvo Single Motor ist das *Front*antrieb, ab Modelljahr 2024 Heckantrieb). Mehr in [[typbezeichnungen]].""",
    ["frontantrieb", "allradantrieb", "typbezeichnungen"], ["antrieb"])

C["allradantrieb"] = (
    "Allradantrieb (AWD)", "Beide Achsen werden angetrieben, bei Elektroautos meist durch je einen eigenen Motor pro Achse.",
    """Elektrischer Allradantrieb braucht keine Kardanwelle: Ein zweiter [[elektromotor]] sitzt direkt an der anderen Achse. Das bringt mehr Traktion und Leistung, kostet aber meist etwas Reichweite.

**Markennamen im Bestand** ([[tn-batterycheck-alle-daten]]):

| Bezeichnung | Hersteller |
|---|---|
| quattro | [[audi]] |
| xDrive | [[bmw]] |
| 4MATIC | [[mercedes]] |
| 4Motion / 4M | [[volkswagen]], [[cupra]] |
| x (z. B. „85x") | [[skoda]] |
| D / Dual Motor, AWD | [[tesla]] |
| Twin Motor | [[volvo]] |
| AWD | [[ford]], [[hyundai]], [[kia]] |
| 4 / 4S / Turbo | [[porsche]] (alle Taycan-Varianten außer der Basis) |

Siehe auch [[typbezeichnungen]].""",
    ["hinterradantrieb", "frontantrieb", "elektromotor", "typbezeichnungen"], ["antrieb"])

C["plattform-meb"] = (
    "MEB (Modularer E-Antriebs-Baukasten)", "Volkswagens erste reine Elektroauto-Plattform, Basis für ID.-Modelle, Enyaq, Elroq, Born, Tavascan und Q4 e-tron.",
    """Der MEB wurde ab 2019 in Serie gebracht. Die [[traktionsbatterie]] liegt flach im Unterboden, der Hauptmotor sitzt hinten ([[hinterradantrieb]]); Allradversionen erhalten einen Asynchronmotor vorne ([[allradantrieb]]). Er arbeitet mit rund 400 Volt.

**Batteriestufen im Bestand** ([[tn-batterycheck-alle-daten]]) – über alle Marken hinweg identisch:

| Brutto | Netto | Beispiele |
|---|---|---|
| 55 kWh | 52 kWh (ID.3 Pure: 45) | [[vw-id-4|ID.4 Pure]], [[skoda-enyaq|Enyaq 50]], [[audi-q4-e-tron|Q4 35]] (51,5) |
| 62/63 kWh | 58/59 kWh | [[vw-id-3|ID.3 Pro]], [[cupra-born]], [[skoda-elroq|Elroq 60]] |
| 82 kWh | 77 kWh (Audi: 76,6) | ID.4/ID.5/ID.7 Pro, [[skoda-enyaq|Enyaq 80/85]], [[cupra-tavascan]] |
| 84 kWh | 79 kWh | [[vw-id-buzz|ID. Buzz]] ab 2024 |
| 91 kWh | 86 kWh | [[vw-id-7|ID.7 Pro S]], ID. Buzz LWB |

**MEB-Fahrzeuge im Bestand:** [[vw-id-3]], [[vw-id-4]], [[vw-id-5]], [[vw-id-7]], [[vw-id-buzz]], [[skoda-enyaq]], [[skoda-elroq]], [[cupra-born]], [[cupra-tavascan]], [[audi-q4-e-tron]]. Siehe auch [[plattform-geschwister]].""",
    ["plattform-ppe", "plattform-geschwister", "hinterradantrieb"], ["plattform", "vw-konzern"])

C["plattform-ppe"] = (
    "PPE (Premium Platform Electric)", "Gemeinsame Elektroplattform von Audi und Porsche für Oberklasse-Fahrzeuge mit 800-Volt-Technik.",
    """PPE wurde von Audi und Porsche gemeinsam entwickelt und debütierte 2024 im [[porsche-macan-electric|Porsche Macan]] und [[audi-q6-e-tron|Audi Q6 e-tron]]. Kennzeichen: [[800-volt-architektur]], prismatische Zellen, 100 kWh brutto / rund 95 kWh netto in der großen Ausbaustufe (Audi Q6: 94,9 kWh netto; Macan: 95,0 kWh – [[tn-batterycheck-alle-daten]]).

Weitere PPE-Modelle (A6 e-tron, Cayenne Electric) sind noch nicht im Bestand.""",
    ["800-volt-architektur", "plattform-j1", "plattform-meb"], ["plattform", "vw-konzern"])

C["plattform-j1"] = (
    "J1-Plattform", "Porsches Elektro-Sportwagenplattform für Taycan und Audi e-tron GT.",
    """Die J1-Plattform wurde für den [[porsche-taycan]] entwickelt (Marktstart 2019) und auch für den [[audi-e-tron-gt]] genutzt. Sie war die erste Serienplattform mit [[800-volt-architektur]] in Europa.

**Batteriestufen im Bestand** ([[tn-batterycheck-alle-daten]]):

| Generation | Brutto | Netto | Name bei Porsche |
|---|---|---|---|
| J1 (2019–2024) | 79,2 kWh | 71,0 kWh | Performance-Batterie |
| J1 (2019–2024) | 93,4 kWh | 83,7 kWh | Performance-Batterie Plus |
| J1.2 (ab 2024) | 89 kWh | 82,3 kWh | Performance-Batterie |
| J1.2 (ab 2024) | 105 kWh | 97,0 kWh | Performance-Batterie Plus |

Beim Audi e-tron GT und RS e-tron GT gelten die gleichen Werte (93,4/83,7 bzw. 105/97).""",
    ["800-volt-architektur", "plattform-ppe", "modellpflege"], ["plattform", "vw-konzern"])

C["plattform-e-gmp"] = (
    "E-GMP (Electric Global Modular Platform)", "Elektroplattform von Hyundai und Kia, Basis für IONIQ 5/6/9 und EV6/EV9.",
    """Die E-GMP kam 2021 mit dem [[hyundai-ioniq-5|IONIQ 5]] und dem [[kia-ev6|EV6]] auf den Markt. Sie arbeitet mit [[800-volt-architektur]] und erlaubt dadurch sehr kurze [[dc-schnellladen|DC-Ladezeiten]]. Grundkonfiguration ist [[hinterradantrieb]] („2WD"/„RWD"), optional [[allradantrieb]].

**Batteriestufen im Bestand** ([[tn-batterycheck-alle-daten]]):

| Brutto | Netto | Stand |
|---|---|---|
| 58 kWh | 54 kWh | Standard Range, 2021–2023 |
| 63 kWh | 60 kWh | Standard Range, ab Modellpflege |
| 72,6 kWh | 70 kWh | Long Range, frühe Version |
| 77,4 kWh | 74 kWh | Long Range, ab 2022 |
| 84 kWh | 80 kWh | Long Range, ab Modellpflege 2024 |
| 99,8 / 110,3 kWh | 96 / 106 kWh | Kia EV9 / Hyundai IONIQ 9 |

**E-GMP-Fahrzeuge im Bestand:** [[hyundai-ioniq-5]], [[hyundai-ioniq-6]], [[hyundai-ioniq-9]], [[kia-ev6]], [[kia-ev9]]. Die neueren [[kia-ev3]] und [[kia-ev4]] nutzen eine 400-Volt-Variante.""",
    ["800-volt-architektur", "plattform-geschwister", "modellpflege"], ["plattform", "hyundai-kia"])

C["plattform-stellantis"] = (
    "Stellantis-Plattformen (e-CMP, EMP2, STLA)", "Die Elektro-Baukästen des Stellantis-Konzerns (Peugeot, Citroën, Opel u. a.).",
    """Stellantis setzt auf Multi-Energy-Plattformen, auf denen Verbrenner und Elektroautos gemeinsam gebaut werden:

- **e-CMP** (Kleinwagen/kompakte SUV) – z. B. [[peugeot-e-208]], [[peugeot-e-2008]], [[citroen-e-c4]], [[citroen-e-c4-x]]. Batteriestufen im Bestand: 50 kWh brutto / 46,3 kWh netto, später 51 bzw. 54 kWh / 48,1 bzw. 50,8 kWh netto.
- **EMP2** (Kompakt- und Nutzfahrzeuge) – [[peugeot-e-308]], [[peugeot-e-408]], sowie die Transporter [[citroen-e-jumpy]], [[citroen-e-spacetourer]], [[peugeot-e-expert]], [[peugeot-e-traveller]] (50 bzw. 75 kWh) und die Hochdachkombis [[citroen-e-berlingo]], [[peugeot-e-rifter]], [[peugeot-e-partner]].
- **STLA Medium** – [[peugeot-e-3008]] (77 / 101 kWh brutto).
- **Smart Car Platform** – günstige Kleinwagen mit [[lfp-zellchemie|LFP]]: [[citroen-e-c3]], [[citroen-e-c3-aircross]].

Viele Fahrzeuge verschiedener Marken teilen identische Batterien – siehe [[plattform-geschwister]].""",
    ["plattform-geschwister", "konversionsfahrzeug", "elektro-transporter"], ["plattform", "stellantis"])

C["konversionsfahrzeug"] = (
    "Konversionsfahrzeug", "Elektroauto, das von einem Modell mit Verbrennungsmotor abgeleitet ist, statt auf einer reinen Elektroplattform zu basieren.",
    """Bei Konversionsfahrzeugen („Conversion Design") wird die [[traktionsbatterie]] in eine vorhandene Karosserie integriert – unter Sitzen, im Tunnel oder im Unterboden. Das spart Entwicklungskosten, führt aber oft zu weniger Platz, kleineren Batterien und [[frontantrieb]].

**Beispiele im Bestand:** [[vw-e-golf]], [[vw-e-up]], [[hyundai-ioniq-electric]], [[hyundai-kona-electric]], [[kia-niro-ev]], [[mercedes-eqa]], [[mercedes-eqb]], [[mercedes-eqc]], [[volvo-ex40|Volvo XC40 Recharge]], [[bmw-ix3]], [[bmw-i4]], [[mini-cooper-electric|Mini Cooper SE (bis 2023)]], sowie die Transporter [[mercedes-evito]] und [[renault-master-electric]].

Gegenstück sind reine Elektroplattformen wie [[plattform-meb|MEB]], [[plattform-e-gmp|E-GMP]], [[plattform-ppe|PPE]] oder [[plattform-j1|J1]]. Mischformen sind Multi-Energy-Plattformen wie bei [[plattform-stellantis|Stellantis]] oder BMW CLAR.""",
    ["plattform-meb", "plattform-stellantis", "frontantrieb"], ["plattform"])

C["plattform-geschwister"] = (
    "Plattform-Geschwister (Badge-Engineering)", "Fahrzeuge verschiedener Marken, die technisch weitgehend baugleich sind und dieselbe Batterie nutzen.",
    """Für einen [[batteriecheck]] ist das nützlich: Geschwister haben identische Brutto-/Nettowerte und ähnliches Alterungsverhalten. Wichtige Gruppen im Bestand ([[tn-batterycheck-alle-daten]]):

| Gruppe | Fahrzeuge | Batterie brutto / netto |
|---|---|---|
| Mitsubishi i-MiEV-Drillinge | [[citroen-c-zero]], [[peugeot-ion]] | 16 / 14,5 kWh |
| VW up!-Drillinge | [[vw-e-up]], [[seat-mii-electric]], [[skoda-citigo-e-iv]] | 36,8 / 32,3 kWh |
| Stellantis-Transporter | [[citroen-e-jumpy]], [[citroen-e-spacetourer]], [[peugeot-e-expert]], [[peugeot-e-traveller]] | 50 / 46,3 oder 75 / 68 kWh |
| Stellantis-Hochdachkombis | [[citroen-e-berlingo]], [[peugeot-e-rifter]], [[peugeot-e-partner]] | 50 / 46,3 kWh |
| Erste Hochdachkombi-Generation | [[citroen-e-berlingo|E-Berlingo Multispace]], [[peugeot-partner-tepee-electric]] | 22,5 / 20,5 kWh |
| Kangoo-Familie | [[renault-kangoo-electric]], [[mercedes-eqt]] | ~45–50 kWh |
| MEB | siehe [[plattform-meb]] | 55–91 kWh |
| J1 | [[porsche-taycan]], [[audi-e-tron-gt]] | 93,4 / 83,7 oder 105 / 97 kWh |
| PPE | [[porsche-macan-electric]], [[audi-q6-e-tron]] | 100 / ~95 kWh |
| E-GMP | siehe [[plattform-e-gmp]] | 58–110 kWh |
| Hyundai/Kia 64-kWh-Generation | [[hyundai-kona-electric]], [[kia-niro-ev|Kia e-Niro]], [[kia-soul-ev|Kia e-Soul]] | 67,5 / 64 kWh |
| Volvo CMA | [[volvo-ex40]], [[volvo-ec40]] | 69–82 kWh |
| BMW iX1/iX2, Mini Countryman | [[bmw-ix1]], [[bmw-ix2]], [[mini-countryman-electric]] | 66,5 / 64,6–64,7 kWh |

Der [[mercedes-eqt]] basiert auf dem Renault Kangoo; die Batteriewerte weichen im Bestand leicht ab (50/45 vs. 48/45 kWh) – siehe [[datenqualitaet]].""",
    ["plattform-meb", "plattform-stellantis", "plattform-e-gmp"], ["plattform"])

C["typbezeichnungen"] = (
    "Typbezeichnungen", "Wie Hersteller Leistungsstufe, Batterie und Antrieb in Modellnamen codieren – ein Lesehilfe-Artikel.",
    """Die Variantennamen in [[tn-batterycheck-alle-daten]] folgen herstellerspezifischen Codes:

| Hersteller | Schema | Bedeutung |
|---|---|---|
| [[audi]] | 35 / 40 / 45 / 50 / 55 e-tron | Leistungsklasse, nicht Batteriegröße; „quattro" = [[allradantrieb]]; „S"/„RS" = Sportmodell |
| [[bmw]] | eDrive / xDrive + Zahl, M50/M60/M70 | eDrive = Heck-, xDrive = Allrad; Zahl = Leistungsstufe |
| [[mercedes]] | EQA 250 / 300 4MATIC / 350 4MATIC | Leistungsstufe; „+" = größere Batterie (73,9 statt 69,7 kWh) |
| [[volkswagen]] | Pure / Pro / Pro S / GTX | Pure = kleinste Batterie, Pro = mittlere/große, Pro S = größte, GTX = Sport-Allrad |
| [[skoda]] | 50 / 60 / 80 / 85, „x" | Zahl grob ≈ Batterie-/Leistungsstufe; „x" = [[allradantrieb]] |
| [[tesla]] | 60/70/75/85/90/100 (+D, P) | Zahl ≈ Batterie in kWh (brutto); D = Dual Motor, P = Performance, L = Ludicrous |
| [[renault]] Zoe | R/Q + Zahl, Z.E. 40/50 | R = Renault-eigener Motor, Q = Continental-Motor mit schnellem AC-Laden (43 kW); Zahl = NEFZ-Reichweite in km (Q210, R240) bzw. PS (R75, R90, Q90, R110, R135); Z.E. 40/50 = Batterie-Generation |
| [[kia]], [[hyundai]] | Standard / Long Range, 2WD / AWD | Batteriestufe und Antrieb |
| [[ford]] | SR / ER, RWD / AWD | Standard / Extended Range |
| [[volvo]] | Single Motor / Twin Motor, ER | Ein oder zwei Motoren; ER = Extended Range |
| [[porsche]] | Taycan / 4 / 4S / GTS / Turbo / Turbo S / Turbo GT | Leistungsstufen; Batterie davon teils unabhängig |

Achtung: Zahlen im Modellnamen stimmen **nicht** zwingend mit der Batteriegröße überein (Audi Q4 **40** e-tron gibt es mit 63 *und* 82 kWh brutto).""",
    ["allradantrieb", "hinterradantrieb", "karosserieformen", "modellpflege"], ["bezeichnungen"])

C["karosserieformen"] = (
    "Karosserieformen", "Varianten der Aufbauform eines Modells – beeinflussen Aussehen und Luftwiderstand, meist nicht die Batterie.",
    """Im Bestand kommen folgende Zusätze vor ([[tn-batterycheck-alle-daten]]):

- **Sportback** (Audi) – SUV-Coupé mit abfallender Dachlinie ([[audi-e-tron]], [[audi-q4-e-tron]], [[audi-q6-e-tron]], [[audi-q8-e-tron]]).
- **Coupé** (Škoda) – [[skoda-enyaq|Enyaq Coupé]].
- **Sport Turismo** (Porsche) – Kombi/Shooting Brake des [[porsche-taycan]]; **Cross Turismo** – höhergelegter Kombi mit Offroad-Optik.
- **Tourer** (VW) – Kombi des [[vw-id-7]]; **Touring** (BMW) – Kombi des [[bmw-i5]].
- **Fastback / Hatchback** (Kia) – Limousine mit Fließheck bzw. Schrägheck beim [[kia-ev4]].
- **SW** (Peugeot) – Kombi (*Station Wagon*) des [[peugeot-e-308]].
- **Kurz / Lang / Extra lang**, **M / XL / XS**, **L2 / L3**, **LWB** – Längenvarianten bei Transportern und Vans ([[elektro-transporter]]).

Die Batterie ist in der Regel dieselbe wie beim Basismodell.""",
    ["typbezeichnungen", "elektro-transporter"], ["bezeichnungen"])

C["modellpflege"] = (
    "Modellpflege (Facelift)", "Überarbeitung eines Modells während der Bauzeit – bei Elektroautos oft mit neuer Batterie.",
    """Bei Elektroautos bringt die Modellpflege häufig neue Zellgenerationen mit mehr Kapazität bei gleicher Baugröße. Deshalb hat dieselbe Modellbezeichnung im Bestand oft mehrere Batteriewerte – für einen [[batteriecheck]] muss das Baujahr bzw. die Batterie-Generation bekannt sein.

**Beispiele** ([[tn-batterycheck-alle-daten]]):
- [[bmw-i3]]: 22 → 33,2 → 42,2 kWh brutto (2013 / 2016 / 2018)
- [[renault-zoe]]: 22 kWh-Klasse (25,9) → Z.E. 40 (44,1) → Z.E. 50 (54,7 kWh)
- [[hyundai-ioniq-5]] / [[kia-ev6]]: 72,6 → 77,4 → 84 kWh
- [[porsche-taycan]]: 93,4 → 105 kWh (J1.2, 2024)
- [[vw-e-up]]: 18,7 → 36,8 kWh
- [[tesla-model-3]]: diverse Pack-Generationen zwischen 75 und 82 kWh im Long Range""",
    ["typbezeichnungen", "batteriecheck", "software-lock"], ["bezeichnungen"])

C["elektro-transporter"] = (
    "Elektro-Transporter und Vans", "Leichte Nutzfahrzeuge und Großraum-Pkw mit Elektroantrieb – im Bestand vor allem von Stellantis, Mercedes, Renault und VW.",
    """Transporter haben eigene Anforderungen: hohe Zuladung, wechselnde Beladung, oft kurze, planbare Tagesstrecken. Viele Hersteller bieten deshalb zwei Batteriegrößen an.

**Im Bestand** ([[tn-batterycheck-alle-daten]]):
- **Stellantis** – [[citroen-e-jumpy]], [[citroen-e-spacetourer]], [[peugeot-e-expert]], [[peugeot-e-traveller]] (50/75 kWh), [[citroen-e-berlingo]], [[peugeot-e-rifter]], [[peugeot-e-partner]] (50 kWh), ältere [[peugeot-partner-tepee-electric]] (22,5 kWh).
- **Mercedes-Benz** – [[mercedes-evito]], [[mercedes-eqv]], [[mercedes-eqt]], [[mercedes-esprinter]] (bis ca. 119 kWh, [[lfp-zellchemie|LFP]]).
- **Renault** – [[renault-kangoo-electric]], [[renault-master-electric]].
- **Volkswagen** – [[vw-id-buzz]] inkl. Cargo.
- **Ford** – [[ford-f-150-lightning]] (Pick-up, USA).

Längenvarianten siehe [[karosserieformen]]. Viele Modelle sind [[plattform-geschwister]].""",
    ["plattform-stellantis", "plattform-geschwister", "karosserieformen"], ["nutzfahrzeug"])
