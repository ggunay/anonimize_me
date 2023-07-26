import re
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to check if a cell data matches the given pattern
def cell_matches_pattern(cell_text, pattern):
    return re.search(pattern, cell_text)

# Function to scrape proxy data from a URL
def scrape_proxy_data(urls, user_agent, proxy_types_from_command_line, verbose):
    # Function to check if a cell text represents a valid port value
    def is_valid_port(td_element):
        port_pattern = r'(?<!\S)\d{2,5}(?!\S)'
        port_class_pattern = r'\bport\b'
        if cell_matches_pattern(td_element.text, port_pattern):

            class_attribute = td_element.get_attribute('class')
            if (class_attribute and cell_matches_pattern(class_attribute, port_class_pattern)) or not class_attribute:
                return True
            else:
                inner_elements = td_element.find_elements(By.XPATH, ".//*")
                for element in inner_elements:
                    if cell_matches_pattern(element.text, port_class_pattern):
                        return True
            return False
        else:
            return False

    # Set custom user-agent
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
        # Initialize WebDriver with custom user-agent
    driver = webdriver.Chrome(options=options)

    proxy_config = ""
    for url in urls:
        if verbose:
            print(f"Scraping proxies from: {url}")
        driver.get(url)

        # Wait for all table elements to be present
        wait = WebDriverWait(driver, 10)  # 10 seconds maximum wait time
        tables = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'table')))

        # Regular expression patterns to match IP address
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

        #proxy_data = []
        
        # Iterate through all tables on the page
        for table in tables:
            # Get all rows of the table
            rows = table.find_elements(By.TAG_NAME, 'tr')

            # Iterate through the rows and check for IP and port in each cell
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]

                # Check if IP and port exist in the row cells
                has_ip = any(cell_matches_pattern(cell_text, ip_pattern) for cell_text in row_data)
                has_port = any(is_valid_port(cell) for cell in cells)

                if has_ip and has_port:
                    # Check for potential proxy types (socks4, socks5, http)
                    proxy_types = [proxy_type.lower() for proxy_type in proxy_types_from_command_line if any(proxy_type in data.lower() for data in row_data)]

                    # If proxy types exist, extract IP, port, and proxy types
                    if proxy_types:
                        for cell in cells:
                            ip_match = cell_matches_pattern(cell.text, ip_pattern)
                            if ip_match:
                                ip = ip_match.group()
                                break

                        for cell in cells:
                            if is_valid_port(cell):
                                port = cell.text
                                break

                        for proxy_type in proxy_types:
                            proxy_config += f"{proxy_type} {ip} {port}\n"

                        #TODO: JSON support
                        # proxy_info = {
                        #     'ip': ip,
                        #     'port': port,
                        #     'proxy_types': proxy_types
                        # }
                        # proxy_data.append(proxy_info)

    # Close the driver after scraping is done
    driver.quit()

    return proxy_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Proxy Scraper with ProxyChains Config Generation')
    parser.add_argument('url', help='URL in the for of http(s)://... to scrape proxies from (or path to the file containing URLs, one per line)')
    parser.add_argument('--user_agent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', help='Custom user-agent (optional)')
    parser.add_argument('--chain-len', type=int, default=1, help='Chain length for proxychains config (optional)')
    parser.add_argument('--proxy_types', nargs='+', default=['socks4', 'socks5', 'http'], help='Proxy types to use, seperated by space (optional)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode to print messages for each critical step (optional)')


    args = parser.parse_args()


    proxy_types_from_command_line = [proxy_type.lower() for proxy_type in args.proxy_types[0].split()]
    proxy_config = "random_chain\n"
    proxy_config += f"chain_len = {args.chain_len}\n"
    proxy_config += "[ProxyList]\n"



    if args.url.startswith('http'):
        urls = [args.url]
    else:
        # Assume it's a file path, read URLs from the file
        with open(args.url, 'r') as file:
            urls = [line.strip() for line in file.readlines()]



    filename = f"proxychains.conf"
        
    try:
        with open(filename, "w") as f:
            f.write(proxy_config)

        proxy_data = scrape_proxy_data(urls, args.user_agent, proxy_types_from_command_line, args.verbose)

        filename = f"proxychains.conf"
        with open(filename, "a") as f:
            f.write(proxy_data)

        if args.verbose:
            #print(f"Proxies scraped from {url}:")
            print(proxy_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
