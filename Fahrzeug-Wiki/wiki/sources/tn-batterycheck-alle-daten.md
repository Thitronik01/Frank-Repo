---
type: "source"
updated: "2026-09-24"
tags: ["rohquelle", "tabelle", "batteriekapazitaet"]
---

# TN Batterycheck – alle Daten (Excel)

**Herausgeber:** nicht angegeben · **Eingang:** 2026-09-23 · **Art:** Tabelle (xlsx, 2 Blätter)
**Raw:** `raw/tn_batterycheck_alle_daten.xlsx`

## Kernaussagen

- Referenztabelle mit **Brutto- und Nettokapazität** der [[traktionsbatterie]] für **467 Fahrzeugvarianten** von **19 Herstellern**.
- Die Varianten lassen sich zu **90 Modellreihen** zusammenfassen – jede hat in diesem Wiki eine eigene Seite.
- Zweck ist offenbar ein [[batteriecheck]]: Die [[nettokapazitaet]] ist der Referenzwert, gegen den der [[state-of-health]] einer gebrauchten Batterie gerechnet wird.
- Das Blatt „Übersicht“ belegt einen internen Abgleich: extrahierte Zeilen = Zeilen laut Quellangabe, für alle Marken „OK“.
- Einzelne Zeilen sind fehlerhaft oder doppelt. Das Wiki nutzt deshalb eine **bereinigte Fassung** (`data/tn_batterycheck_bereinigt.xlsx`); alle Änderungen mit Beleg stehen in [[datenqualitaet]].

## Aufbau

| Blatt | Inhalt |
|---|---|
| Fahrzeuge | 469 Zeilen: Marke, Modell, Kapazität brutto, Kapazität netto (Text mit Einheit „kWh“, Dezimalpunkt) |
| Übersicht | je Marke: extrahierte Zeilen, Quellangabe, Abgleich (alle „OK“), Summe 469 |

## Zeilen je Hersteller

| Hersteller | Varianten | Modellreihen |
|---|---|---|
| [[tesla\|Tesla]] | 63 | 4 |
| [[volkswagen\|Volkswagen]] | 41 | 7 |
| [[audi\|Audi]] | 40 | 5 |
| [[porsche\|Porsche]] | 40 | 2 |
| [[bmw\|BMW]] | 34 | 8 |
| [[peugeot\|Peugeot]] | 32 | 11 |
| [[kia\|Kia]] | 27 | 6 |
| [[hyundai\|Hyundai]] | 25 | 6 |
| [[mercedes\|Mercedes-Benz]] | 25 | 7 |
| [[citroen\|Citroën]] | 23 | 8 |
| [[renault\|Renault]] | 23 | 6 |
| [[skoda\|Škoda]] | 23 | 3 |
| [[volvo\|Volvo]] | 22 | 3 |
| [[ford\|Ford]] | 15 | 2 |
| [[mg\|MG]] | 15 | 5 |
| [[mini\|Mini]] | 8 | 3 |
| [[cupra\|Cupra]] | 6 | 2 |
| [[dacia\|Dacia]] | 4 | 1 |
| [[seat\|SEAT]] | 1 | 1 |

## Zusammenfassung

Die Tabelle deckt praktisch den gesamten europäischen Elektroauto-Markt von 2011 (Mitsubishi-i-MiEV-Ableger [[citroen-c-zero]], [[peugeot-ion]]) bis 2025 ab, vom Kleinstwagen mit 16 kWh bis zum Pick-up [[ford-f-150-lightning]] mit 143,4 kWh brutto. Tesla (63), Porsche (41), Volkswagen (41) und Audi (40) sind am stärksten vertreten – bei Porsche vor allem, weil jede Taycan-Karosserie und Leistungsstufe einzeln mit beiden Batteriegenerationen gelistet ist.

Es fehlt eine Angabe zu Modelljahr oder Batterie-Generation. Deshalb erscheinen gleichnamige Varianten mehrfach mit unterschiedlichen Werten (z. B. Audi e-tron 55 quattro mit drei Nettowerten, Hyundai IONIQ 5 Long Range mit 72,6 und 77,4 kWh). Für einen [[batteriecheck]] muss die Generation also aus anderen Fahrzeugdaten bestimmt werden. Die Werte sind in sich weitgehend plausibel; Ausreißer sind in [[datenqualitaet]] gesammelt.

## Berührte Seiten

- Alle 90 Fahrzeugseiten — Kapazitätstabellen (siehe [[fahrzeuguebersicht]])
- Alle 19 Herstellerseiten — Kennzahlen je Marke
- [[bruttokapazitaet]], [[nettokapazitaet]], [[batteriepuffer]], [[software-lock]], [[lfp-zellchemie]], [[plattform-geschwister]] — Zahlenbeispiele
- [[puffer-analyse]], [[datenqualitaet]] — Auswertungen

## Widersprüche und Spannungen

- Cupra Born Zeile 99: netto (60 kWh) > brutto (53 kWh) — widerspricht der Definition in [[nettokapazitaet]].
- [[mercedes-eqt]] (50/45 kWh) vs. baugleicher [[renault-kangoo-electric|Renault Kangoo E-Tech]] (48/45 kWh) — gleiche Batterie, verschiedene Bruttowerte.
- [[renault-city-k-ze]] (30/26,8 kWh) vs. baugleicher [[dacia-spring]] (26,8/25 kWh).
- Auflösung dieser und weiterer Befunde (Stand 2026-09-24): [[datenqualitaet]].

## Offene Fragen

- Wer ist der Herausgeber (Präfix „tn“)? Aus welcher Primärquelle stammen die Werte (Herstellerangaben, eigene Messungen, Datenbank)?
- Stichtag der Daten? Neueste Modelle (Kia EV4, Hyundai IONIQ 9, Škoda Elroq) deuten auf Stand 2025 hin.
- Sind die Tesla-Nettowerte gemessen oder berechnet? Viele liegen exakt bei 95 % des Bruttowerts.
