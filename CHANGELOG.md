# Changelog

## 1.1.0

Fork van [mvn23/hwam_stove](https://github.com/mvn23/hwam_stove) door [@peterlindeman](https://github.com/peterlindeman), bijgewerkt voor Home Assistant 2026.06.

### Wijzigingen

- **Fix: kacheldatum crasht bij maand/dag = 0** — de kachelfirmware stuurt maanden als 0-gebaseerd (0–11) en stuurt dag/maand `0` als de klok nooit gesynchroniseerd is. pystove gaf deze waarden onbewerkt door aan Python's `datetime()`, wat crashte. Opgelost door pystove te vendoren (meeleveren in de integratie) met de fix toegepast.
- **Fix: `CONF_MONITORED_VARIABLES` verwijderd uit `homeassistant.const`** — dit constant bestaat niet meer in recente HA-versies. Nu lokaal gedefinieerd in de integratie (alleen nog gebruikt voor de verouderde YAML-configuratie).
- **Fix: config flow stapnaam `init` → `user`** — HA vereist `step_id="user"` als startpunt voor de GUI-installatie. De vorige naam `init` werkte niet via de UI.
- **Bijgewerkt: `hacs.json`** — bijgewerkt voor HACS v2 compatibiliteit.
- **Bijgewerkt: `manifest.json`** — minimale HA versie toegevoegd (`2024.1.0`).
- **Bijgewerkt: vertalingen** — stapnaam in `en.json`, `nl.json` en `de.json` bijgewerkt naar `user`, inclusief titel en beschrijving voor de installatiepagina.

## 1.0.0b2

- Add german translation (thanks @UDicke) (#46)
- Pin pystove version (#45)

## 1.0.0b1

- Remove services.yaml (#43)
- Add dutch translation (thanks @Schrikt) (#42)
- Update README.md
- Remove obsolete constants (#41)
- Improve component setup (#40)
- Support config entry unloading (#39)
- Update value when adding entities to Home Assistant (#38)
- Update sensor descriptions (#37)
- Update English language file (#36)
- Update entity descriptions
- Increase time between updates when stove is in standby mode (#31)

## 1.0.0b0

- Complete overhaul from 0.0.1
