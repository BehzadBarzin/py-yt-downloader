import requests
import sys

from .console import print_error, print_success

# ------------------------------------------------------------------------------
def check_vpn():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip = response.json().get("ip")
        # ----------------------------------------------------------------------
        # Check if the current IP is from Iran
        if ip:
            response = requests.get(f'https://api.hackertarget.com/geoip/?q={ip}&output=json').json()
            country = response.get("country")
            if country == "Iran":
                print_error("You are in Iran! Please, connect to VPN.")
                sys.exit(1)
            elif country == None:
                print_error("Could not determine IP location.")
                sys.exit(1)
            else:
                print_success(f"You are in {country}")
        else:
            print_error("Could not determine IP location.")
            sys.exit(1)
    except requests.RequestException as e:
        print_error("Error fetching public IP")
        sys.exit(1)

# ------------------------------------------------------------------------------


