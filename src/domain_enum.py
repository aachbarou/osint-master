import requests

from utils.network import check_ssl, check_takeover_risk

def enumerate_domain(domain):
    """
    Enumerate subdomains and check for takeover risks.
    """
    result = []
    result.append(f"Main Domain: {domain}\n")
    
    subdomains = []
    try:
        # Use HackerTarget API for subdomain enumeration
        req = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        if req.status_code == 200:
            lines = req.text.strip().split('\n')
            for line in lines:
                if ',' in line:
                    sub, ip = line.split(',', 1)
                    if sub:
                        subdomains.append((sub.strip(), ip.strip()))
    except Exception as e:
        result.append(f"Error enumerating domain: {e}")
        return "\n".join(result)

    result.append(f"Subdomains found: {len(subdomains)}")
    takeover_risks = []
    
    for sub, ip in subdomains:
        ssl_status = check_ssl(sub)
        result.append(f"  - {sub} (IP: {ip})")
        result.append(f"    SSL Certificate: {ssl_status}")
        
        # Check for takeover risks
        risk = check_takeover_risk(sub)
        if risk:
            takeover_risks.append((sub, risk))
            
    if takeover_risks:
        result.append("\nPotential Subdomain Takeover Risks:")
        for sub, risk in takeover_risks:
            result.append(f"  - Subdomain: {sub}")
            result.append(f"    {risk}")
            
    return "\n".join(result)
