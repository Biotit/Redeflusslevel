# Run locally
To run the source code locally via flet
- Dependencies
- run via flet run redeflusslevel_main.py
- run several times on the same port to make use of the synchronisation (PubSub) between the page sessions: flet run --web --port 8000 redeflusslevel_main.py
- https://docs.flet.dev/getting-started/running-app/#desktop-app

# Built app for own device
- flet build apk PATH_TO_PROGRAMM_FOLDER
- need flutter installed, need flutter to be initialized (command flutter run once)
- need android-sdk installed (sudo apt install google-android-cmdline-tools-13.0-installer)
- then run sdkmanager --licenses

# TODO
- run on cloudflare: https://docs.flet.dev/publish/web/static-website/hosting/cloudflare/
- github
- Infos über Burgen Seite füllen.
- Possibility to permanently save data

# Erledigte TODO:
- Button um Daten zu löschen vom Verlauf "Verlauf löschen" unter dem Abbildung aktualisieren

