#!/usr/bin/env python3
# Check my DuckDNS domain IP, log changes to CSV, and provide buzzer feedback.

import csv
import os
from datetime import datetime
import socket

from gpiozero import Buzzer
from gpiozero.exc import GPIOPinInUse
from time import sleep

# Default Configuration Placeholders.
DOMAIN = "your-domain.duckdns.org"  # Your dynamic DNS name.
DATAFILE = "./ipHistory.csv"  # Full path to your CSV data file.

# Cytron Maker PHAT GPIO Pin Mapping.
LED_PINS   = [17, 18, 27, 22, 25, 12, 13, 19]
SW1_PIN    = 21
SW2_PIN    = 16
SW3_PIN    = 20
BUZZER_PIN = 26

# My Local Secrets/Overrides, if they exist...
try:
    import mySecrets
    DOMAIN = getattr(mySecrets, "IPTDOMAIN", DOMAIN)
    DATAFILE = getattr(mySecrets, "IPTDATAFILE", DATAFILE)
except ImportError:
    pass


def BuzzerAlert(bzDuration, pulses=1, pause=0.05):
    # Try to grab the Cytron GPIO buzzer pin and sound a quick beep.
    try:
        buzzer = Buzzer(BUZZER_PIN)
        while pulses > 0:
            buzzer.on()
            sleep(bzDuration)
            buzzer.off()
            pulses -= 1
            # If there are still pulses left, pause before the next one.
            if pulses > 0:
                sleep(pause)
        buzzer.close()
    except (GPIOPinInUse, Exception):
        # Pass silently if the buzzer pin is locked by another process.
        pass


def GetCurrentIP(domain):
    # Resolve the target domain name to its current public IP address via DNS.
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print("Error resolving domain: %s" % str(e))
        return None


def GetLastLoggedIP(dataFile):
    # Check if the history file exists; return None if it hasn't been created yet.
    if not os.path.exists(dataFile):
        return None
    try:
        with open(dataFile, mode="r", encoding="utf-8") as file:
            csvReader = list(csv.reader(file))
            if len(csvReader) > 1: # If there are rows past the header.
                return csvReader[-1][1] # Return the last recorded IP address.
    except Exception as e:
        print("Error reading data file: %s" % str(e))
    return None


def LogIP():
    currentIP = GetCurrentIP(DOMAIN)
    if not currentIP:
        return

    fileExists = os.path.exists(DATAFILE)
    previousIP = GetLastLoggedIP(DATAFILE)

    # Log the current IP only if it has changed or if the data file doesn't exist yet.
    if currentIP != previousIP:
        timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(DATAFILE, mode="a", newline="", encoding="utf-8") as file:
                csvWriter = csv.writer(file)
                if not fileExists or os.path.getsize(DATAFILE) == 0:
                    csvWriter.writerow(["Timestamp", "IP Address"])
                csvWriter.writerow([timeNow, currentIP])
            print("[%s] IP changed and logged: %s" % (timeNow, currentIP))
            # Distinct double-beep for an actual IP change (and a longer duration).
            BuzzerAlert(bzDuration=0.08, pulses=2, pause=0.08)
        except Exception as e:
            print("Error writing to data file: %s" % str(e))
    else:
        print("IP unchanged (%s). No log added!" % currentIP)
        # Micro-chirp (almost a silent tick) just to confirm cron executed.
        BuzzerAlert(bzDuration=0.01, pulses=1)


if __name__ == "__main__":
    LogIP()


# EOF