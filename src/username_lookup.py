import requests
import re
from datetime import datetime, timezone

from utils.parsers import extract_meta_details

def lookup_username(username):
    """
    Search information by username on various platforms.
    """
    # Remove @ if provided
    if username.startswith('@'):
        username = username[1:]

    result = []
    
    platforms = {
        "Facebook": f"https://www.facebook.com/{username}",
        "Twitter": f"https://x.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}/",
        "Instagram": f"https://www.instagram.com/{username}/",
        "GitHub": f"https://github.com/{username}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    for platform, url in platforms.items():
        try:
            req = requests.get(url, headers=headers, timeout=5)
            # 200 is found, though some sites might redirect to a login/home page if not found.
            # This is a best effort check.
            if req.status_code == 200:
                details = extract_meta_details(req.text)
                result.append(f"{platform}: Found{details}")
            else:
                result.append(f"{platform}: Not Found")
        except Exception:
            result.append(f"{platform}: Error connecting")

    # Fetch GitHub detailed user info
    try:
        user_req = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=5)
        if user_req.status_code == 200:
            u_data = user_req.json()
            name = u_data.get("name")
            bio = u_data.get("bio")
            followers = u_data.get("followers")
            
            gh_details = []
            if name: gh_details.append(f"Name: {name}")
            if bio:
                bio = bio.replace("\n", " ").replace("\r", "")
                if len(bio) > 50: bio = bio[:47] + "..."
                gh_details.append(f"Bio: {bio}")
            if followers is not None: gh_details.append(f"Followers: {followers}")
            
            if gh_details:
                result.append("GitHub Profile: " + ", ".join(gh_details))
    except Exception:
        pass

    # Fetch GitHub recent activity
    try:
        gh_req = requests.get(f"https://api.github.com/users/{username}/events/public", headers=headers, timeout=5)
        if gh_req.status_code == 200:
            events = gh_req.json()
            if events:
                latest_event = events[0]
                created_at_str = latest_event.get("created_at", "")
                
                if created_at_str:
                    try:
                        # Convert GitHub ISO8601 (ending in Z) to Python datetime
                        created_dt = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                        now_dt = datetime.now(timezone.utc)
                        diff = now_dt - created_dt
                        days = diff.days
                        
                        if days == 0:
                            time_str = "today"
                        elif days == 1:
                            time_str = "1 day ago"
                        else:
                            time_str = f"{days} days ago"
                            
                        result.append(f"Recent Activity: Active on GitHub, last event {time_str}")
                    except Exception:
                        result.append(f"Recent Activity: Active on GitHub (latest event at {created_at_str})")
                else:
                    result.append("Recent Activity: Active on GitHub")
            else:
                result.append("Recent Activity: Active on GitHub, but no recent public events")
        else:
            pass # Keep it simple, just don't append if user isn't on GitHub or API fails
    except Exception:
        pass

    return "\n".join(result)
