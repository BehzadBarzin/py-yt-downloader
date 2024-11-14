import os
import requests
import sys
import geoip2.database

from .console import print_error, print_success
from .file import get_project_root

# ------------------------------------------------------------------------------
# Get the country name from ip address
def get_country_of_ip(ip: str) -> str:
    db_path = os.path.join(get_project_root(), "data", "GeoLite2-Country.mmdb")
    with geoip2.database.Reader(db_path) as reader:
        response = reader.country(ip)
        return response.country.name
        

# ------------------------------------------------------------------------------
def check_vpn():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip = response.json().get("ip")
        # ----------------------------------------------------------------------
        # Check if the current IP is from Iran
        if ip:
            # Get country name
            country = get_country_of_ip(ip)
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


