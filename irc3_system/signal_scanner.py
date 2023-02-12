import re, subprocess

def get_signal_data():
    data = {
        "link_quality": 0,
        "signal_level_dbm": 0,
        "bit_rate": 0,
        "access_point": "",
        "essid": ""
    }
    iwconfig_output = subprocess.run(["iwconfig"], stdout=subprocess.PIPE, text=True)
    output = iwconfig_output.stdout
    
    output_lines = output.split("\n")
    for line in output_lines:
        if "Link Quality" in line:
            match = re.search("Link Quality=([0-9]+)/([0-9]+)", line)
            # Link Quality is measured out of 70. This will turn the Link Quality returned to the API as a %
            link_quality = int(match.group(1)) / int(match.group(2)) * 100
            data["link_quality"] = link_quality
            
        if "Signal level" in line:
            # Signal level reports a value between -110 and -40. The higher the value the better the signal
            match = re.search("Signal level=-([0-9]+)", line)
            signal_level_dbm = -(int(match.group(1)))
            data["signal_level_dbm"] = signal_level_dbm
            
        if "Bit Rate" in line:
            match = re.search("Bit Rate=([0-9]+)", line)
            bit_rate = int(match.group(1))
            data["bit_rate"] = bit_rate
            
        if "Access Point" in line:
            match = re.search("Access Point: ([0-9A-Fa-f:]+)", line)
            data["access_point"] = match.group(1)
            
        if "ESSID" in line:
            match = re.search('ESSID:"([^"]+)"', line)
            data["essid"] = match.group(1)
            
    return data