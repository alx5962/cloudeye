# Cloud Eye

Cloud Eye is a software that describes as keywords an image grabbed by a webcam. Those keywords can also be translated to a desired language (default language is english).
The goal of this project is to help people with visual impairment by bringing a description of their surrounding world using a portable device.


### Requirements
* An Orange Pi computer (Mine is a OrangePI 2+ but it must be easily adapted to other devices like a Raspberry Pi, using the appropriate GPIO library).
* A camera (I used both a Logitech and a PS3 Eye for this project). Under Linux, it uses /dev/video0. 
* An External Speaker connected to the 3.5mm Orange Pi jack (or hdmi audio out).
* A push to make button connected between GPIO 37 and GND.
* A LED Connected to GPIO 31 and GND.
 

### Usage:
There are 2 ways to use this script:
* Keyboard (Windows & Linux): press 'd' key to analyze, 'q' to quit.
* Push Button (Orange Pi only): press the push button to analyze.


### Python Dependencies
* GPIO library for OrangePI (https://github.com/duxingkei33/orangepi_PC_gpio_pyH3)
* pygame
* gtts
* googleapiclient
* oauth2client.client


### Other Dependencies
* A Google Translate API key (more infos here: https://cloud.google.com/translate/v2/quickstart).
* A Google Application Default Credentials JSON key  (more infos here: https://developers.google.com/identity/protocols/application-default-credentials#whentouse). 
* mpg123 (Linux)
* VLC (Windows)
* Internet access


### First Use:
You need to set the GOOGLE_APPLICATION_CREDENTIALS on your environment variables and your API_key for Google Translate in the script.

* Windows:
```
set GOOGLE_APPLICATION_CREDENTIALS=F:\keys\mykey.json
```

* Linux:
```
export GOOGLE_APPLICATION_CREDENTIALS=/home/user/keys/mykey.json
```

then launch cloudeye.py


### Issues/Bugs
You can adjust the volume with alsamixer under Linux.


### License
Cloud Eye is licensed under the GPLv3 License. 


### Credits
- The OrangePI code is mainly based on the work of dony71's [AlexaOPi](https://github.com/dony71/AlexaOPi)


