---
type: "synthesis"
updated: "2026-09-23"
tags: ["analyse", "batteriepuffer"]
---

# Puffer-Analyse: Brutto vs. Netto

**Anlass:** Auswertung aller 468 plausiblen Varianten aus [[tn-batterycheck-alle-daten]] · Stand 2026-09-23

## Stand

Der [[batteriepuffer]] (Brutto − Netto, relativ zur [[bruttokapazitaet]]) liegt im Bestand im **Median bei 6,1 %**, im Mittel bei 6,6 %. Die Spanne reicht von 0,4 % bis 18,2 %. Eine Variante mit negativem Puffer (netto > brutto) ist ausgeschlossen und in [[datenqualitaet]] dokumentiert.

Muster, die sich zeigen:

- **Sehr kleine Puffer (< 2 %)** treten vor allem bei [[lfp-zellchemie|LFP]]-Batterien und bei Herstellern auf, die offenbar den nutzbaren Wert nahe am Brutto angeben (z. B. [[citroen-e-c3]], [[mg4-electric]] 51 kWh). Solche Werte sollten vor einem [[batteriecheck]] besonders geprüft werden.
- **Große Puffer (> 12 %)** finden sich bei frühen Konstruktionen ([[bmw-i3]] mit 33,2 kWh, [[vw-e-golf]]), bei den 41-kWh-Transportern von Mercedes ([[mercedes-evito]], [[mercedes-esprinter]]), bei [[software-lock|softwarebegrenzten]] Batterien (Tesla Model S/X 60) und bei der ersten MEB-Einstiegsbatterie (VW ID.3 Pure 55 → 45 kWh laut Quelle – Bruttowert fraglich, siehe [[datenqualitaet]]).
- **Plattform-Geschwister** haben identische Puffer – siehe [[plattform-geschwister]].

## Verteilung

| Puffer | Varianten | |
|---|---|---|
| 0–2 % | 5 | █ |
| 2–4 % | 73 | ██████████████████ |
| 4–6 % | 130 | ████████████████████████████████ |
| 6–8 % | 159 | ████████████████████████████████████████ |
| 8–10 % | 35 | █████████ |
| 10–12 % | 42 | ██████████ |
| 12–15 % | 14 | ████ |
| ≥ 15 % | 10 | ██ |

## Nach Hersteller

| Hersteller | Varianten | Puffer Median | Min | Max |
|---|---|---|---|---|
| [[volvo\|Volvo]] | 22 | 3,7 % | 2,9 % | 4,3 % |
| [[bmw\|BMW]] | 34 | 3,8 % | 1,9 % | 18,1 % |
| [[mg\|MG]] | 15 | 4,5 % | 0,4 % | 8,5 % |
| [[hyundai\|Hyundai]] | 25 | 4,8 % | 3,6 % | 8,2 % |
| [[kia\|Kia]] | 27 | 4,8 % | 3,8 % | 11,5 % |
| [[tesla\|Tesla]] | 63 | 5,0 % | 3,3 % | 17,3 % |
| [[mercedes\|Mercedes-Benz]] | 25 | 5,9 % | 4,6 % | 14,6 % |
| [[cupra\|Cupra]] | 5 | 6,1 % | 6,1 % | 6,5 % |
| [[skoda\|Škoda]] | 23 | 6,1 % | 5,5 % | 12,2 % |
| [[volkswagen\|Volkswagen]] | 41 | 6,1 % | 5,5 % | 18,2 % |
| [[audi\|Audi]] | 40 | 6,6 % | 5,1 % | 12,0 % |
| [[dacia\|Dacia]] | 4 | 6,7 % | 6,7 % | 6,7 % |
| [[renault\|Renault]] | 24 | 7,0 % | 3,2 % | 10,7 % |
| [[citroen\|Citroën]] | 23 | 7,4 % | 0,5 % | 9,4 % |
| [[peugeot\|Peugeot]] | 32 | 7,4 % | 4,1 % | 9,4 % |
| [[porsche\|Porsche]] | 41 | 7,6 % | 5,0 % | 10,4 % |
| [[ford\|Ford]] | 15 | 7,8 % | 6,9 % | 10,9 % |
| [[mini\|Mini]] | 8 | 9,2 % | 2,9 % | 11,3 % |
| [[seat\|SEAT]] | 1 | 12,2 % | 12,2 % | 12,2 % |

## Größte Puffer

| Fahrzeug | Variante | Brutto | Netto | Puffer |
|---|---|---|---|---|
| [[vw-id-3\|VW ID.3]] | ID.3 Pure | 55 kWh | 45,0 kWh | 18,2 % |
| [[vw-id-3\|VW ID.3]] | ID.3 Pure Performance | 55 kWh | 45,0 kWh | 18,2 % |
| [[bmw-i3\|BMW i3]] | i3 | 33,2 kWh | 27,2 kWh | 18,1 % |
| [[bmw-i3\|BMW i3]] | i3 (Range Extender) | 33,2 kWh | 27,2 kWh | 18,1 % |
| [[bmw-i3\|BMW i3]] | i3s | 33,2 kWh | 27,2 kWh | 18,1 % |
| [[bmw-i3\|BMW i3]] | i3s (Range Extender) | 33,2 kWh | 27,2 kWh | 18,1 % |
| [[tesla-model-s\|Tesla Model S]] | Model S 60 | 75 kWh | 62,0 kWh | 17,3 % |
| [[tesla-model-s\|Tesla Model S]] | Model S 60D | 75 kWh | 62,0 kWh | 17,3 % |
| [[tesla-model-s\|Tesla Model S]] | Model S P60 | 75 kWh | 62,0 kWh | 17,3 % |
| [[tesla-model-x\|Tesla Model X]] | Model X 60D | 75 kWh | 62,0 kWh | 17,3 % |
| [[mercedes-esprinter\|Mercedes-Benz eSprinter]] | eSprinter | 41 kWh | 35,0 kWh | 14,6 % |
| [[mercedes-evito\|Mercedes-Benz eVito]] | eVito extra long | 41 kWh | 35,0 kWh | 14,6 % |

## Kleinste Puffer

| Fahrzeug | Variante | Brutto | Netto | Puffer |
|---|---|---|---|---|
| [[mg4-electric\|MG4 Electric]] | MG4 Electric | 51,0 kWh | 50,8 kWh | 0,4 % |
| [[citroen-e-c3\|Citroën ë-C3]] | e-C3 | 44 kWh | 43,8 kWh | 0,5 % |
| [[citroen-e-c3-aircross\|Citroën ë-C3 Aircross]] | e-C3 Aircross | 44 kWh | 43,8 kWh | 0,5 % |
| [[citroen-e-c3-aircross\|Citroën ë-C3 Aircross]] | e-C3 Aircross Extended Range | 54 kWh | 53,5 kWh | 0,9 % |
| [[bmw-ix\|BMW iX]] | iX xDrive 50 | 111,5 kWh | 109,4 kWh | 1,9 % |
| [[bmw-ix\|BMW iX]] | iX xDrive 60 | 111,5 kWh | 109,1 kWh | 2,2 % |
| [[bmw-ix\|BMW iX]] | iX M70 | 111,5 kWh | 108,9 kWh | 2,3 % |
| [[bmw-ix1\|BMW iX1]] | iX1 eDrive20 | 66,5 kWh | 64,7 kWh | 2,7 % |
| [[bmw-ix1\|BMW iX1]] | iX1 xDrive30 | 66,5 kWh | 64,7 kWh | 2,7 % |
| [[bmw-ix2\|BMW iX2]] | iX2 eDrive20 | 66,5 kWh | 64,7 kWh | 2,7 % |
| [[bmw-ix2\|BMW iX2]] | iX2 eDrive30 | 66,5 kWh | 64,7 kWh | 2,7 % |
| [[mini-countryman-electric\|Mini Countryman E / SE]] | Countryman E | 66,5 kWh | 64,6 kWh | 2,9 % |

## Belastbarkeit

- **Gut belegt:** Die Werte selbst stammen aus einer Quelle ([[tn-batterycheck-alle-daten]]), die intern abgeglichen ist (Blatt „Übersicht“: alle Marken „OK“).
- **Dünn:** Es gibt nur diese eine Quelle. Herstellerangaben und unabhängige Messungen fehlen als Gegenprobe.
- **Strittig:** Sehr kleine Puffer (< 1 %) und die in [[datenqualitaet]] gelisteten Zeilen.

## Was fehlt

- Herstellerdatenblätter oder eine zweite Datenbank (z. B. EV-Database) als Abgleich
- Modelljahr/Batterie-Generation je Zeile – ohne sie sind gleichnamige Varianten mit verschiedenen Werten nicht eindeutig zuzuordnen
