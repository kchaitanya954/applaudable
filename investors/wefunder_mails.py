import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess

def save_to_csv(data, filename):
    fieldnames = ['name', 'url', 'email_addresses', 'mobile_numbers']
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
        
def get_html(first_name):
    url = f"https://www.google.com/search?q=%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com%7C+intext%3A%40.com%7C+intext%3A%40+%29+AND+%28intext%3A%27{first_name}%27%29"
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
    json_names = []
    with open('data/wefunder_random_data.csv', 'r') as file:
        # Read each line as a separate JSON object
        reader = csv.DictReader(file)
        for row in reader:
            json_names.append(
                {
                    "name": row["name"].lower(),
                    "url" : row["url"] 
                }
            )
    # Access the parsed JSON objects
    count = 1665
    for obj in json_names[1665:]:
        # print(obj)
        count += 1
        if count%10==0:
            print(count)
        if ' | ' in obj['name']:
            name = obj['name'].split(" | ")[0]
            obj['name'] = name

        try:
            url = obj['url'].split("/url?q=")[1].split("&")[0]
            obj['url'] = url
            username = url.split('wefunder.com/')[-1].split('/')[0]
            print(username)
        except:
            continue
        
        if username:            
            html_content = get_html(username)
            if html_content == 'skip':
                continue
            email_addresses, mobile_numbers = get_contact(html_content)

            obj['email_addresses'] = email_addresses
            obj['mobile_numbers'] = mobile_numbers            
            
            save_to_csv(obj, f'processed_data/wefunder_random_mails.csv')
            time.sleep(0.2)
        
if __name__ == "__main__":
    main()