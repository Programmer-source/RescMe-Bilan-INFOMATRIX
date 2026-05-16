# RescMe-Bilan-INFOMATRIX
Andrii BIlan's INFOMATRIX Hackathon K-12 app
This mobile app was made in 24 hours using Python and a framework called “Flet”. It is made to help people react the right day during difficult situations.  Its main advantage is that it is very user-friendly – has a very simple and understandable UI and it works entirely offline because there is a very low chance that in a dangerous situation you’ll have internet and a stable connection. 

The problem:
When disaster strikes — earthquakes, fires, medical emergencies — internet and cell networks often fail. So our app's goal is to work and instruct the user correctly in case that happens.

The app's features are:
1. Offline mental help assistant chat (a logical script that creates a calming feeling for the user as if they're not alone);
2. Threat Detection image classifier model - classifies enviromental dangers. Runs localy on your device and offline;
3. Offline map with high risk danger zones;
4. Training feature - shows step by step guides on what to do in high risk situations;
5. I need help NOW (SOS Emergency feature) - user answers 3 simple questions (answer options are in a list) and gets step by step instructions on what to do in their situation. There's also an option for simulating a call to 911 (when the product will get into commercial use - you can add a real call to 911). Also it reads out loud the user's conditions.

BENEFIT - RUNS COMPLETELY LOCALLY AND OFFLINE!!!

How to use?
1. Run the file;
2. Log in;
3. Explore the features.

Required libraries:
flet
flet-map
pyttsx3
Pillow
tf-keras
tensorflow
numpy
opencv-python

NOTE - mobile port is still in development. However, it already works!
