# Book API mit Flask

Dieses Lernprojekt implementiert eine RESTful-API für eine Büchersammlung. Es zeigt den vollständigen Weg von einfachen Flask-Routen bis zu CRUD-Operationen, Validierung, Fehlerbehandlung, Filterung, Paginierung, Ratenbegrenzung und Logging.

## Sinn und Zweck

Die Anwendung demonstriert, wie Clients strukturierte JSON-Daten über HTTP abrufen und verändern können. Dabei werden robuste API-Grundlagen praktisch umgesetzt: passende HTTP-Methoden und Statuscodes, kontrollierte Eingaben, verständliche Fehlermeldungen, skalierbare Ergebnislisten und Schutz vor zu vielen Anfragen.

## Installation und Start

```bash
pip install -r requirements.txt
python3 app.py
```

Die API läuft anschließend unter `http://127.0.0.1:5000`.

## Endpunkte

| Methode | Route | Beschreibung |
| --- | --- | --- |
| `GET` | `/api/books` | Bücher abrufen; unterstützt `author`, `page` und `limit` |
| `POST` | `/api/books` | Buch mit `title` und `author` anlegen |
| `PUT` | `/api/books/<id>` | Vorhandenes Buch aktualisieren |
| `DELETE` | `/api/books/<id>` | Vorhandenes Buch löschen |

Beispiel für einen gefilterten, paginierten Abruf:

```text
GET /api/books?author=George%20Orwell&page=1&limit=10
```

Beispiel für POST oder PUT:

```json
{
  "title": "The Hobbit",
  "author": "J. R. R. Tolkien"
}
```

## Verhalten

- Neue Bücher erhalten automatisch die nächste freie ID.
- Fehlende Ressourcen liefern JSON mit Status `404`.
- Nicht erlaubte HTTP-Methoden liefern JSON mit Status `405`.
- Ungültige oder unvollständige Buchdaten liefern Status `400`.
- `GET` und `POST /api/books` sind auf zehn Anfragen pro Minute begrenzt; Überschreitungen liefern Status `429`.
- Eingehende API-Aufrufe werden mit Zeitstempel und Log-Level protokolliert.

## Paginierungs-Client

`pagination_client.py` ruft alle Seiten mit jeweils zehn Büchern ab. Bei aktiver Ratenbegrenzung muss zwischen mehr als zehn Seiten entsprechend gewartet werden.

```bash
python3 pagination_client.py
```

## Tests

```bash
python3 -m unittest -v
```

Die Daten werden für dieses Lernprojekt im Arbeitsspeicher gehalten und beim Neustart der Anwendung zurückgesetzt.
