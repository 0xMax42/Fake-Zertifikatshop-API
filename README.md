# Fake-Zertifikatshop API

### Von
- [Gespensterkind](https://github.com/gespensterkind)
- [0xMax42](https://github.com/0xMax42)

### Voraussetzungen

* Python 3.12 oder neuer
* [Poetry](https://python-poetry.org/docs/#installation) installiert
* Optional: Docker (für Containerbetrieb)

---

### 1. Projekt lokal einrichten

```bash
# Projektverzeichnis wechseln
cd <pfad-zum-projekt>

# Abhängigkeiten installieren und virtuelle Umgebung erzeugen
poetry install

# In die virtuelle Umgebung wechseln (Poetry aktiviert automatisch die venv beim Ausführen von Befehlen)
poetry shell
```

Alternativ, wenn du Poetry nicht dauerhaft ins Shell-Env laden willst, kannst du alle Befehle mit `poetry run` präfixen:

```bash
poetry run python ...
poetry run pytest
```

---

### 2. Server starten

**Entwicklung (mit automatischem Reload):**

```bash
poetry run task serve
```

**Produktion (mit fester IP und Port):**

```bash
poetry run task serve_prod
```

---

### 3. Datenbank initialisieren und Seed-Daten laden

```bash
# Datenbank initialisieren:
poetry run task init-db

# Seed-Daten einspielen:
poetry run task seed
```

---

### 4. Tests ausführen

```bash
poetry run task test
```

Warnungen (z. B. DeprecationWarnings) werden dabei ignoriert.

---

### 5. Docker-Variante bauen und starten

**Image bauen:**

```bash
docker build -t Fake-Zertifikatshop-API .
```

**Container starten (wird nach dem Stoppen automatisch gelöscht):**

```bash
docker run --rm -it -p 8000:8000 Fake-Zertifikatshop-API
```

Die API ist dann unter [http://localhost:8000](http://localhost:8000) erreichbar.

> **Hinweis:** Beim Starten des Containers können die Umgebungsvariablen `VALID_USERNAME` und `VALID_PASSWORD` gesetzt werden, um die Zugangsdaten für das Admin-Panel zu konfigurieren. Beispiel:

```bash
docker run --rm -it -p 8000:8000 -e VALID_USERNAME=admin -e VALID_PASSWORD=secret Fake-Zertifikatshop-API
```

---

### 6. Changelog generieren (optional)

```bash
poetry run task changelog
```

Dies verwendet `git-cliff` und schreibt in `CHANGELOG.md`.

**Installation von git-cliff:**

```bash
# Mit Cargo (falls Rust installiert ist)
cargo install git-cliff

# Alternativ: als vorgefertigtes Binary herunterladen
wget https://github.com/orhun/git-cliff/releases/latest/download/git-cliff-x86_64-unknown-linux-gnu.tar.gz
# Entpacken und z. B. nach /usr/local/bin verschieben
```

Weitere Infos: [https://github.com/orhun/git-cliff](https://github.com/orhun/git-cliff)

---