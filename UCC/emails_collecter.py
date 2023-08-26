import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess

def save_to_csv(data, filename):
    fieldnames = ['Corporate_Name', 'Document_Number', 'Status', 'email_addresses', 'mobile_numbers']
    global names

    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty (to write the header only once)
            file.seek(0, 2)
            if file.tell() == 0:
                writer.writeheader()

            # save the data to the file and add it to the set
            writer.writerow(data)
    except IOError:
        print("Error: Could not write to file.")
        
def get_html(first_name, last_name):
    url = f"https://www.google.com/search?q=%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com+%29+AND+%28intext%3A%27{first_name}%27%29+AND+%28intext%3A%27{last_name}%27%29"
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Proceed with parsing the HTML content
            html_content = response.text
        else:
            print("Failed to fetch the page. Status code:", response.status_code)
            time.sleep(5)
            stop_vpn()
            time.sleep(5)
            start_vpn()
            time.sleep(5)
            exit = True
            while exit:
                if connected_to_internet():
                    break       
                else:
                    time.sleep(5)

            html_content = 'skip'
    except:
        time.sleep(5)
        stop_vpn()
        time.sleep(5)
        start_vpn()
        time.sleep(5)
        exit = True
        while exit:
            if connected_to_internet():
                break       
            else:
                time.sleep(5)

        html_content = 'skip'
        
    return html_content

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def get_contact(html_content):
    
    # Regular expressions for email addresses and mobile numbers
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    mobile_pattern = r'\b\d{10}\b'

    # Extract email addresses and mobile numbers using the patterns
    email_addresses = re.findall(email_pattern, html_content, re.IGNORECASE)
    mobile_numbers = re.findall(mobile_pattern, html_content)
    return email_addresses, mobile_numbers




def start_vpn():
    vpn_command = "expressvpn connect"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def stop_vpn():
    vpn_command = "expressvpn disconnect"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def main():

    with open('florida.json', 'r') as file:
        # Read each line as a separate JSON object
        json_objects = [json.loads(line) for line in file]

    # Access the parsed JSON objects
    count = 11261
    for obj in json_objects[11261:]:
        count += 1
        if count%10==0:
            print(count)

        if ',' in obj["Corporate_Name"]:
            first_name, last_name = obj["Corporate_Name"].split(',')[:2]
        else:
            first_name = obj["Corporate_Name"]
            last_name = None

        company = obj["Document_Number"]
        filling_type = obj["Status"]
        if filling_type.lower() == 'active':
            html_content = get_html(first_name, last_name)
            if html_content == 'skip':
                continue
            email_addresses, mobile_numbers = get_contact(html_content)


            #html_content = get_html(first_name, last_name, company=None)
            #email_addresses_without_company, mobile_numbers_without_company = get_contact(html_content)

            #email_addresses.extend(email_addresses_without_company)
            #mobile_numbers.extend(mobile_numbers_without_company)

            obj['email_addresses'] = email_addresses
            obj['mobile_numbers'] = mobile_numbers

            save_to_csv(obj, f'data/florida.csv')
            time.sleep(0.2)
        
if __name__ == "__main__":
    main()