import pyperclip
import re
import ipaddress
import ipinfo
from prettytable import PrettyTable

# GET TOKEN FROM HERE: https://ipinfo.io/
access_token = 'TOKEN_GOES_HERE'  # Replace with your actual ipinfo access token
handler = ipinfo.getHandler(access_token)

def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

def get_ip_info(ip):
    if is_private_ip(ip):
        return {"ip": ip, "location": "Local IP Address", "organization": "Private Network"}
    else:
        try:
            details = handler.getDetails(ip)
            location = f'{details.city}, {details.region}, {details.country}'  # Customize this format as needed
            organization = details.org or "N/A"
            return {"ip": ip, "location": location, "organization": organization}
        except Exception as e:
            return {"ip": ip, "location": "Lookup Failed", "organization": "Lookup Failed"}

def main():
    clipboard_content = pyperclip.paste()
    ips = set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', clipboard_content))
    
    table = PrettyTable()
    table.field_names = ["IP Address", "Location", "Organization / Local IP Address"]
    
    for ip in ips:
        info = get_ip_info(ip)
        table.add_row([info["ip"], info["location"], info["organization"]])
    
    print(table)

if __name__ == "__main__":
    main()
