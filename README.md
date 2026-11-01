# ipTracker
A simple python script to track and log changes in my dynamic Internet IP address.

# Raspberry Pi IP Tracker & Buzzer Alert

A lightweight Python script designed for a Raspberry Pi (specifically tested with a Raspberry Pi 3A+ and a Cytron Maker PHAT) that monitors a dynamic DNS domain (like DuckDNS), logs IP address changes to a CSV file, and provides physical buzzer feedback.


## Features

* **Dynamic IP Tracking:** Resolves your target domain name via DNS and checks for changes.
* **CSV Logging:** Automatically logs timestamps and new IP addresses with a header row if the file doesn't exist.
* **Audio Feedback (`gpiozero`):** 
  * Distinct double-beep when an IP address change is detected and logged.
  * Micro-chirp tick when the script runs and confirms the IP is unchanged (great for cron job verification).
* **Secure Configuration:** Separates local settings into an un-tracked configuration file to protect your personal domain and file paths when publishing to GitHub.


## Hardware Requirements

* Raspberry Pi
* Cytron Maker PHAT (or a standard active buzzer connected to GPIO pin 26)


## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Install Dependencies
Ensure you have Python 3 and the `gpiozero` library installed:
```bash
sudo apt update
sudo apt install python3-gpiozero
```

### 3. Configure Local Settings
Create a file named `mySecrets.py` in the same directory as `ipTracker.py` to store your personal domain and data path:

```python
# mySecrets.py

# Configuration for ipTracker.py
IPTDOMAIN = "your-domain.duckdns.org"  # Your dynamic DNS name.
IPTDATAFILE = "/home/pi/data/ipHistory.csv"  # Full path to your CSV data file.
```


## Usage

Run the script manually to test:
```bash
python3 ipTracker.py
```

### Automated Scheduling (Cron)
To check your IP automatically in the background (e.g., every 15 minutes, or 1 min past the hour), open your crontab:
```bash
crontab -e
```

Add one of the following lines of config to your crontab (adjusting paths to match your system):
```bash
# Execute the script every 15 mins:
*/15 * * * * /usr/bin/python3 /path/to/ipTracker.py >/dev/null 2>&1
```

```bash
# Execute the script at 1 min past the hour:
1 * * * * /usr/bin/python3 /path/to/ipTracker.py >/dev/null 2>&1
```

Finally, verify the contents of your crontab file:
```bash
crontab -l
```


## License

This project is open-source and available under the [MIT License](LICENSE).


//EOF