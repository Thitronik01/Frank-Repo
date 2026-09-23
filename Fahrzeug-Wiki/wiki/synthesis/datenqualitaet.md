---
type: "synthesis"
updated: "2026-09-23"
tags: ["datenqualitaet", "lint"]
---

# Datenqualität der Rohquelle

**Anlass:** Befunde beim Ingest von [[tn-batterycheck-alle-daten]] am 2026-09-23

## Stand

Die Quelle ist formal vollständig: Das Blatt „Übersicht“ bestätigt für alle 19 Marken, dass die extrahierten Zeilen der Quellangabe entsprechen (469/469). Inhaltlich gibt es aber **5 automatisch erkannte Auffälligkeiten** (Duplikate, unmögliche Werte, Näherungswerte) und **161 fachliche Hinweise** aus der Einordnung der einzelnen Fahrzeuge.

## Automatisch erkannte Befunde

- [[cupra-born|Cupra Born]]: **Netto > Brutto:** „Born“ 53 kWh brutto / 60,0 kWh netto (Zeile 99) – physikalisch unmöglich, vermutlich vertauschte oder falsche Werte.
- [[mercedes-esprinter|Mercedes-Benz eSprinter]]: **Näherungswert:** „eSprinter LFP“ ist in der Quelle als „ca. 119 kWh“ angegeben (Zeile 192).
- [[mercedes-esprinter|Mercedes-Benz eSprinter]]: **Näherungswert:** „eSprinter LFP“ ist in der Quelle als „ca. 60 kWh“ angegeben (Zeile 193).
- [[mercedes-esprinter|Mercedes-Benz eSprinter]]: **Näherungswert:** „eSprinter LFP“ ist in der Quelle als „ca. 85 kWh“ angegeben (Zeile 194).
- [[porsche-taycan|Porsche Taycan]]: **Duplikat:** „Taycan Sport Turismo“ 93,4/83,7 kWh steht 2× in der Quelle (Zeilen 281, 282).

## Uneinheitliche Schreibweisen

- Hersteller „Citroen“ ohne Trema (offiziell Citroën), Modelle „e-C4“ statt „ë-C4“; „E-Berlingo Multispace“ mit großem E neben „e-Berlingo“.
- „Mercedes“ statt „Mercedes-Benz“; „Skoda“ statt „Škoda“.
- Leerzeichen uneinheitlich: BMW „iX xDrive 40“ vs. „iX1 xDrive30“.
- Werte teils mit, teils ohne Nachkommastelle („71 kWh“ vs. „71.0 kWh“); Dezimalpunkt statt Komma.

## Fachliche Hinweise je Fahrzeug

### [[audi-e-tron|Audi e-tron]]

- Zeile 7 (e-tron S quattro, 105/97 kWh) passt nicht zur Baureihe: 105/97 kWh entspricht der Performancebatterie Plus von Porsche Taycan/Audi e-tron GT nach Modellpflege; der Sportback S (Zeile 12) steht mit 95/86,5 kWh. Wahrscheinlich Datenfehler.
- Der Nettowert 89,0 kWh (Zeilen 5 und 11) entspricht dem Wert des Q8 50 e-tron; ob er für den e-tron 55 zutrifft, ist unsicher.
- Drei Nettowerte bei identischer Bezeichnung e-tron 55 quattro (83,6 / 86,5 / 89,0 kWh) – ohne Modelljahr nicht eindeutig zuzuordnen.

### [[audi-e-tron-gt|Audi e-tron GT]]

- Nach der Modellpflege 2024 heißen die Versionen S e-tron GT, RS e-tron GT und RS e-tron GT performance und haben alle die 105-kWh-Batterie. Der Eintrag RS e-tron GT mit 93,4 kWh (Zeile 36) bezieht sich daher vermutlich auf das Vor-Facelift-Modell; ein RS e-tron GT ab 2024 mit 105 kWh fehlt in den Daten.

### [[audi-q4-e-tron|Audi Q4 e-tron]]

- Q4 40 e-tron und Q4 Sportback 40 e-tron erscheinen jeweils zweimal mit unterschiedlichen Batterien (63 und 82 kWh brutto); die zeitliche Zuordnung der Bezeichnungen ist ohne Modelljahr nicht eindeutig.

### [[audi-q8-e-tron|Audi Q8 e-tron]]

- Unterschiedliches Zellformat (Pouch beim 95-kWh-Akku, prismatisch beim 114-kWh-Akku) wird häufig genannt, ist hier aber nicht verifiziert.
- Bauzeit: Produktion vermutlich von Ende 2022 bis Anfang 2025 (Schließung des Werks Brüssel) – Angabe prüfen.

### [[bmw-i3|BMW i3]]

- Für den i3s (Range Extender) fehlt in den Daten die 120-Ah-Version (42,2 kWh); ob sie angeboten wurde, ist hier nicht geprüft.
- Die Ah-Bezeichnungen (60/94/120 Ah) sind geläufig, stehen aber nicht in den Rohdaten.

### [[bmw-i4|BMW i4]]

- i4 M60 xDrive ist mit 81,1 kWh netto gelistet, die übrigen 83,9-kWh-Versionen mit 80,7 kWh – vermutlich Rundungs- oder Quellenunterschied bei gleicher Batterie.

### [[bmw-i5|BMW i5]]

- Zeile 58 heißt nur "i5 M60", Zeile 59 "i5 M60 xDrive Touring" – uneinheitliche Schreibweise; der i5 M60 hat ebenfalls Allradantrieb.

### [[bmw-ix|BMW iX]]

- Die Nettowerte der 111,5-kWh-Batterie variieren (107,7 / 108,9 / 109,1 / 109,4 kWh), der Puffer wäre teils sehr klein (ca. 2 kWh). Andere Quellen nennen für den iX xDrive50 deutlich niedrigere Nettowerte – prüfen.
- iX xDrive 40 mit 74,4 kWh netto bei 76,6 kWh brutto ergibt ebenfalls einen ungewöhnlich kleinen Puffer; Quelle prüfen.
- Schreibweise mit Leerzeichen ("xDrive 40") statt "xDrive40".

### [[bmw-ix2|BMW iX2]]

- Zeile 74 lautet "iX2 eDrive30"; üblich ist beim iX2 die Bezeichnung xDrive30 (Allradantrieb). Wahrscheinlich Schreibfehler.

### [[bmw-ix3|BMW iX3]]

- Nettowert mit zwei Nachkommastellen (73,83 kWh) – ungewöhnlich präzise im Vergleich zu den übrigen Einträgen.
- Bauzeit des G08 nicht sicher belegt (ca. ab 2020); der neue iX3 der Neuen Klasse fehlt in den Daten.

### [[citroen-c-zero|Citroën C-Zero]]

- In der Literatur werden für i-MiEV/C-Zero/iOn je nach Baujahr sowohl 16 kWh als auch 14,5 kWh als Gesamtkapazität genannt. Möglicherweise ist der Wert 14,5 kWh keine Nettokapazität, sondern die Bruttokapazität einer späteren Batterieversion – bitte prüfen.

### [[citroen-e-berlingo|Citroën ë-Berlingo]]

- Unter einem Slug sind zwei Fahrzeuggenerationen zusammengefasst: das alte Berlingo-Elektromodell (22,5 kWh) und der aktuelle ë-Berlingo (50/52 kWh). Ggf. trennen.
- Schreibweise uneinheitlich: „e-Berlingo“ vs. „E-Berlingo Multispace“.
- Die 52-kWh-Batterie (50,0 kWh netto) hat einen deutlich kleineren Puffer als die 50-kWh-Version (46,3 kWh netto). Bei den Peugeot-Geschwistern (e-Rifter, e-Partner) fehlt die 52-kWh-Version in den Rohdaten.
- Die genaue Zuordnung der 52-kWh-Batterie zur Modellpflege (Jahr) ist nicht gesichert.

### [[citroen-e-c3|Citroën ë-C3]]

- Sehr kleiner Puffer: 44 kWh brutto vs. 43,8 kWh netto (ca. 0,5 %). Möglicherweise ist der Bruttowert gerundet oder die Nettoangabe entspricht eher der Herstellerangabe zur Gesamtkapazität.

### [[citroen-e-c3-aircross|Citroën ë-C3 Aircross]]

- Sehr kleiner Puffer bei beiden Batterien (44/43,8 und 54/53,5 kWh).
- Ob auch die Extended-Range-Batterie auf LFP-Zellen basiert, ist nicht gesichert.

### [[citroen-e-jumpy|Citroën ë-Jumpy Combi]]

- Der Puffer der 75-kWh-Batterie (68,0 kWh netto) ist mit rund 9 % größer als der der 50-kWh-Batterie (ca. 7 %).

### [[citroen-e-spacetourer|Citroën ë-SpaceTourer]]

- Schreibweise in den Rohdaten „e-Spacetourer“, Herstellerschreibweise „ë-SpaceTourer“.

### [[cupra-born|Cupra Born]]

- Zeile 99: Nettokapazität (60,0 kWh) ist größer als die Bruttokapazität (53 kWh) – physikalisch unmöglich, vermutlich Tipp- oder Zuordnungsfehler (Einstiegsbatterie des MEB wird meist mit 45 kWh netto geführt).
- Zeilen 100 und 102 haben identische Batteriewerte; der Unterschied (e-boost) betrifft nur die Motorleistung.

### [[dacia-spring|Dacia Spring Electric]]

- Vier Zeilen mit identischen Kapazitätswerten – für die Batteriekapazität de facto Duplikate.
- Ob die Batterie beim Modell ab 2024 die Zellchemie gewechselt hat (NMC vs. LFP), ist nicht gesichert und wird hier bewusst nicht behauptet.
- Der Bruttowert 26,8 kWh taucht beim Schwestermodell Renault City K-ZE als Nettowert auf – mögliche Inkonsistenz zwischen den beiden Datensätzen.

### [[ford-f-150-lightning|Ford F-150 Lightning]]

- Bauzeit bewusst offen gelassen: Marktstart war 2022; Angaben zu einem Produktionsende bzw. einer Umstellung auf ein Modell mit Range-Extender sind nicht sicher bestätigt.
- Das Fahrzeug wurde in Europa nicht regulär angeboten; Bruttowerte stammen vermutlich aus US-Quellen.

### [[ford-mustang-mach-e|Ford Mustang Mach-E]]

- Gleiche Modellbezeichnungen erscheinen mehrfach mit identischem Brutto-, aber unterschiedlichem Nettowert (z. B. Zeilen 111/112, 118/119). Zuordnung zu Modelljahren ist in den Rohdaten nicht vermerkt.
- Dass die Batterie mit 78 kWh brutto / 72,6 kWh netto LFP-Zellen verwendet, ist eine Vermutung und nicht gesichert.
- Die Rally-Version (Zeile 117) ist nur mit dem höheren Nettowert 91 kWh gelistet, passend zu ihrer späteren Markteinführung.

### [[hyundai-inster|Hyundai Inster]]

- Die Plattformzuordnung (Ableitung vom Hyundai Casper) ist als Einordnung zu verstehen; eine offizielle Plattformbezeichnung wurde nicht übernommen.
- Zellchemie der beiden Batterien in den Rohdaten nicht angegeben und hier nicht behauptet.

### [[hyundai-ioniq-5|Hyundai IONIQ 5]]

- „IONIQ 5 Long Range 2WD“ und „IONIQ 5 Long Range AWD“ kommen je zweimal mit unterschiedlichen Kapazitäten vor (72,6 bzw. 77,4 kWh brutto) – verschiedene Batterie-Generationen unter gleichem Namen.
- „IONIQ 5 RWD“ erscheint zweimal (63,0 und 84,0 kWh brutto); gemeint sind die Standard- und die Long-Range-Batterie nach der Modellpflege.
- Uneinheitliche Antriebsbezeichnung: „2WD“ (vor der Modellpflege) und „RWD“ (danach) meinen beide Hinterradantrieb.
- Die Zuordnung der Stufen zu Modelljahren (insbesondere Einführung der 77,4-kWh-Batterie) ist aus den Rohdaten nicht ablesbar.

### [[hyundai-ioniq-6|Hyundai IONIQ 6]]

- Die Rohdaten enthalten keine Varianten nach einer möglichen Modellpflege mit größeren Batterien (wie beim IONIQ 5); ob solche Versionen fehlen, ist nicht geprüft.

### [[hyundai-ioniq-9|Hyundai IONIQ 9]]

- Bauzeit bewusst offen gelassen: Produktionsstart Ende 2024, Markteinführung in Europa 2025 – exakte Angabe nicht gesichert.
- Alle Varianten mit identischen Kapazitäten; in den Rohdaten existiert keine kleinere Batterieoption.

### [[hyundai-ioniq-electric|Hyundai IONIQ Elektro]]

- Zwei Zeilen mit identischer Bezeichnung „IONIQ Electric“ – Unterscheidung nur über die Kapazität (Generation vor/nach Modellpflege 2019).
- Die Brutto-Angabe der ersten Generation (30,5 kWh) entspricht der des Kia Soul EV (erste Generation), die Netto-Werte unterscheiden sich jedoch (28 vs. 27 kWh); ob es sich um denselben Batteriepack handelt, ist nicht belegt.

### [[hyundai-kona-electric|Hyundai Kona Elektro]]

- Vier Zeilen mit identischem Namen „Kona Electric“ ohne Hinweis auf Generation oder Batteriegröße.
- Die Batterien der 1. Generation sind mit Kia e-Niro und e-Soul identisch (42,0/39,2 und 67,5/64,0 kWh).
- Die großen Batterien der 2. Generation (68,5/65,4 kWh) und des Kia Niro EV (68,0/64,8 kWh) liegen sehr nah beieinander; ob es sich um denselben Pack mit abweichender Angabe handelt, ist unklar.

### [[kia-niro-ev|Kia e-Niro / Niro EV]]

- Die Zeilennummern sind nicht zusammenhängend (e-Niro und Niro EV liegen in der Quelle an verschiedenen Stellen), vermutlich wegen alphabetischer Sortierung.
- Niro EV 68,0/64,8 kWh vs. Kona Elektro 2. Generation 68,5/65,4 kWh – ähnliche, aber nicht identische Werte.

### [[kia-soul-ev|Kia Soul EV / e-Soul]]

- Der Puffer der ersten Soul-EV-Batterie ist mit 3,5 kWh (30,5 brutto / 27,0 netto) im Verhältnis zur Größe vergleichsweise groß.
- Zeilennummern nicht zusammenhängend (e-Soul und Soul EV an getrennten Stellen der Quelle).
- Ob die 33-kWh-Version einer Modellpflege oder einem Modelljahreswechsel zuzuordnen ist, ist aus den Rohdaten nicht ersichtlich.

### [[kia-ev3|Kia EV3]]

- Kia kommuniziert die Batterien häufig als „58,3 kWh“ und „81,4 kWh“; ob diese Werte brutto oder netto sind, wird in Quellen uneinheitlich dargestellt. Die Rohdaten führen sie als brutto.

### [[kia-ev4|Kia EV4]]

- EV4 Fastback nur mit 81,4 kWh gelistet; ob eine Standard-Range-Version des Fastback existiert oder in den Rohdaten fehlt, ist unklar.
- Brutto-/Netto-Zuordnung wie beim EV3 (Herstellerangabe 81,4 kWh wird teils als Nennwert kommuniziert).

### [[kia-ev6|Kia EV6]]

- Alle Versionsbezeichnungen (GT, Long Range 2WD/AWD, Standard Range 2WD/AWD) kommen je zweimal mit unterschiedlichen Kapazitäten vor – Generation vor und nach der Modellpflege.
- Die erste Long-Range-Batterie des IONIQ 5 (72,6/70 kWh) taucht beim EV6 nicht auf.

### [[kia-ev9|Kia EV9]]

- „EV9 RWD“ erscheint zweimal (76,1 und 99,8 kWh brutto); die kleine Batterie ist nicht als Standard Range gekennzeichnet.
- Ob die 76,1-kWh-Version in Deutschland angeboten wurde, ist nicht gesichert.

### [[mercedes-eqa|Mercedes-Benz EQA]]

- Nach der Modellpflege 2023 sollen auch weitere Versionen die größere Batterie erhalten haben; die Daten führen die 4MATIC-Modelle nur mit 69,7 kWh – ohne Modelljahr nicht eindeutig.

### [[mercedes-eqb|Mercedes-Benz EQB]]

- EQB 300 4MATIC steht zweimal mit unterschiedlichen Batterien (Zeilen 182 und 183).
- Zeile 184 "EQB 350" ohne 4MATIC: Die Leistungsstufe 350 ist bei Mercedes üblicherweise ein Allradmodell – mögliche unvollständige Bezeichnung.

### [[mercedes-eqc|Mercedes-Benz EQC]]

- Bauzeit nicht sicher belegt (Marktstart 2019, Produktionsende ca. 2023/2024).
- Die Bezeichnung in den Daten lautet nur "EQC 400"; offiziell EQC 400 4MATIC.

### [[mercedes-eqt|Mercedes-Benz EQT]]

- Runde Werte 50/45 kWh – vermutlich gerundete Herstellerangaben.

### [[mercedes-eqv|Mercedes-Benz EQV]]

- Runde Werte (66/60, 100/90 kWh) – vermutlich gerundete Herstellerangaben.

### [[mercedes-esprinter|Mercedes-Benz eSprinter]]

- Bruttowerte der LFP-Versionen sind als "ca." markiert (geschätzt).
- Die Reihenfolge der LFP-Zeilen (119, 60, 85 kWh) ist nicht nach Größe sortiert.

### [[mercedes-evito|Mercedes-Benz eVito]]

- Runde Werte (41/35, 66/60, 100/90 kWh) – vermutlich gerundete Herstellerangaben.

### [[mg-cyberster|MG Cyberster]]

- Plattform nicht angegeben: Eine Zuordnung zur MSP-Plattform des MG4 ist nicht gesichert.
- Kapazität identisch mit der größten MG4-Batterie (77,0/74,4 kWh); ob es derselbe Pack ist, ist nicht belegt.
- Die Antriebszuordnung Trophy = Hinterradantrieb, GT = Allradantrieb gilt für den europäischen Markt; in anderen Märkten können die Bezeichnungen abweichen.

### [[mg-marvel-r|MG Marvel R]]

- Bauzeit offen gelassen: Europa-Marktstart 2021, Ende des Vertriebs in Europa nicht gesichert.
- Motoranordnung der Basisversion (Hinterachse, ggf. zwei Motoren) nicht gesichert und daher nicht im Text ausgeführt.
- Puffer von 5 kWh (75 brutto / 70 netto) – deutlich größer als bei anderen MG-Modellen.

### [[mg4-electric|MG4 Electric]]

- Die 51-kWh-Batterie hat laut Rohdaten nur 0,2 kWh Puffer (51,0 brutto / 50,8 netto) – ungewöhnlich klein, bei LFP-Batterien aber nicht untypisch.
- Drei Zeilen mit identischer Bezeichnung „MG4 Electric“ – Unterscheidung nur über die Kapazität.

### [[mg5-electric|MG5 Electric]]

- „MG5 EV Long Range“ und „MG5 Electric Long Range“ mit identischen Werten (61,1/57,4 kWh) – wahrscheinlich Duplikat mit unterschiedlicher Schreibweise.
- Uneinheitliche Namensgebung „MG5 EV“ vs. „MG5 Electric“.
- Zellchemie der Standard-Range-Batterie (möglicherweise LFP) nicht gesichert und daher nicht behauptet.
- Die Einordnung als Geschwister des ZS EV bezieht sich auf die gemeinsame Konversionsbauweise und Antriebstechnik, nicht auf identische Batterien.

### [[mg-zs-ev|MG ZS EV]]

- Die Long-Range-Batterie (72,6 kWh brutto) hat denselben Bruttowert wie die erste Long-Range-Batterie des Hyundai IONIQ 5 – rein zufällige Übereinstimmung, kein technischer Zusammenhang.
- Zellchemie der Standard-Range-Batterie (möglicherweise LFP) nicht gesichert.

### [[mini-aceman|Mini Aceman]]

- Kleine Batterie hier mit 42,5/38,5 kWh, beim Cooper E dagegen 40,7/36,8 kWh – möglicherweise dieselbe Batterie mit unterschiedlichen Quellenangaben.

### [[mini-cooper-electric|Mini Cooper E / SE]]

- Cooper SE erscheint zweimal mit völlig unterschiedlichen Batterien (Zeilen 220 und 221) – zwei Fahrzeuggenerationen unter gleichem Namen.
- Nettowert 49,8 kWh bei 54,2 kWh brutto weicht vom Aceman (49,2 kWh netto bei gleicher Bruttokapazität) ab; vermutlich Quellen- oder Tippfehler.

### [[mini-countryman-electric|Mini Countryman E / SE]]

- Nettowert 64,6 kWh gegenüber 64,7 kWh bei iX1/iX2 mit identischer Batterie – Rundungsdifferenz.

### [[peugeot-e-2008|Peugeot e-2008]]

- „e-2008 SUV“ (50 kWh) ist inhaltlich ein Duplikat zu „e-2008“ (50 kWh) – nur abweichende Schreibweise.

### [[peugeot-e-208|Peugeot e-208]]

- Die Zeile 51 kWh brutto / 48,1 kWh netto passt zu keiner der bei den Geschwistermodellen erfassten Batterien (50/46,3 bzw. 54/50,8). Möglicherweise wurde ein Nettowert der neueren Batterie als Bruttowert erfasst – bitte prüfen.

### [[peugeot-e-3008|Peugeot e-3008]]

- Weitere STLA-Medium-Modelle (z. B. Peugeot e-5008, Opel Grandland Electric) sind in families.json nicht enthalten.

### [[peugeot-e-308|Peugeot e-308]]

- Die Batterie hat nach den Rohdaten dieselben Werte (54/50,8 kWh) wie die überarbeitete e-CMP-Batterie. Ob es sich um exakt dasselbe Batteriepaket handelt, ist nicht gesichert.

### [[peugeot-e-408|Peugeot e-408]]

- Die Batteriekapazität weicht vom technisch eng verwandten e-308 (54/50,8 kWh) ab; möglicherweise handelt es sich um eine neuere Batterieversion, die inzwischen auch im e-308 angeboten wird. Nicht gesichert.

### [[peugeot-e-partner|Peugeot e-Partner]]

- Die bei den Geschwistermodellen (ë-Berlingo) erfasste neuere 52-kWh-Batterie fehlt hier.
- Nicht erkennbar, ob die Zeile die Personen- oder die Nutzfahrzeugversion betrifft.

### [[peugeot-e-rifter|Peugeot e-Rifter]]

- Vier Zeilen mit identischen Werten; „Standard“ und „M“ sowie „Long“ und „XL“ sind vermutlich jeweils dieselbe Version unter verschiedenen Bezeichnungen (Duplikate).
- Die beim ë-Berlingo erfasste neuere 52-kWh-Batterie fehlt hier.

### [[peugeot-e-traveller|Peugeot e-Traveller]]

- L2/L3 und Standard/Long liefern identische Werte – vermutlich Duplikate unter zwei Namensschemata.
- Ob die Längenbezeichnungen L2/L3 mit einer Modellpflege eingeführt wurden, ist nicht gesichert.

### [[peugeot-ion|Peugeot iOn]]

- Je nach Baujahr werden für i-MiEV/C-Zero/iOn sowohl 16 kWh als auch 14,5 kWh als Gesamtkapazität genannt; möglicherweise ist 14,5 kWh eine spätere Bruttokapazität statt eines Nettowerts.

### [[peugeot-partner-tepee-electric|Peugeot Partner Tepee Electric]]

- Bauzeit nicht sicher bekannt, daher null.
- Die Konversion erfolgte nach verbreiteten Angaben in Zusammenarbeit mit einem externen Partner; Details nicht gesichert.

### [[porsche-macan-electric|Porsche Macan (Elektro)]]

- Die Audi-Schwester Q6 e-tron ist mit 100/94,9 kWh gelistet, der Macan mit 100/95 kWh – Rundungsdifferenz bei vermutlich gleicher Batterie.

### [[porsche-taycan|Porsche Taycan]]

- Doppelter Eintrag: "Taycan Sport Turismo" mit 93,4/83,7 kWh erscheint zweimal (Zeilen 281 und 282).
- Die Batteriebezeichnungen (Performancebatterie/Performancebatterie Plus) stehen nicht in den Rohdaten; die Zuordnung erfolgt über die Kapazität.

### [[renault-city-k-ze|Renault City K-ZE]]

- Die Werte weichen vom baugleichen Dacia Spring ab (dort 26,8 kWh brutto / 25,0 kWh netto). Hier erscheint 26,8 kWh als Nettowert – möglicherweise ist der Bruttowert 30 kWh unsicher oder falsch.
- Bauzeit nicht sicher bekannt, daher null.

### [[renault-kangoo-electric|Renault Kangoo Z.E. / E-Tech]]

- Unter einem Slug sind zwei Fahrzeuggenerationen (Kangoo Z.E. und Kangoo E-Tech) zusammengefasst.
- Für den Kangoo Z.E. mit kleiner Batterie findet man 22 kWh teils als Brutto-, teils als Nettoangabe.
- Mercedes EQT ist in families.json mit 50/45 kWh erfasst, der Kangoo E-Tech mit 48/45 kWh – gleicher Nettowert, abweichender Bruttowert.

### [[renault-master-electric|Renault Master Z.E. / E-Tech]]

- Zwei Generationen unter einem Slug zusammengefasst.
- Für den Master E-Tech werden in Herstellerangaben häufig 40 kWh und 87 kWh (nutzbar) genannt. Die Zeile 55/52 kWh passt dazu nicht – bitte prüfen.
- Die Batterie des Master Z.E. (33/31 kWh) hat dieselben Werte wie der Kangoo Z.E. mit großer Batterie; eine technische Identität wird hier nicht behauptet.
- Die Werte 92/87 kWh stimmen mit der großen Batterie des Renault Scenic E-Tech überein; ob es sich um dasselbe Batteriepaket handelt, ist nicht gesichert.

### [[renault-scenic-e-tech|Renault Scenic E-Tech]]

- Weitere AmpR-Medium-Modelle (Renault Megane E-Tech, Nissan Ariya) sind in families.json nicht enthalten.
- Die Werte der großen Batterie (92/87 kWh) stimmen mit dem Renault Master E-Tech überein.

### [[renault-twingo-electric|Renault Twingo Electric]]

- Kleiner Puffer (22 vs. 21,3 kWh); in manchen Quellen wird 22 kWh als nutzbare Kapazität angegeben.
- Das Schwestermodell Smart ForFour EQ ist nicht in families.json enthalten.

### [[renault-zoe|Renault Zoe]]

- „Zoe R110“ und „Zoe R110 Z.E. 40“ haben identische Werte (44,1/41,0 kWh) – vermutlich Duplikat.
- „Zoe R75“ erscheint mit zwei Batterien (25,9 und 44,1 kWh); die Zuordnung der R75-Variante ist nicht gesichert.
- „Zoe R90 Entry“ mit 25,9 kWh ist ungewöhnlich, da R90 sonst mit der Z.E.-40-Batterie verbunden ist – bitte prüfen.
- Die erste Batteriegeneration wird im Handel als „22 kWh“ bezeichnet, in den Rohdaten aber mit 25,9 kWh brutto / 23,3 kWh netto geführt.
- Die Bedeutung der Zahl in den Motorbezeichnungen (Reichweite vs. Leistung) ist je nach Generation unterschiedlich; hier nur grob beschrieben.

### [[seat-mii-electric|Seat Mii electric]]

- Bauzeit offen gelassen: Markteinführung um 2019/2020, genaues Produktionsende nicht sicher belegt.

### [[skoda-citigo-e-iv|Škoda Citigo e iV]]

- Schreibweise in den Rohdaten „Citigo-e IV“; offizielle Schreibweise ist „Citigo e iV“.
- Bauzeit offen gelassen, da genaue Produktionsdaten nicht sicher sind (Markteinführung um 2019/2020, nur kurze Bauzeit).

### [[skoda-enyaq|Škoda Enyaq]]

- Doppelte Einträge durch Namensschema: „Enyaq iV 85“ (Zeile 340) und „Enyaq 85“ (Zeile 327) haben identische Werte, ebenso die jeweiligen x- und Coupé-Versionen.
- Schreibweise „Coupe“ ohne Akzent (offiziell „Coupé“).
- Zeilen 333/334 und 335/336: gleicher Name, zwei leicht unterschiedliche Batterien (62/58 vs. 63/59 kWh).

### [[tesla-model-3|Tesla Model 3]]

- Mehrfach vorkommende Bezeichnungen mit unterschiedlichen Werten (z. B. Long Range AWD in vier Varianten, Zeilen 345–348); Zuordnung zu Baujahr, Werk oder Zelllieferant fehlt in den Rohdaten.
- Die Bruttowerte bei Tesla sind oft nicht offiziell veröffentlicht und stammen aus Messungen bzw. Schätzungen Dritter.
- Standard Range plus in drei Varianten (Zeilen 356–358), vermutlich unterschiedliche Zellchemien (NCA vs. LFP).

### [[tesla-model-s|Tesla Model S]]

- Viele Nettowerte entsprechen exakt 95 % des Bruttowerts (z. B. 100/95, 90/85,5, 85/80,8, 70/66,5) – wirkt schematisch berechnet statt gemessen.
- Bauzeit offen gelassen: Produktionsstart 2012; ein angekündigtes Produktionsende (2026) ist nicht sicher bestätigt.
- „Model S P60“ und „Model S P70“ sind als offizielle Varianten nicht bekannt; möglicherweise Fehler in den Rohdaten.
- „Model S 70“ und „70D“ erscheinen mit 70 kWh und mit 75 kWh brutto; die 75-kWh-Variante könnte ebenfalls softwarebegrenzt sein – nicht gesichert.
- „Model S Performance“ mit zwei Batteriewerten (100 und 103 kWh brutto, Zeilen 383/384).

### [[tesla-model-x|Tesla Model X]]

- Nettowerte vielfach exakt 95 % des Bruttowerts – vermutlich schematisch berechnet.
- Bauzeit offen gelassen: Produktionsstart 2015; ein angekündigtes Produktionsende (2026) ist nicht sicher bestätigt.
- „Model X Performance“ mit zwei Batteriewerten (100 und 103 kWh brutto, Zeilen 398/399).

### [[tesla-model-y|Tesla Model Y]]

- „Model Y RWD“ und „Long Range AWD“ jeweils mit zwei Batteriewerten; Zuordnung zu Werk oder Baujahr fehlt.
- Bruttowerte bei Tesla sind überwiegend Messwerte Dritter, keine Herstellerangaben.

### [[vw-e-up|VW e-up!]]

- Schreibweise in den Rohdaten „e-Up“; offizielle Schreibweise ist „e-up!“.
- Bauzeit offen gelassen: Markteinführung 2013, das Produktionsende ist nicht sicher belegt.

### [[vw-id-3|VW ID.3]]

- ID.3 Pure und Pure Performance (Zeilen 416/417): 55 kWh brutto bei nur 45 kWh netto – ungewöhnlich großer Puffer (ca. 18 %). Der Bruttowert ist vermutlich zu hoch angesetzt oder bezieht sich auf eine andere Batterie.
- Die Varianten GTX und Pro S nach der Modellpflege sind in den Rohdaten nicht gesondert aufgeführt.

### [[vw-id-4|VW ID.4]]

- Mehrere Bezeichnungen mit identischen Werten (82/77 kWh) für im Grunde dieselbe Batterie; „ID.4 AWD“/„ID.4 RWD“ überschneiden sich vermutlich mit „Pro 4M“/„Pro“.
- Eine mittlere Batterie (62/58 kWh), die es beim ID.4 zeitweise gab, ist in den Rohdaten nicht enthalten.

### [[vw-id-5|VW ID.5]]

- „ID.5 GTX“ und „ID.5 GTX 4M“ bezeichnen vermutlich dasselbe Fahrzeug (der GTX hat grundsätzlich Allradantrieb) – mögliche Dublette.

### [[vw-id-buzz|VW ID. Buzz]]

- „ID.BUZZ Pro“ und „ID.BUZZ GTX“ jeweils mit zwei Batteriewerten (84 und 91 kWh brutto); vermutlich kurzer vs. langer Radstand, in den Rohdaten nicht gekennzeichnet.
- Schreibweise „ID.BUZZ“ in den Rohdaten; offiziell „ID. Buzz“.
- Die Zuordnung der 84-kWh-Batterie zu einer bestimmten Modellpflege ist nicht gesichert.

### [[volvo-ec40|Volvo EC40 (C40 Recharge)]]

- Uneinheitlicher Nettowert für die 69-kWh-Batterie: 67 kWh (Pure Electric, EC40 Single Motor) gegenüber 66 kWh (C40 Recharge Single Motor).
- "Recharge Pure Electric" und "Recharge Twin Pure Electric" sind ältere Verkaufsbezeichnungen und überschneiden sich mit den späteren Single-/Twin-Motor-Namen.

### [[volvo-ex40|Volvo EX40 (XC40 Recharge)]]

- Uneinheitlicher Nettowert für die 69-kWh-Batterie: 67 kWh (Pure Electric, EX40 Single Motor) gegenüber 66 kWh (XC40 Recharge Single Motor).
- Viele Namensvarianten für gleiche Technik (P8 AWD, Twin Pure Electric, Twin Motor) – die Einträge überschneiden sich.

### [[volvo-ex90|Volvo EX90]]

- Die Single-Motor-Version war nicht in allen Märkten erhältlich (hier nicht verifiziert).
- Eine spätere Umstellung auf 800-Volt-Technik wird berichtet, ist hier aber nicht geprüft.

## Empfehlungen

1. Cupra Born Zeile 99 (53/60 kWh) korrigieren – Brutto und Netto sind so unmöglich; gegen Herstellerangabe prüfen.
2. Exakte Duplikate entfernen (Porsche Taycan Sport Turismo 93,4/83,7).
3. Spalte **Modelljahr / Batterie-Generation** ergänzen – viele gleichnamige Varianten haben mehrere Werte.
4. „ca.“-Werte (Mercedes eSprinter LFP) durch Herstellerangaben ersetzen.
5. Werte mit Puffer < 1 % gegen Herstellerdatenblätter prüfen.
