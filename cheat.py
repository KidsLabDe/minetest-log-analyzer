import re
from collections import defaultdict
from datetime import datetime
import sys

def analyze_log_file(filename):
    # Dictionary to store IP -> set of usernames mapping
    ip_to_users = defaultdict(set)
    
    # Regular expression pattern to extract information
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}): ACTION\[Server\]: (\w+) \[([0-9.]+)\] joins game'
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Only process 'joins game' entries
                if 'joins game' in line:
                    match = re.match(pattern, line)
                    if match:
                        timestamp, username, ip = match.groups()
                        ip_to_users[ip].add(username)
        
        # Find and report IPs with multiple usernames
        suspicious_ips = {
            ip: usernames 
            for ip, usernames in ip_to_users.items() 
            if len(usernames) > 1
        }
        
        if suspicious_ips:
            print("\nGefundene IPs mit mehreren Usernames:")
            for ip, usernames in suspicious_ips.items():
                print(f"\nIP: {ip}")
                print(f"Usernames: {', '.join(sorted(usernames))}")
        else:
            print("\nKeine IPs mit mehreren Usernames gefunden.")
            
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{filename}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")

# Hauptprogramm
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Verwendung: python script.py logfile.log")
        sys.exit(1)
        
    logfile = sys.argv[1]
    analyze_log_file(logfile)
