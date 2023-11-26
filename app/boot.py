import uos, machine, gc, network, time, json, neopixel

# Collect garbage
gc.collect()

# Load settings from JSON file
def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except OSError:
        print("Error: Unable to open 'settings.json'.")
        return None
    except ValueError:
        print("Error: Decoding JSON has failed.")
        return None

settings = load_settings()

# Exit if settings could not be loaded
if settings is None:
    print("Failed to load settings. Exiting...")
    machine.reset()

# Configuration from JSON
#Wifi Settings
SSID_TO_CONNECT = settings['wifi']['ssid']
WIFI_PASSWORD = settings['wifi']['password']
#Device Settings
NEOPIXEL_PIN = settings.get('neopixel_pin', 5)
BUTTON_PIN = settings.get('button_pin', 13)
NUMLEDS = settings.get('numleds', 1)
#OTA Settings
GITUSER = settings['ota']['gituser']
GITREPO = settings['ota']['gitrepo']
GITDIR = settings['ota']['gitdir']
GITFILES = settings['ota']['gitfiles']

np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUMLEDS)

def codeOTA():
    import senko
    OTA = senko.Senko(user=GITUSER, repo=GITREPO, working_dir=GITDIR, files=[GITFILES])
        
    if OTA.fetch():
        print("A newer version is available!")
        # RGB Flash
        for i in range(NUMLEDS):
            np[i] = (0, 0, 0)  # GRB format

        np[0] = (0, 255, 0)  # GRB format
        np[1] = (255, 0, 0)  # GRB format
        np[2] = (0, 0, 255)  # GRB format
        np.write()
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 1000:  # Loop for 1 second
            machine.idle()
        np[2] = (0, 255, 0)  # GRB format
        np[0] = (255, 0, 0)  # GRB format
        np[1] = (0, 0, 255)  # GRB format
        np.write()
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 1000:  # Loop for 1 second
            machine.idle()
        np[1] = (0, 255, 0)  # GRB format
        np[2] = (255, 0, 0)  # GRB format
        np[0] = (0, 0, 255)  # GRB format
        np.write()
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 1000:  # Loop for 1 second
            machine.idle()
            
        if OTA.update():
            print("Updated to the latest version! Rebooting...")
            machine.reset()
    else:
        print("Up to date!")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        print("Wifi disabled. Restart device to check for updates again.")
        print("Running main program")
        #import main


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        # Wait for connection with a timeout
        timeout = 10
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                print("Failed to connect to WiFi within timeout period.")
                return False
            time.sleep(1)
    print('Network config:', wlan.ifconfig())
    return True

def scan_for_ssid(ssid, wlan):
    print("Scanning for SSID:", ssid)
    networks = wlan.scan()
    for network in networks:
        if network[0].decode('utf-8') == ssid:
            return True
    return False

def main():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if scan_for_ssid(SSID_TO_CONNECT, wlan):
        if connect_to_wifi(SSID_TO_CONNECT, WIFI_PASSWORD):
            print("Connected to", SSID_TO_CONNECT)
            codeOTA()
        else:
            print("Failed to connect, turning off Wi-Fi")
            wlan.active(False)
    else:
        print("SSID not found, turning off Wi-Fi")
        wlan.active(False)

if __name__ == '__main__':
    main()