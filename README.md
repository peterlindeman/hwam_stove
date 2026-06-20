# HWAM Smart Stove — Home Assistant integratie

Fork van [mvn23/hwam_stove](https://github.com/mvn23/hwam_stove), bijgewerkt voor **Home Assistant 2026.06**.

De `hwam_stove` integratie laat je een [HWAM kachel met Smartcontrol](http://www.hwam.com/) bedienen vanuit Home Assistant.

## Installatie via HACS

1. Ga naar **HACS → Integraties → ⋮ → Aangepaste repositories**
2. Voeg toe: `https://github.com/peterlindeman/hwam_stove` — categorie **Integration**
3. Zoek op "HWAM", klik **Download**
4. Herstart Home Assistant
5. Ga naar **Instellingen → Apparaten & Diensten → + Integratie toevoegen → HWAM Smart Stove**
6. Vul de naam en het IP-adres van de kachel in

Of gebruik de knop hieronder na installatie:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hwam_stove)

## Wijzigingen t.o.v. het origineel

Deze fork bevat de volgende fixes voor HA 2026.06:

### pystove: 0-gebaseerde maand/dag crash
De kachelfirmware stuurt maanden als 0–11 (0 = januari) en stuurt `0` voor dag en maand als de klok nooit gesynchroniseerd is. pystove gaf deze waarden direct door aan Python's `datetime()`, wat een `ValueError` veroorzaakte en de integratie liet crashen bij elke update. Opgelost door pystove mee te leveren in de integratie (vendoring) met de fix toegepast. De gefixte pystove broncode staat ook in [peterlindeman/pystove](https://github.com/peterlindeman/pystove).

### `CONF_MONITORED_VARIABLES` verwijderd uit HA
Dit constant is verwijderd uit `homeassistant.const` in recente HA-versies. De import werd vervangen door een lokale definitie (alleen nog relevant voor de verouderde YAML-configuratie, die al als deprecated wordt aangegeven).

### Config flow stap `init` → `user`
HA vereist dat de eerste stap in een config flow `step_id="user"` heet. De vorige naam `init` zorgde ervoor dat HA de integratie niet als GUI-configureerbaar herkende.

### HACS v2 en manifest
`hacs.json` en `manifest.json` bijgewerkt voor compatibiliteit met HACS v2 en moderne HA-versies.

## Klok synchroniseren

Als de kachel zijn klok nog nooit gesynchroniseerd heeft (typisch bij eerste ingebruikname), verschijnen datum/tijd entiteiten als `onbekend`. Gebruik de **"Synchronize clock"** knop in de integratie om de kacheltijd gelijk te zetten met Home Assistant.
