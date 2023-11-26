# LUD-ESP01
Code for Light Up Decoration project. Configured for automatic updates when device in school.

Also needs a settings.json file on device.

{
  "wifi": {
    "ssid": "SSID",
    "password": "SSIDPASSWORD"
  },
  "ota": {
    "gituser": "tghturner",
    "gitrepo": "LUD-ESP01",
    "gitdir": "app",
    "gitfiles": ["main.py","boot.py","config.py","senko.py"]
  },
  "neopixel_pin": 5,
  "numleds": 3,
  "button_pin": 13
}
