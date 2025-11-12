# Spin the Wheel 🛞

En enkel og pen Python GUI-applikasjon for å trekke tilfeldig blant elever/medlemmer ved hjelp av et visuelt "lykkehjul".
Denne README-en er skrevet for å ligge på GitHub — den forklarer funksjoner, hvordan du kjører programmet og hvordan du kan bidra.

## Høydepunkter

- Pen GUI basert på CustomTkinter (mørkt tema).
- Roterende lykkehjul med tekst på hver seksjon.
- Ikke-blokkerende, jevn animasjon ved spinning (ease-out).
- Konfetti-animasjon når vinneren er valgt.
- Administrasjon av klasser / lister av navn (lagre/last som JSON i `klasser/`).
- Enkelt å pakke til en exe (det finnes en `EXE/bygg exe/` med hjelpe-batfiler i repoen).

## Skjermbilder

Se `screenshot.png` eller ta skjermdump fra programmet og legg i repoet for visning på GitHub (ikke inkludert i dette repo-klippet).

## Funksjoner (kort)

- `SPINN HJULET` — starter en jevn, ikke-blokkerende rotasjon og velger en vinner.
- `Administrer klasser` — åpner et vindu for å opprette, lagre, laste og slette klasser (lagres som JSON i `klasser/`).
- `Tilbakestill hjulet` — gjenoppretter navnene fra lagret klasse.
- Listevisning til venstre for rask oversikt over navn på hjulet.

## Filstruktur (viktigste filer)

- `Nyeste versjon/spinthewheel.py` — hovedapplikasjonen (GUI).
- `EXE/bygg exe/bygg exe.bat` — hjelpe-skript for å lage en kjørbar (eks. med PyInstaller).
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

## Hvordan bruke

1. Velg eller opprett en klasse i `Administrer klasser`.
2. Legg til navn og lagre. Filen lagres i `klasser/` som en JSON-liste.
3. Velg klassen fra toppmenyen — navnene vises i venstre kolonne og på hjulet.
4. Trykk `SPINN HJULET` for å starte animasjonen og velge en vinner.

## Tips / Vanlige problemer

- Popup-vindu og oppgavelinje: Hvis du opplever at admin-vinduet vises delvis under Windows oppgavelinje (taskbar), bruk mellombar løsning: maksimer eller flytt hovedvinduet før du åpner admin-vinduet, eller bruk prosjektets `klasse_admin_vindu` (som standard sentrerer vinduet på skjermen for å unngå dette problemet).
- Hvis animasjonen hakker: prøv å kjøre på en maskin uten tung bakgrunnsprosess, eller reduser `canvas_size` i koden for mindre pikselarbeid.

## Pakk som kjørbar (.exe)

Eksempel med PyInstaller (anbefales å bruke en virtuell env):

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile "Nyeste versjon\spinthewheel.py"
```

Merk: det finnes allerede en `EXE/bygg exe/bygg exe.bat` i repoen som kan brukes som utgangspunkt.

## Utvikling og bidrag

Alle bidrag er velkomne. Forslag til forbedringer:

- Trekke ut klasse-administrasjonslogikk til egen modul for enklere testing.
- Legge til mulighet for differentierte vekter (sannsynlighet) per navn.
- Eksport/import av klasser via UI.

Hvordan bidra:

1. Fork repoet
2. Lag feature-branch
3. Opprett PR med beskrivelse av endringene

## Lisens

Velg en lisens for prosjektet (f.eks. MIT) og legg til en `LICENSE`-fil hvis du vil gjøre koden åpen for andre.

## Kontakt

For spørsmål eller hjelp: legg igjen en issue i repoet.

----

Hvis du vil, kan jeg også:
- Lage en kort `CONTRIBUTING.md` med retningslinjer for PRs.
- Legge til en pen `README`-screenshot og en `LICENSE`-fil (f.eks. MIT).

Sier du til hvilke av disse du vil ha, så legger jeg dem til også.