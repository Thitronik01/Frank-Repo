---
type: "synthesis"
updated: "2026-09-24"
tags: ["datenqualitaet", "lint", "korrekturen"]
---

# Datenqualität der Rohquelle

**Anlass:** Befunde beim Ingest von [[tn-batterycheck-alle-daten]] am 2026-09-23, Bereinigung am 2026-09-24

## Stand

Die Rohquelle bleibt unverändert. Das Wiki nutzt seit 2026-09-24 die **bereinigte Fassung** `data/tn_batterycheck_bereinigt.xlsx` (erzeugt von `tools/clean.py` aus der Rohquelle und `tools/corrections.json`).

| Maßnahme | Anzahl |
|---|---|
| Zeilen mit korrigierten Werten | 10 (12 Werte) |
| Entfernte Duplikate | 2 |
| Als Alias gekennzeichnet (gleiches Fahrzeug, anderer Name) | 12 |
| Schreibweisen vereinheitlicht | 56 |
| Noch zu prüfen (offenes Issue) | 9 Zeilen |
| Näherungswerte („ca.“) | 3 Zeilen |
| Zeilen in der bereinigten Fassung | 467 von 469 |

## Korrekturen

| Zeile | Fahrzeug | Feld | Alt | Neu | Grund | Beleg |
|---|---|---|---|---|---|---|
| 7 | [[audi-e-tron\|Audi e-tron S quattro]] | Brutto kWh | 105 | 95 | 105/97 sind die Werte der großen Taycan-Batterie. Der e-tron S (SUV) hat dieselbe 95-kWh-Batterie wie der Sportback S. | [Quelle 1](https://ev-database.org/car/1658/Audi-e-tron-S), [Quelle 2](https://ev-database.org/car/1659/Audi-e-tron-S-Sportback), [#5](https://github.com/Thitronik01/Frank-Repo/issues/5) |
| 7 | [[audi-e-tron\|Audi e-tron S quattro]] | Netto kWh | 97 | 86,5 | 105/97 sind die Werte der großen Taycan-Batterie. Der e-tron S (SUV) hat dieselbe 95-kWh-Batterie wie der Sportback S. | [Quelle 1](https://ev-database.org/car/1658/Audi-e-tron-S), [Quelle 2](https://ev-database.org/car/1659/Audi-e-tron-S-Sportback), [#5](https://github.com/Thitronik01/Frank-Repo/issues/5) |
| 58 | [[bmw-i5\|BMW i5 M60]] | Modell | i5 M60 | i5 M60 xDrive | Offizielle Bezeichnung „i5 M60 xDrive“. | [Quelle 1](https://ev-database.org/car/1907/BMW-i5-M60-xDrive-Sedan), [#15](https://github.com/Thitronik01/Frank-Repo/issues/15) |
| 65 | [[bmw-ix\|BMW iX M60]] | Netto kWh | 107,7 | 105,2 | Laut BMW-Datenblatt und ev-database hat der iX M60 111,5 / 105,2 kWh. | [Quelle 1](https://ev-database.org/uk/car/1590/BMW-iX-M60), [Quelle 2](https://www.press.bmwgroup.com/asia/article/attachment/T0334029EN/481303), [#9](https://github.com/Thitronik01/Frank-Repo/issues/9) |
| 67 | [[bmw-ix\|BMW iX xDrive 40]] | Netto kWh | 74,4 | 71 | Laut BMW-Datenblatt (06/2021) hat der iX xDrive40 76,6 / 71,0 kWh. | [Quelle 1](https://www.press.bmwgroup.com/asia/article/attachment/T0334029EN/481303), [Quelle 2](https://ev-database.org/uk/car/1472/BMW-iX-xDrive-40), [#9](https://github.com/Thitronik01/Frank-Repo/issues/9) |
| 69 | [[bmw-ix\|BMW iX xDrive 50]] | Netto kWh | 109,4 | 105,2 | Laut BMW-Datenblatt (06/2021) hat der iX xDrive50 111,5 / 105,2 kWh. | [Quelle 1](https://www.press.bmwgroup.com/asia/article/attachment/T0334029EN/481303), [#9](https://github.com/Thitronik01/Frank-Repo/issues/9) |
| 74 | [[bmw-ix2\|BMW iX2 eDrive30]] | Modell | iX2 eDrive30 | iX2 xDrive30 | „eDrive30“ gibt es nicht, nur eDrive20 und xDrive30. | [Quelle 1](https://www.bimmertoday.de/2023/10/11/bmw-ix2-xdrive30-edrive20-bilder-infos-zum-elektro-x2/), [#15](https://github.com/Thitronik01/Frank-Repo/issues/15) |
| 84 | [[citroen-e-c3-aircross\|Citroen e-C3 Aircross Extended Range]] | Netto kWh | 53,5 | 52,8 | ADAC (Herstellerdaten): 54,0 / 52,8 kWh. Die 53,5 kWh sind ein Schätzwert von ev-database. Der baugleiche Opel Frontera ER hat laut ADAC 52,0 kWh netto. | [Quelle 1](https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/citroen/c3-aircross/2generation/350756/), [Quelle 2](https://ev-database.org/car/3228/Citroen-e-C3-Aircross-Extended-Range-54-kWh), [#10](https://github.com/Thitronik01/Frank-Repo/issues/10) |
| 99 | [[cupra-born\|Cupra Born]] | Brutto kWh | 53 | 63 | 53/60 ist unmöglich (netto > brutto). Gemeint ist vermutlich die 59-kWh-Batterie ab Modelljahr 2025 mit 63 / 59 kWh (ev-database; electrive nennt 63 / 60). Die Zuordnung ist erschlossen und muss bestätigt werden. | [Quelle 1](https://ev-database.org/de/pkw/3262/CUPRA-Born-150-kW---59-kWh), [Quelle 2](https://ev-database.org/car/2233/CUPRA-Born-170-kW---59-kWh), [Quelle 3](https://www.electrive.net/2024/08/08/cupra-ueberarbeitet-das-born-angebot/), [#1](https://github.com/Thitronik01/Frank-Repo/issues/1) |
| 99 | [[cupra-born\|Cupra Born]] | Netto kWh | 60 | 59 | 53/60 ist unmöglich (netto > brutto). Gemeint ist vermutlich die 59-kWh-Batterie ab Modelljahr 2025 mit 63 / 59 kWh (ev-database; electrive nennt 63 / 60). Die Zuordnung ist erschlossen und muss bestätigt werden. | [Quelle 1](https://ev-database.org/de/pkw/3262/CUPRA-Born-150-kW---59-kWh), [Quelle 2](https://ev-database.org/car/2233/CUPRA-Born-170-kW---59-kWh), [Quelle 3](https://www.electrive.net/2024/08/08/cupra-ueberarbeitet-das-born-angebot/), [#1](https://github.com/Thitronik01/Frank-Repo/issues/1) |
| 184 | [[mercedes-eqb\|Mercedes EQB 350]] | Modell | EQB 350 | EQB 350 4MATIC | Den EQB 350 gibt es nur mit 4MATIC. | [Quelle 1](https://en.wikipedia.org/wiki/Mercedes-Benz_EQB), [#15](https://github.com/Thitronik01/Frank-Repo/issues/15) |
| 187 | [[mercedes-eqt\|Mercedes EQT]] | Brutto kWh | 50 | 48 | Der EQT nutzt die 45-kWh-Batterie des Renault Kangoo E-Tech. ev-database: 48 / 45 kWh; für 50 kWh brutto gibt es keinen Beleg. | [Quelle 1](https://ev-database.org/car/1908/Mercedes-Benz-EQT-200-Standard), [Quelle 2](https://ev-database.org/car/1802/Renault-Kangoo-E-Tech-Electric), [#3](https://github.com/Thitronik01/Frank-Repo/issues/3) |
| 219 | [[mini-cooper-electric\|Mini Cooper E]] | Netto kWh | 36,8 | 36,6 | Laut ev-database und Auto Bild hat der Cooper E 40,7 / 36,6 kWh. | [Quelle 1](https://ev-database.org/uk/car/1997/Mini-Cooper-E), [#8](https://github.com/Thitronik01/Frank-Repo/issues/8) |
| 221 | [[mini-cooper-electric\|Mini Cooper SE]] | Netto kWh | 49,8 | 49,2 | Der neue Cooper SE (J01) hat dieselbe Batterie wie der Aceman SE: 54,2 / 49,2 kWh. | [Quelle 1](https://ev-database.org/uk/car/1998/Mini-Cooper-SE), [#8](https://github.com/Thitronik01/Frank-Repo/issues/8) |
| 282 | [[porsche-taycan\|Porsche Taycan Sport Turismo]] | Zeile | 93,4 kWh / 83,7 kWh | entfernt | Exaktes Duplikat von Zeile 281 (Taycan Sport Turismo, 93,4 / 83,7 kWh). |  |
| 297 | [[renault-city-k-ze\|Renault City K-ZE]] | Brutto kWh | 30 | 27,4 | 30 kWh brutto sind nicht belegt (nur auto-data.net). Renault nennt 26,8 kWh; der baugleiche Dacia Spring hat laut ADAC (Herstellerdaten) 27,4 / 26,8 kWh. | [Quelle 1](https://paultan.org/2019/09/10/renault-k-ze-launched-in-china/), [Quelle 2](https://www.batterydesign.net/dacia-spring-battery/), [#4](https://github.com/Thitronik01/Frank-Repo/issues/4) |
| 317 | [[renault-zoe\|Renault Zoe R75]] | Zeile | 25,9 kWh / 23,3 kWh | entfernt | Einen Zoe R75 mit 22-kWh-Batterie gab es nicht; der R75 wurde nur mit Z.E. 40 angeboten (Zeile 318). | [#13](https://github.com/Thitronik01/Frank-Repo/issues/13) |

## Offene Klärungen

Was sich nicht eindeutig belegen ließ, wird in GitHub-Issues geklärt. Bis dahin sind die betroffenen Zeilen als „zu prüfen“ markiert und auf der Fahrzeugseite unter „Offene Punkte“ vermerkt.

| Issue | Thema | Zeilen | Stand |
|---|---|---|---|
| [#1](https://github.com/Thitronik01/Frank-Repo/issues/1) | Cupra Born (Zeile 99): Netto größer als Brutto | 99 | korrigiert auf 63 / 59 kWh (erschlossen) – bitte bestätigen |
| [#2](https://github.com/Thitronik01/Frank-Repo/issues/2) | VW ID.3 Pure 55/45 vs. ID.4 Pure 55/52 | 416, 417 | geklärt: Werte korrekt (Software-Lock) – geschlossen am 2026-09-24 |
| [#3](https://github.com/Thitronik01/Frank-Repo/issues/3) | Mercedes EQT vs. Renault Kangoo E-Tech | 187 | korrigiert auf 48 / 45 kWh – geschlossen am 2026-09-24 |
| [#4](https://github.com/Thitronik01/Frank-Repo/issues/4) | Renault City K-ZE vs. Dacia Spring | 297, 105–108 | K-ZE korrigiert; Spring: Quellen widersprechen (netto 26,8 vs. 25,0) – Entscheidung offen |
| [#5](https://github.com/Thitronik01/Frank-Repo/issues/5) | Audi e-tron S quattro mit Taycan-Werten | 7 | korrigiert auf 95 / 86,5 kWh – geschlossen am 2026-09-24 |
| [#6](https://github.com/Thitronik01/Frank-Repo/issues/6) | Peugeot e-208 51/48,1 kWh | 228 | geklärt: Zeile korrekt (156 PS, 11/2022–04/2025) – geschlossen am 2026-09-24 |
| [#7](https://github.com/Thitronik01/Frank-Repo/issues/7) | Renault Master E-Tech 55/52 kWh | 303, 304 | offen: Bruttowerte nirgends belegt |
| [#8](https://github.com/Thitronik01/Frank-Repo/issues/8) | Mini Aceman vs. Cooper | 219, 221 | korrigiert (Cooper E und SE netto) – geschlossen am 2026-09-24 |
| [#9](https://github.com/Thitronik01/Frank-Repo/issues/9) | BMW iX: zu kleine Puffer | 65–70 | korrigiert (xDrive40, xDrive50, M60) – geschlossen am 2026-09-24 |
| [#10](https://github.com/Thitronik01/Frank-Repo/issues/10) | Puffer unter 1 %: ë-C3, ë-C3 Aircross, MG4 | 82–84, 205, 206, 208 | ë-C3 bestätigt, Aircross ER korrigiert; MG4: Quellen widersprechen – Entscheidung offen |
| [#11](https://github.com/Thitronik01/Frank-Repo/issues/11) | Mercedes eSprinter LFP: nur „ca.“-Bruttowerte | 192–194 | nicht klärbar: Hersteller nennt nur netto – Schätzung bleibt markiert |
| [#12](https://github.com/Thitronik01/Frank-Repo/issues/12) | Tesla: Nettowerte exakt 95 % des Bruttowerts | Tesla-Block | offen |
| [#13](https://github.com/Thitronik01/Frank-Repo/issues/13) | Renault Zoe: R90 Entry und R75 | 317, 318, 320 | geklärt: R75 nur mit Z.E. 40 (Zeile 317 entfernt), R90 Entry korrekt – geschlossen am 2026-09-24 |
| [#14](https://github.com/Thitronik01/Frank-Repo/issues/14) | Kleine Abweichungen bei baugleichen Batterien | siehe Issue | offen (Mini Cooper SE über #8 erledigt) |
| [#15](https://github.com/Thitronik01/Frank-Repo/issues/15) | Bezeichnungen: iX2 eDrive30, EQB 350, i5 M60 | 58, 74, 184 | korrigiert – geschlossen am 2026-09-24 |
| [#16](https://github.com/Thitronik01/Frank-Repo/issues/16) | Namensdubletten | 12 Zeilen | als Alias gekennzeichnet – bitte bestätigen |
| [#17](https://github.com/Thitronik01/Frank-Repo/issues/17) | Modelljahr / Batterie-Generation fehlt | ganze Tabelle | Spalten angelegt, für recherchierte Zeilen gefüllt – Rest offen |
| [#18](https://github.com/Thitronik01/Frank-Repo/issues/18) | Herausgeber und Stichtag der Rohdaten | – | offen |

## Schreibweisen

Vereinheitlicht auf die Herstellerschreibweise; der Originalname bleibt in der Spalte „Modell (Rohquelle)“ erhalten: Citroën, Mercedes-Benz, Škoda, SEAT; ë-C3, ë-C4, ë-Berlingo, ë-Jumpy, ë-SpaceTourer; Enyaq … Coupé; Citigo e iV; iX xDrive40 usw.; e-up!; ID. Buzz; EQC 400 4MATIC. Kapazitäten als Zahl mit Dezimalpunkt statt Text mit Einheit.

## Fachliche Hinweise je Fahrzeug

### [[audi-e-tron|Audi e-tron]]

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

### [[citroen-e-jumpy|Citroën ë-Jumpy Combi]]

- Der Puffer der 75-kWh-Batterie (68,0 kWh netto) ist mit rund 9 % größer als der der 50-kWh-Batterie (ca. 7 %).

### [[cupra-born|Cupra Born]]

- Zeilen 100 und 102 haben identische Batteriewerte; der Unterschied (e-boost) betrifft nur die Motorleistung.

### [[dacia-spring|Dacia Spring Electric]]

- Vier Zeilen mit identischen Kapazitätswerten – für die Batteriekapazität de facto Duplikate.
- Ob die Batterie beim Modell ab 2024 die Zellchemie gewechselt hat (NMC vs. LFP), ist nicht gesichert und wird hier bewusst nicht behauptet.

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

### [[mercedes-eqc|Mercedes-Benz EQC]]

- Bauzeit nicht sicher belegt (Marktstart 2019, Produktionsende ca. 2023/2024).

### [[mercedes-eqv|Mercedes-Benz EQV]]

- Runde Werte (66/60, 100/90 kWh) – vermutlich gerundete Herstellerangaben.

### [[mercedes-esprinter|Mercedes-Benz eSprinter]]

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

- Drei Zeilen mit identischer Bezeichnung „MG4 Electric“ – Unterscheidung nur über die Kapazität.

### [[mg5-electric|MG5 Electric]]

- Uneinheitliche Namensgebung „MG5 EV“ vs. „MG5 Electric“.
- Zellchemie der Standard-Range-Batterie (möglicherweise LFP) nicht gesichert und daher nicht behauptet.
- Die Einordnung als Geschwister des ZS EV bezieht sich auf die gemeinsame Konversionsbauweise und Antriebstechnik, nicht auf identische Batterien.

### [[mg-zs-ev|MG ZS EV]]

- Die Long-Range-Batterie (72,6 kWh brutto) hat denselben Bruttowert wie die erste Long-Range-Batterie des Hyundai IONIQ 5 – rein zufällige Übereinstimmung, kein technischer Zusammenhang.
- Zellchemie der Standard-Range-Batterie (möglicherweise LFP) nicht gesichert.

### [[mini-cooper-electric|Mini Cooper E / SE]]

- Cooper SE erscheint zweimal mit völlig unterschiedlichen Batterien (Zeilen 220 und 221) – zwei Fahrzeuggenerationen unter gleichem Namen.

### [[mini-countryman-electric|Mini Countryman E / SE]]

- Nettowert 64,6 kWh gegenüber 64,7 kWh bei iX1/iX2 mit identischer Batterie – Rundungsdifferenz.

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

- Die beim ë-Berlingo erfasste neuere 52-kWh-Batterie fehlt hier.

### [[peugeot-e-traveller|Peugeot e-Traveller]]

- Ob die Längenbezeichnungen L2/L3 mit einer Modellpflege eingeführt wurden, ist nicht gesichert.

### [[peugeot-ion|Peugeot iOn]]

- Je nach Baujahr werden für i-MiEV/C-Zero/iOn sowohl 16 kWh als auch 14,5 kWh als Gesamtkapazität genannt; möglicherweise ist 14,5 kWh eine spätere Bruttokapazität statt eines Nettowerts.

### [[peugeot-partner-tepee-electric|Peugeot Partner Tepee Electric]]

- Bauzeit nicht sicher bekannt, daher null.
- Die Konversion erfolgte nach verbreiteten Angaben in Zusammenarbeit mit einem externen Partner; Details nicht gesichert.

### [[porsche-macan-electric|Porsche Macan (Elektro)]]

- Die Audi-Schwester Q6 e-tron ist mit 100/94,9 kWh gelistet, der Macan mit 100/95 kWh – Rundungsdifferenz bei vermutlich gleicher Batterie.

### [[porsche-taycan|Porsche Taycan]]

- Die Batteriebezeichnungen (Performancebatterie/Performancebatterie Plus) stehen nicht in den Rohdaten; die Zuordnung erfolgt über die Kapazität.

### [[renault-city-k-ze|Renault City K-ZE]]

- Bauzeit nicht sicher bekannt, daher null.

### [[renault-kangoo-electric|Renault Kangoo Z.E. / E-Tech]]

- Unter einem Slug sind zwei Fahrzeuggenerationen (Kangoo Z.E. und Kangoo E-Tech) zusammengefasst.
- Für den Kangoo Z.E. mit kleiner Batterie findet man 22 kWh teils als Brutto-, teils als Nettoangabe.

### [[renault-master-electric|Renault Master Z.E. / E-Tech]]

- Zwei Generationen unter einem Slug zusammengefasst.
- Die Batterie des Master Z.E. (33/31 kWh) hat dieselben Werte wie der Kangoo Z.E. mit großer Batterie; eine technische Identität wird hier nicht behauptet.

### [[renault-scenic-e-tech|Renault Scenic E-Tech]]

- Weitere AmpR-Medium-Modelle (Renault Megane E-Tech, Nissan Ariya) sind in families.json nicht enthalten.
- Die Werte der großen Batterie (92/87 kWh) stimmen mit dem Renault Master E-Tech überein.

### [[renault-twingo-electric|Renault Twingo Electric]]

- Kleiner Puffer (22 vs. 21,3 kWh); in manchen Quellen wird 22 kWh als nutzbare Kapazität angegeben.
- Das Schwestermodell Smart ForFour EQ ist nicht in families.json enthalten.

### [[renault-zoe|Renault Zoe]]

- Die erste Batteriegeneration wird im Handel als „22 kWh“ bezeichnet, in den Rohdaten aber mit 25,9 kWh brutto / 23,3 kWh netto geführt.
- Die Bedeutung der Zahl in den Motorbezeichnungen (Reichweite vs. Leistung) ist je nach Generation unterschiedlich; hier nur grob beschrieben.

### [[seat-mii-electric|Seat Mii electric]]

- Bauzeit offen gelassen: Markteinführung um 2019/2020, genaues Produktionsende nicht sicher belegt.

### [[skoda-citigo-e-iv|Škoda Citigo e iV]]

- Bauzeit offen gelassen, da genaue Produktionsdaten nicht sicher sind (Markteinführung um 2019/2020, nur kurze Bauzeit).

### [[skoda-enyaq|Škoda Enyaq]]

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
