# Project Atlas – Codex Rebuild Plan

## Doel

Project Atlas wordt opnieuw opgebouwd met Codex, sprint voor sprint, op een schone rebuild-branch.

De huidige versie blijft bewaard als referentie en backup.

## Belangrijke regels

- Eén sprint tegelijk.
- Eén duidelijke wijziging per taak.
- Eerst backend werkend, daarna dashboard.
- Eerst testen, daarna committen.
- Bij fouten eerst logs analyseren.
- Geen secrets of `.env` committen.
- Geen grote refactors zonder voorstel.
- Architectuur gaat vóór snelheid.
- Huidige project mag als referentie worden gebruikt, maar niet blind gekopieerd.

## Branch-strategie

### Backup huidige versie

```bash
git branch backup/current-atlas
git push origin backup/current-atlas