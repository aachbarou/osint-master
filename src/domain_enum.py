import requests
import ssl
import socket
import datetime
import dns.resolver

def check_ssl(hostname):
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5.0)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            not_after_str = cert['notAfter']
            not_after = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
            return f"Valid until {not_after.strftime('%Y-%m-%d')}"
    except Exception:
        return "Not found"

def check_takeover_risk(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            target = rdata.target.to_text().lower()
            # Common vulnerable services
            vulnerable_services = [
                '.s3.amazonaws.com', 
                '.github.io', 
                '.herokuapp.com', 
                '.azurewebsites.net', 
                '.cloudapp.net',
                '.storage.googleapis.com',
                '.zendesk.com'
            ]
            if any(svc in target for svc in vulnerable_services):
                try:
                    # Check if target domain doesn't resolve or returns 404
                    req = requests.get(f"http://{target}", timeout=3)
                    if req.status_code == 404:
                        return f"CNAME record points to a potentially non-existent or misconfigured service ({target})\n    Recommended Action: Remove or update the DNS record to prevent potential misuse"
                except Exception:
                    # DNS failure for CNAME target
                    return f"CNAME record points to a non-existent or failing service ({target})\n    Recommended Action: Remove or update the DNS record to prevent potential misuse"
    except Exception:
        pass
    return None

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
