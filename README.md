Downloads Sorter
================

Dieses Repository enthält ein kleines Werkzeug, das den `Downloads`-Ordner organisiert:

- `sort.py` — Python-Skript, das Dateien nach Dateityp in Zielordner verschiebt.
- `sort.bat` — Starter-Batch für Windows: doppelklick führt `sort.py` aus.

Zielordner (innerhalb von `Downloads`): `Videos`, `Bilder`, `Dokumente`, `Archive`, `Musik`.

Sicherheit & Privatsphäre
-------------------------
Dieses Projekt enthält keine Passwörter, API‑Keys oder personenbezogene Pfade. Beispielpfade wurden durch `%USERPROFILE%\Downloads` ersetzt.

Benutzung
--------
- Dry-run (zeigt Aktionen, führt aber nichts aus):

```powershell
py -3 "%USERPROFILE%\Downloads\sort.py" --dry-run
```

- Echt ausführen:

```powershell
py -3 "%USERPROFILE%\Downloads\sort.py"
```

- Doppelklick: öffne den Ordner mit `sort.bat` und doppelklicke darauf.

Automatisch beim Anmelden
-------------------------
- Lege eine Verknüpfung zu `sort.bat` in `shell:startup` (Windows) ab, oder erstelle einen Task im Task Scheduler, der beim Anmelden `py -3 "%USERPROFILE%\Downloads\sort.py"` ausführt.
