import pprint

import requests
import json
import argparse
import os
import time
from wakeonlan import send_magic_packet
import config

"""
This script starts defined Bravia screens by a defined time
and powers off the screens at a defined time.
add the script to your crontab to run at the desired time to power on/off the screens
"""

timeout = config.timeout
tvs = config.tvs
pin = config.pin

def execute_command(command, ip):
    """
    Execute a command on the TV with the given IP address.
    """
    auth = ('', pin) if pin else None
    headers = {
        'Connection': 'keep-alive',
        'X-Auth-PSK': pin
    }
    url = f'http://{ip}/sony/system'
    try:
        response = requests.post(url, data=command, headers=headers, timeout=timeout, auth=auth)
        return response
    except requests.exceptions.ConnectionError:
        print(f"Error connecting to IP: {ip}")
        return "Error"

def host_up(hostname, waittime=10):
    """
    Check if the host is up by pinging the IP address.
    """
    assert isinstance(hostname, str), "IP/hostname must be provided as a string."
    return os.system(f"ping -c 1 -W {waittime} {hostname} > /dev/null 2>&1") == 0

def get_power_status(ip):
    """
    Get the power status of the TV.
    """
    if host_up(ip, waittime=2):
        try:
            cmd = json.dumps({"method": "getPowerStatus", "params": [], "id": 50, "version": "1.0"}).encode("utf-8")
            res = execute_command(cmd, ip)
            if res != "Error":
                jres = json.loads(res.text)
                return jres["result"][0]["status"] == "active"
            return False
        except ValueError as e:
            print(f"Error getting PowerStatus: {e}")
            return False
    return False

def power_off(ip):
    """
    Power off the TV.
    """
    try:
        cmd = json.dumps({"method": "setPowerStatus", "id": 55, "params": [{"status": False}], "version": "1.0"}).encode("utf-8")
        res = execute_command(cmd, ip)
        if res != "Error":
            jres = json.loads(res.text)
            return True
        return False
    except ValueError as e:
        print(f"Error powering off the TV: {e}")
        return False

def power_on(ip):
    """
    Power on the TV.
    """
    try:
        cmd = json.dumps({"method": "setPowerStatus", "id": 55, "params": [{"status": True}], "version": "1.0"}).encode("utf-8")
        res = execute_command(cmd, ip)
        jres = json.loads(res.text)
        return True
    except ValueError as e:
        print(f"Error powering on the TV: {e}")
        return False

def enable_wol(ip):
    """
    Enable Wake-on-LAN (WOL) mode on the TV.
    """
    try:
        cmd = json.dumps({"method": "setWolMode", "params": [{"enabled": True}], "id": 55, "version": "1.0"}).encode("utf-8")
        res = execute_command(cmd, ip)
        jres = json.loads(res.text)
        return True
    except ValueError as e:
        print(f"Error enabling WOL mode: {e}")
        return False

def get_wol_mode(ip):
    """
    Get the WOL mode status of the TV.
    """
    try:
        cmd = json.dumps({"method": "getWolMode", "id": 50, "params": [], "version": "1.0"}).encode("utf-8")
        res = execute_command(cmd, ip)
        jres = json.loads(res.text)
        return jres["result"][0]["enabled"] == "True"
    except ValueError as e:
        print(f"Error getting WOL mode: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--Power', dest='format', choices=['on', 'off'], help="Power on or off the configured TVs")
    parser.add_argument('--enableWol', action='store_true', help="Enable WOL on the configured TVs")
    parser.add_argument('--getPower', action='store_true', help="Get power status of all TVs")
    args = parser.parse_args()
    power = args.format

    if power == 'on':
        for ip, mac in tvs.items():
            try:
                if get_power_status(ip):
                    print("The monitor is on")
                else:
                    print(f"Powering on monitor with IP {ip}")
                    send_magic_packet(mac)
                    time.sleep(10)
                    if host_up(ip):
                        try:
                            print(f"Powering on monitor with IP {ip}")
                            power_on(ip)
                        except ValueError as e:
                            print(f"Error powering on the TV: {e}")
            except ValueError as e:
                print(f"Error turning on the TV: {e}")
    elif power == 'off':
        for ip, mac in tvs.items():
            try:
                if power_off(ip):
                    print(f"Powered off the monitor: {ip}")
            except ValueError as e:
                print(f"Error powering off the TV: {e}")

    if args.enableWol:
        for ip, mac in tvs.items():
            try:
                enable_wol(ip)
                if get_wol_mode(ip):
                    print(f"WOL for {ip} is enabled")
                else:
                    print(f"Unable to enable WOL for {ip}")
            except ValueError as e:
                print(f"Error enabling WOL for {ip}: {e}")

    if args.getPower:
        for ip, mac in tvs.items():
            try:
                if get_power_status(ip):
                    print(f"{ip} is ON")
                else:
                    print(f"{ip} is OFF")
            except ValueError as e:
                print(f"Error getting power status for {ip}: {e}")

if __name__ == "__main__":
    main()