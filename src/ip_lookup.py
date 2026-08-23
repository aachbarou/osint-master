import requests
import json

def lookup_ip(ip):
    """
    Search information by IP address.
    Uses ip-api.com for IP geolocation and ISP.
    Uses api.blocklist.de for Abuse checks.
    """
    result = []
    
    # Geolocate and ASN
    try:
        req = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if req.status_code == 200:
            data = req.json()
            if data.get("status") == "success":
                result.append(f"ISP: {data.get('isp', 'Unknown')}")
                result.append(f"City: {data.get('city', 'Unknown')}")
                result.append(f"Country: {data.get('country', 'Unknown')}")
                # Format ASN string if it contains ASN name
                asn_str = data.get('as', 'Unknown')
                if asn_str.startswith("AS"):
                    asn = asn_str.split(" ")[0][2:]
                else:
                    asn = asn_str
                result.append(f"ASN: {asn}")
            else:
                result.append(f"Error querying IP: {data.get('message', 'Unknown error')}")
        else:
             result.append("Error querying IP geolocation data.")
    except Exception as e:
        result.append(f"Error querying IP geolocation data: {e}")

    # Abuse check
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
        abuse_req = requests.get(f"https://api.blocklist.de/api.php?ip={ip}", headers=headers, timeout=5)
        if abuse_req.status_code == 200:
            text = abuse_req.text
            if "reports: 0" in text and "attacks: 0" in text:
                result.append("Known Issues: No reported abuse")
            else:
                result.append(f"Known Issues: Reported abuse found (blocklist.de)")
        else:
             result.append("Known Issues: Error querying abuse database")
    except Exception as e:
        result.append(f"Known Issues: Error querying abuse database: {e}")
        
    return "\n".join(result)
