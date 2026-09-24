---
type: "concept"
updated: "2026-09-24"
sources: 0
tags: ["fachbegriff", "batterie", "elektronik"]
---

# Batteriemanagementsystem (BMS)

**Kurzdefinition:** Elektronik und Software, die jede Zelle der Traktionsbatterie überwacht, schützt und den Ladezustand berechnet.

## Erläuterung

Das BMS misst laufend Spannung, Strom und Temperatur der Zellen bzw. Zellblöcke. Daraus berechnet es den Ladezustand ([[state-of-charge]]) und schätzt den Gesundheitszustand ([[state-of-health]]). Es verhindert Über- und Tiefentladung, begrenzt die Lade- und Entladeleistung bei Kälte oder Hitze, gleicht Spannungsunterschiede zwischen Zellen aus (*Balancing*) und steuert das Thermomanagement.

Das BMS legt auch fest, wie viel der [[bruttokapazitaet]] nutzbar ist ([[batteriepuffer]], [[software-lock]]).

Ein [[batteriecheck]] liest in der Regel Daten aus dem BMS über die Diagnoseschnittstelle (OBD) aus oder wertet einen kontrollierten Lade- bzw. Entladevorgang aus.

## Verwandte Begriffe

- [[state-of-charge|State of Charge (SoC)]] — Der aktuelle Ladezustand der Batterie in Prozent der Nettokapazität – die „Tankanzeige“.
- [[state-of-health|State of Health (SoH)]] — Gesundheitszustand der Batterie: verbleibende Kapazität im Verhältnis zur Neu-Kapazität, in Prozent.
- [[batteriecheck|Batteriecheck (Batteriezertifikat)]] — Standardisierte Prüfung des Gesundheitszustands der Traktionsbatterie, meist für den Gebrauchtwagenhandel.

## Belege

- Begriffserklärung: allgemeines Fachwissen des LLM (Stand 2026-09-24), keine Rohquelle im Bestand.
