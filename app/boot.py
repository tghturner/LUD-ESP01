import uos, machine, gc, network, time, json, neopixel, config

# Collect garbage
gc.collect()

# Exit if settings could not be loaded
if config.settings is None:
    print("Failed to load settings. Exiting...")
    machine.reset()

# Configuration from JSON
#Wifi Settings
SSID_TO_CONNECT = config.settings['wifi']['ssid']
WIFI_PASSWORD = config.settings['wifi']['password']
#Device Settings
NEOPIXEL_PIN = config.settings.get('neopixel_pin', 5)
NUMLEDS = config.settings.get('numleds', 1)
#OTA Settings
GITUSER = config.settings['ota']['gituser']
GITREPO = config.settings['ota']['gitrepo']
GITDIR = config.settings['ota']['gitdir']
GITFILES = config.settings['ota']['gitfiles']

np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUMLEDS)

def codeOTA():
    import senko
    OTA = senko.Senko(user=GITUSER, repo=GITREPO, working_dir=GITDIR, files=GITFILES)
        
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
        np[0] = (0, 255, 0)  # GRB format
        np[1] = (255, 0, 0)  # GRB format
        np[2] = (0, 0, 255)  # GRB format
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
        gc.collect()
        import main
        main.mainloop()


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
