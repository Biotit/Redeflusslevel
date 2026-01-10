# 🗣️ Redeflusslevel
Redeflusslevel provides a way for Oliver to give Daniel suggestions about his amount of talking.

## ▶️ Installation, Running and Building
### Download code
```
git clone https://github.com/Biotit/Redeflusslevel
```

### Run locally
To run the source code locally via flet, create an environment and install flet, as well as matplotlib and numpy.
Or if using conda
```
conda env create -f conda/environment.yaml
conda activate app_oli
flet run main.py
```

### Run for test on Android
Install flet App on your Android device. Then run on a machine in the same network: `flet run --android` and scan the QR code with your Android device.

### Run using the synchronisation between page sessions
The app can be run several times on the same port, when using the web app.
```
flet run --web --port 8000 main.py
```
Now, changes in the slider get synchronised to the other open instance.

### Built app for own device
It is possible to build the app for Windows, Linux, Android and iOS, e.g. for Android via `flet build apk PATH_TO_PROGRAMM_FOLDER`.
However, additional installations are necessary. So for apk flutter needs to be installed and initialized, as well as android-sdk and sdkmanager.

### Replit
This app is available via Replit on https://redeflusslevel--biotit.replit.app/.

## ❗Features
### Slider
The slider provides the option to set an individual `Redeflusslevel` for Daniel (how much Oliver wishes him to speak). However, Daniel might or might not follow this suggestion. On the same page, there is a histogram displaying the likely distribution of Daniels `Redefluss`, because the distribution is spread around this optimal level. Additionally, further text fields allow to change the width and samples of the displayed distribution.

### Trend
Figure showing the trend of the set `Redeflusslevel` over time (after updating via button), as well as a violin plot of the set Redefluss values. Additionally, an option exist to delete the trend.

### Information about castles
Since most people (including Oliver) are characterised by their lack of knowledge about castles, this page gives helpful information about the history and architecture of castles, as well as the book of Daniel listing all castles hes been to (Burgenbuch), and how castles are mapped within OpenStreetmap.










