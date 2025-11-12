# Spin the Wheel 🛞

En enkel og pen Python GUI-applikasjon for å trekke tilfeldig blant elever/medlemmer ved hjelp av et visuelt "lykkehjul".
Denne README-en er skrevet for å ligge på GitHub — den forklarer funksjoner, hvordan du kjører programmet og hvordan du kan bidra.

## Høydepunkter

- Pen GUI basert på CustomTkinter (mørkt tema).
- Roterende lykkehjul med tekst på hver seksjon.
- Ikke-blokkerende, jevn animasjon ved spinning (ease-out).
- Konfetti-animasjon når vinneren er valgt.
- Administrasjon av klasser / lister av navn (lagre/last som JSON i `klasser/`).

## Funksjoner (kort)

- `SPINN HJULET` — starter en jevn, ikke-blokkerende rotasjon og velger en vinner.
- `Administrer klasser` — åpner et vindu for å opprette, lagre, laste og slette klasser (lagres som JSON i `klasser/`).
- `Tilbakestill hjulet` — gjenoppretter navnene fra lagret klasse.
- Listevisning til venstre for rask oversikt over navn på hjulet.

## Filstruktur (viktigste filer)

- `Nyeste versjon/spinthewheel.py` — hovedapplikasjonen (GUI).
- `klasser/` — mappe hvor hver klasse lagres som `Klassenavn.json`.

## Krav

- Python 3.8+
- pip
- Avhengigheter (installeres automatisk ved første kjøring av skriptet):
  - `customtkinter`

## Installering (lokalt, Windows PowerShell)

Åpne PowerShell i prosjektmappen og kjør (valgfritt, men anbefalt i et virtuelt miljø):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install customtkinter
```

Kjør programmet:

```powershell
python "Nyeste versjon\spinthewheel.py"
```

Alternativt (Windows) kan du dobbeltklikke på `start spinthewheel.bat` som ligger i `Nyeste versjon/` for å starte programmet uten å åpne kommandolinjen.

## Hvordan bruke

1. Velg eller opprett en klasse i `Administrer klasser`.
2. Legg til navn og lagre. Filen lagres i `klasser/` som en JSON-liste.
3. Velg klassen fra toppmenyen — navnene vises i venstre kolonne og på hjulet.
4. Trykk `SPINN HJULET` for å starte animasjonen og velge en vinner.

## Tips / Vanlige problemer

- Popup-vindu og oppgavelinje: Hvis du opplever at admin-vinduet vises delvis under Windows oppgavelinje (taskbar), bruk mellombar løsning: maksimer eller flytt hovedvinduet før du åpner admin-vinduet, eller bruk prosjektets `klasse_admin_vindu` (som standard sentrerer vinduet på skjermen for å unngå dette problemet).
- Hvis animasjonen hakker: prøv å kjøre på en maskin uten tung bakgrunnsprosess, eller reduser `canvas_size` i koden for mindre pikselarbeid.


