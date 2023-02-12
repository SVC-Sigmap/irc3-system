#-------------------------------------------------------------------
#  File: signal_scanner.py
#  Summary: Module that wraps around iwconfig linux utility and returns
#           a dictonary of the collected data. The main piece of data
#           that this module is responsible for gathering is Link 
#           Quality. This metric is the primary metric that will be used
#           to assess signal strength.
#  Functions:
#           get_signal_data()
#           Creates a dictionary to be turned into json later. Spawns 
#           iwconfig subprocess and monitors the output to a variable.
#           The output is then parsed and relevant data is shipped to
#           the dictionary to be sent over the API.
#-------------------------------------------------------------------
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
            # Additionally, Link Quality is derived from Signal Level, so it is unlikely this metric will be
            # Entirely that useful however it is good to collect and return it anyway.
            # Signal Level can give the same value as Link Quality (%) with the following:
            # quality_percent = (signal_strength + 110) * 10 / 7
            match = re.search("Signal level=-([0-9]+)", line)
            signal_level_dbm = -(int(match.group(1)))
            data["signal_level_dbm"] = signal_level_dbm
            
        if "Bit Rate" in line:
            # Bit rate in iwconfig is a rough approx, however it could be useful at some point.
            match = re.search("Bit Rate=([0-9]+)", line)
            bit_rate = int(match.group(1))
            data["bit_rate"] = bit_rate
            
        if "Access Point" in line:
            # General information gathering
            match = re.search("Access Point: ([0-9A-Fa-f:]+)", line)
            data["access_point"] = match.group(1)
            
        if "ESSID" in line:
            # General information gathering
            match = re.search('ESSID:"([^"]+)"', line)
            data["essid"] = match.group(1)
            
    return data