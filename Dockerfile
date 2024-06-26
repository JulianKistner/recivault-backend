FROM python:3.12

# Kopiere den gesamten Inhalt des aktuellen Verzeichnisses in das Arbeitsverzeichnis im Container
COPY . .

# Installiere Pipenv und die Abhängigkeiten
RUN pip install pipenv
RUN pipenv install --deploy --system

# Setze den Befehl zum Ausführen der Anwendung
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]

EXPOSE 5000