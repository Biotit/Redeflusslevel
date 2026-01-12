# 🗣️ Redeflusslevel
Redeflusslevel provides a way for Oliver to give Daniel suggestions about his amount of talking.

## ▶️ Installation, Running and Building
### Download code
```
git clone https://github.com/Biotit/Redeflusslevel
```

### Run locally
To run the source code locally via flet, create an environment and install flet, as well as matplotlib and numpy.
The specific versions are given inside requirements.txt or pyproject.toml. These specific versions are very important otherwise the code, and e.g. especially building apk does not work! Runtime.txt specifies the python version.

Or if using conda on a linux machine you can recreate my environment via
```
conda env create -f environment.yaml
conda activate App_Oli
cd src
flet run main.py
```

### Run for test on Android
Install flet App on your Android device. Then run on a machine in the same network: 
```
cd src
flet run --android` 
```
and scan the QR code with your Android device.

### Run using the synchronisation between page sessions
The app can be run several times on the same port, when using the web app.
```
cd src
flet run --web --port 8000 main.py
```
Now, changes in the slider get synchronised to the other open instance.

### Built for own device
It is possible to build the app for Linux, Windows, iOS and Android. Tested already for Android (apk).
For Android, run via
```
flet build apk
```
Necessary programs get installed automatically: Flutter, JDK, Android SDK.
The built apk is already provided within the `build` folder.
The specific settings for the building are given inside pyproject.toml.

### Replit
This app is available via Replit on https://redeflusslevel--biotit.replit.app/.

## ❗Features
### Slider
The slider provides the option to set an individual `Redeflusslevel` for Daniel (how much Oliver wishes him to speak). However, Daniel might or might not follow this suggestion. On the same page, there is a histogram displaying the likely distribution of Daniels `Redefluss`, because the distribution is spread around this optimal level. Additionally, further text fields allow to change the width and samples of the displayed distribution.

### Trend
Figure showing the trend of the set `Redeflusslevel` over time (after updating via button), as well as a violin plot of the set Redefluss values. Additionally, an option exist to delete the trend.

### Information about castles
Since most people (including Oliver) are characterised by their lack of knowledge about castles, this page gives helpful information about the history and architecture of castles, as well as the book of Daniel listing all castles hes been to (Burgenbuch), his castle Youtube channel GermanCastleProductions, and how castles are mapped within OpenStreetmap.










