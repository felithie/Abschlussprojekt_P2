# CardioCheck App 🫀
---

Willkommen bei **Cardio Check**! Diese Anwendung wurde entwickelt, um Benutzern zu helfen, ihre Herzgesundheit zu überwachen und mehr über verschiedene Herzthemen zu erfahren. Cardio Check bietet eine Vielzahl von Tools und Informationen, die es Ihnen ermöglichen, EKG-Daten zu analysieren, Ihre Herzfrequenz zu überwachen, informative Artikel zu lesen und vieles mehr.



**App Link:** https://cardiochecksfr.streamlit.app/


## Installation

Um Cardio Check auf Ihrem lokalen System zu installieren, führen Sie bitte die folgenden Schritte aus:

1. Klonen Sie das Repository:
    ```bash
    git clone https://github.com/IhrUsername/CardioCheck.git
    ```
2. Wechseln Sie in das Verzeichnis der Anwendung:
    ```bash
    cd CardioCheck
    ```
3. Installieren Sie die erforderlichen Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```
4. Starten Sie die Anwendung:
    ```bash
    streamlit run main.py
    ```

## Benutzung

Nach dem Start der Anwendung können Sie über die Seitenleiste zwischen verschiedenen Seiten navigieren. Jede Seite bietet unterschiedliche Funktionen und Informationen:

### Startseite

Auf der Startseite werden Sie herzlich willkommen geheißen und erhalten eine kurze Einführung zu Cardio Check. Hier können Sie sich über die verschiedenen Funktionen der App informieren und auswählen, welche Option Sie weiter erkunden möchten.

### About Us

Die Seite "About Us" bietet Informationen über das Team und die Mission von Cardio Check. Erfahren Sie mehr darüber, wer hinter dieser Anwendung steht und warum sie entwickelt wurde.

### Anmeldung

Auf der Anmeldungsseite können Sie sich entweder anmelden oder ein neues Benutzerkonto registrieren. Wenn Sie sich registrieren, können Sie ein Profil erstellen und nach der Anmeldung auf personalisierte Inhalte und Funktionen zugreifen. Sobald Sie angemeldet sind, haben Sie Zugriff auf Daten wie Ihren BMI, Ihre maximale Herzrate, Ihre generelle Herzfrequenz, Ihre Herzfrequenzvariabilität und weitere Gesundheitsdaten. Sie können auch aus einer eigenen CSV-Datei einen Plot Ihrer persönlichen Powercurve erstellen lassen.

Um die App auszutesten, können Sie eines dieser drei Profile benutzen:
- **Benutzername:** julian.huber, Passwort: 123
- **Benutzername:** yannic.heyer, Passwort: 123
- **Benutzername:** yunus.schmirander, Passwort: 123

Oder Sie erstellen ein eigenes Konto unter **"Registrieren"**. 

> [!IMPORTANT]
> Diese drei Benutzer sind hardgecodet, weil es bei der normalen Funktion immer eine Fehlermeldung gab. Mit dem Hardcoding wurde eine eigene Funktion implementiert, die nur verwendet wird, wenn eines dieser drei Benutzer genutzt wird. Falls ein neuer Benutzer erstellt wird, geht dies ganz normal über die normale Funktion. Um die Funktionen eines neuen Profils auszutesten, empfiehlt sich folgende Datei hochzuladen:uploads/ruhe_ecg_data.csv (findet man im Repository im Ordner "Uploads") .

### Über das Herz

Diese Seite bietet eine Sammlung von informativen Artikeln über verschiedene Herzthemen. Wählen Sie einen Artikel aus, um mehr zu erfahren:
- **Allgemeines zum Herz**
- **Herzfrequenz**
- **Was ist ein EKG?**
- **Vorhofflimmern**
- **Herzratenvariabilität**

### Trainingspuls-Rechner

Auf dieser Seite können Sie Ihren Maximalpuls und Ihre individuellen Belastungszonen berechnen. Geben Sie einfach Ihr Alter, Geschlecht und Ruhepuls ein, und die Anwendung berechnet Ihren Maximalpuls sowie die verschiedenen Trainingszonen, die für Ihr Training relevant sind.

### Impressum

Das Impressum enthält rechtliche Informationen zur Anwendung und den Entwicklern. Hier finden Sie Angaben zum Datenschutz und zu den Urhebern der Anwendung.

### Probleme und deren Lösung  :exclamation:

1. **Problem:** Das Hardcoden der drei Benutzer.

   **Lösung:** Diese Benutzer wurden hardgecodet, weil es bei der normalen Funktion immer eine Fehlermeldung gab. Mit dem Hardcoding wurde eine eigene Funktion implementiert, die nur verwendet wird, wenn eines dieser drei Benutzer genutzt wird. Falls ein neuer Benutzer erstellt wird, geht dies ganz normal über die normale Funktion.

3. **Problem:** Es kann nur eine Datei gleichzeitig hochgeladen werden, außer beim Account von Julian.

   **Lösung:** Löschen Sie die vorherige Datei, bevor Sie eine neue hochladen. Bei der Powercurve empfiehlt sich folgende Datei zum Testen:uploads/julian.huber/activity.csv (findet man im Repository im Ordner "Uploads" -> "julian.huber")

## WRAP UP

### Basisaufgaben

- [x] Geburtsjahr, Name und Bild der Personen wird angezeigt 
- [x] Auswahlmöglichkeit für Tests, sofern mehr als ein Test bei einer Person vorliegt 
- [x] Anzeigen des Testdatums und der gesamten Länge der Zeitreihe in Sekunden 
- [x] EKG-Daten werden beim Einlesen sinnvoll resampelt, um Ladezeiten zu verkürzen 
- [x] Sinnvolle Berechnung der Herzrate über den gesamten Zeitraum wird angezeigt 
- [x] Nutzer:in kann sinnvollen Zeitbereich für Plots auswählen 
- [x] Stil z.B. Namenskonventionen, sinnvolle Aufteilung in Module, Objektorientierung 
- [x] Kommentare und Docstrings 
- [x] Design für Computer Bildschirm optimiert und optisch ansprechend
- [x] Deployment auf Heroku oder Streamlit Sharing 

### Freie Aufgaben

- [x] Neue Daten mit einem Nutzer verknüpfen
- [x] Nutzerdaten editierbar machen
- [x] Benutzerspezifische Login-Funktion
- [x] Daten in einer SQLite oder tinyDB speichern 
- [x] Herzrate im sinnvollen gleitenden Durchschnitt als Plot anzeigen
- [x] Herzratenvariabilität anzeigen 
- [x] Maximalpuls anzeigen (ist außerhalb des Anmeldebefehls, damit es jeder benutzen kann, auch ohne Konto)
- [x] Interpretation der Herzraten mit Meldungen
- [x] BMI Rechner
- [x] Powercurve
- [x] About us
- [x] Übers Herz

---

Viel Spaß beim Erkunden und Überwachen Ihrer Herzgesundheit mit Cardio Check!
