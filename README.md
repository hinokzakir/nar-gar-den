# Busstider Ålidhem Centrum

Ett Python-script som hämtar realtidsinformation om busstider från Ålidhem Centrum i Umeå via Trafiklab API.

## Krav

- Python 3.8 eller högre
- Trafiklab API-nyckel
- Internetanslutning

## Installation

1. Klona detta repository
2. Installera nödvändiga paket:
```bash
pip install -r requirements.txt
```

3. Skapa en `.env` fil i projektets rotmapp med din Trafiklab API-nyckel:
```
TRAFIKLAB_API_KEY=din_api_nyckel_här
```

## Användning

Kör scriptet:
```bash
python bus_times.py
```

Scriptet kommer att:
- Hämta aktuella avgångar från Ålidhem Centrum
- Spara informationen i en JSON-fil med tidsstämpel
- Skapa en loggfil (bus_times.log) med information om körningen

## Utdata

Scriptet skapar JSON-filer med följande namnkonvention:
`avgångar_ÅÅÅÅMMDD_TTMM.json`

Varje fil innehåller:
- Hållplatsnamn
- Tidpunkt för hämtning
- Lista med avgångar inklusive:
  - Linjenummer
  - Destination
  - Avgångstid
  - Spår
  - Realtidsinformation
  - Inställda avgångar

## Loggning

Scriptet loggar alla operationer till både:
- Konsolutskrift
- `bus_times.log` fil

## Obs

Detta script använder Trafiklab API. Vänligen respektera deras användarvillkor och gränser. 