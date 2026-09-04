import re

def extract_meta_details(html):
    """
    Extract title or description from HTML to provide more context about the account.
    """
    title = ""
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        
    desc = ""
    og_desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html, re.IGNORECASE)
    if not og_desc_match:
        og_desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.IGNORECASE)
    
    if og_desc_match:
        desc = og_desc_match.group(1).strip()
        
    details = []
    if title:
        title = re.sub(r'\s*[|\-]\s*(LinkedIn|Twitter|X|Facebook|Instagram|GitHub).*', '', title, flags=re.IGNORECASE)
        if title and title != "Log In or Sign Up" and title != "Log in":
            details.append(title)
    if desc:
        if len(desc) > 80:
            desc = desc[:77] + "..."
        if desc and not desc.lower().startswith("log in"):
            details.append(desc)
            
    if details:
        # Unescape basic HTML entities
        text = " | ".join(details).replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'")
        return " - " + text
    return ""
