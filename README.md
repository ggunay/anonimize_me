# Proxy Scraper with ProxyChains Config Generation

This is a Python script that scrapes proxy data from a given URL or a file containing URLs and generates a ProxyChains configuration file for proxy chaining. It uses Selenium and Chrome WebDriver to parse dynamic web pages that load proxies from tables. The scraped proxies are then saved into a ProxyChains configuration file for easy use with various applications.

## Requirements

To use this script, you need to have the following installed:

- Python 3.6 or later
- Chrome WebDriver (compatible with your Chrome browser version)
- Chrome browser (optional, but required for GUI mode)

Furthermore, the proxies must be listed inside a table on the page.

## Installation

1. Clone this repository or download the `anonimize_me.py` script.

2. Install the required Python packages by running the following command:

```bash
pip install -r requirements.txt
```
## Usage

The script supports various options to customize the scraping process. Here are the available command-line arguments:

usage: generic4.py [-h] [--user-agent USER_AGENT] [--chain-len CHAIN_LEN] [--proxy_types PROXY_TYPES [PROXY_TYPES ...]] [--verbose] url

Proxy Scraper with ProxyChains Config Generation

positional arguments:
  url                   URL to scrape proxies from (or path to the file containing URLs, one per line)

optional arguments:
  -h, --help            show this help message and exit
  --user-agent USER_AGENT
                        Custom user-agent (optional)
  --chain-len CHAIN_LEN
                        Chain length for proxychains config (optional)
  --proxy_types PROXY_TYPES [PROXY_TYPES ...]
                        Proxy types to use (optional)
  --verbose             Enable verbose mode to print detailed information during the scraping process (optional)


## Examples

Scrape proxies from a single URL and generate a ProxyChains configuration file:

```bash
python anonimize_me.py https://example.com/proxies
```
Scrape proxies from a file containing multiple URLs and generate a ProxyChains configuration file:

```bash
python anonimize_me.py urls.txt
```
Scrape proxies with a custom user-agent and specify the proxy types to use:

```bash
python anonimize_me.py https://example.com/proxies --user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" --proxy_types socks4 socks5 http 
```
## Output

The script will generate a proxychains.conf file in the same directory. This file contains the ProxyChains configuration for the scraped proxies.

## TODO

Parallel parsing: Implement a feature to scrape multiple URLs concurrently using separate tabs to speed up the scraping process.

JSON output: Provide an option to save the scraped proxy data in JSON format and send it to endpoints for further processing.

Logging and verbose mode: Improve logging and add a verbose mode to print detailed information during the scraping process.

Proxy authentication: Add support for scraping proxies that require authentication.

More proxy types: Include additional proxy types for more comprehensive scraping.

Feel free to contribute to the project by adding new features or fixing bugs!