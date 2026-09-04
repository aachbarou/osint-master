# OSINT-Master

A multi-functional OSINT (Open-Source Intelligence) tool capable of performing comprehensive passive reconnaissance based on IP addresses, usernames, and domains.

> **⚠️ Ethical and Legal Guidelines**
> 
> This tool is developed strictly for educational purposes, defensive security analysis, and authorized auditing.
> - **Do not** use this tool to gather information on targets without explicit, authorized permission.
> - **Privacy Implications:** The tool aggregates publicly available data. Respect privacy laws and regulations (e.g., GDPR, CCPA) in your jurisdiction.
> - **Legal Considerations:** Unauthorized reconnaissance or misuse of the data obtained can result in severe legal consequences. The author(s) assume no liability and are not responsible for any misuse or damage caused by this program.

## Features

- **IP Lookup**: Retrieve geolocation data, ISP details, and known abuse history.
- **Username Lookup**: Check presence on multiple social networks and public repositories.
- **Domain Enumeration**: Discover subdomains, retrieve IP addresses, SSL certificates, and check for subdomain takeover risks.

## Prerequisites and Setup

**Requirements:**
- Python 3.8+
- Internet connection for querying external APIs

**Installation Instructions:**

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/osint-master.git
   cd osint-master
   ```
2. (Recommended) Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a system shortcut to run the tool from anywhere (no sudo required):
   ```sh
   chmod +x src/main.py
   mkdir -p ~/.local/bin
   ln -s $(pwd)/src/main.py ~/.local/bin/osintmaster
   ```
   *(Note: Ensure `~/.local/bin` is in your system's PATH. If not, restart your terminal or add it to your `.bashrc` / `.zshrc`)*

## Command-Line Options

```
$> osintmaster --help
Welcome to osintmaster multi-function Tool

OPTIONS:
  -i "IP Address"   Search information by IP address
  -u "Username"     Search information by username
  -d "Domain"       Enumerate subdomains and check for takeover risks
  -o "FileName"     File name to save output
  --help            Display this help message
```

## Usage Examples

**1. IP Address Lookup**
```sh
osintmaster -i 8.8.8.8
```

**2. Username Lookup**
```sh
osintmaster -u john_doe
```

**3. Domain Enumeration**
```sh
osintmaster -d example.com
```

**4. Saving Output to a File**
You can combine flags and specify an output file in the `output/` directory:
```sh
osintmaster -i 8.8.8.8 -o output/results.txt
```

## Output Format

Results are printed directly to the standard output (terminal) in a readable plaintext format. 
If the `-o` parameter is provided, the exact same text output is written to the specified file (e.g., `output/results.txt`).

## Data Sources and APIs

The tool relies on the following external sources:
- **IP Lookup:** 
  - `ip-api.com` for geolocation and ISP data.
  - `api.blocklist.de` for IP abuse history.
- **Username Lookup:**
  - Standard HTTP requests to check profile existence on Facebook, Twitter/X, LinkedIn, Instagram, and GitHub.
  - `api.github.com` for retrieving detailed GitHub profile metadata and recent event history.
- **Domain Enumeration:**
  - Performs subdomain brute-forcing or queries using public certificate logs (implementation specific).

**API Configuration:** Currently, all APIs used by the tool are public and do not require API keys or complex configuration.

## Known Limitations

- **API Rate Limits:** Free public APIs have rate limits (e.g., GitHub allows 60 unauthenticated requests per hour; `ip-api.com` limits requests per minute). If you exceed these, the tool will output connection or rate-limit errors.
- **Data Accuracy:** Information is only as accurate as the external public APIs provide. Geolocation is often an approximation.
- **Social Media Blocks:** Social networks frequently change their structures and utilize anti-scraping mechanisms, which can lead to false negatives in username lookups.

## Troubleshooting

- **Dependency Errors:** Ensure you have activated your virtual environment and run `pip install -r requirements.txt`.
- **"Error querying IP geolocation data":** Verify your internet connection or check if `ip-api.com` is temporarily down.
- **Missing Results for Usernames:** Some social media platforms might block the bot's requests. This is normal behavior for unauthenticated scraping attempts.

## Project Structure

```
osint-master/
├── src/
│   ├── ip_lookup.py
│   ├── username_lookup.py
│   ├── domain_enum.py
│   └── main.py
├── tests/
│   └── test_main.py
├── output/
│   └── (saved results will be stored here)
├── resources/
│   └── osint-meme.png
├── README.md
├── requirements.txt
└── .gitignore
```
