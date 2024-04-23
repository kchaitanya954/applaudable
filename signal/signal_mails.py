import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess

def save_to_csv(data, filename):
    fieldnames = ['person_id', 'person_name', 'email_addresses', 'mobile_numbers', 'firm_name']
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
        
def get_html(first_name, company=None):
    if company:
        url = f"https://www.google.com/search?q=%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com%7C+intext%3A%40.com%7C+intext%3A%40+%29+AND+%28intext%3A%27{first_name}%27%29+AND+%28intext%3A%27{company}%27%29"
    else:
        url = f"https://www.google.com/search?q=%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com%7C+intext%3A%40.com%7C+intext%3A%40+%29+AND+%28intext%3A%27{first_name}%27%29"
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Proceed with parsing the HTML content
            html_content = response.text
        else:
            print("Failed to fetch the page. Status code:", response.status_code)
            stop_vpn()
            time.sleep(5)
            start_vpn()
            time.sleep(6)
            exit = True
            while exit:
                if connected_to_internet():
                    break       
                else:
                    time.sleep(5)

            html_content = 'skip'
    except:
        stop_vpn()
        time.sleep(5)
        start_vpn()
        time.sleep(7)
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
    vpn_command = "echo -ne '\n' | surfshark-vpn attack"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def stop_vpn():
    vpn_command = "surfshark-vpn down"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def main():
    json_names = []
    with open('signal_names.csv', 'r') as file:
        # Read each line as a separate JSON object
        reader = csv.DictReader(file)
        for row in reader:
            json_names.append(
                {
                    "person_name": row["person_name"],
                    "person_id": row["person_id"],
                    "firm_name": row["firm_name"]
                }
            )

    count = 0

    for obj in json_names[7500:]:
        count += 1
        if count%10==0:
            print(count)
        name = obj['person_name'].lower()
        html_content = get_html(name)
        if html_content == 'skip':
            continue
        email_addresses, mobile_numbers = get_contact(html_content)
        firm_name = obj.get("firm_name")
        if firm_name:
            html_content = get_html(name, firm_name)
            email_addresses2, mobile_numbers2 = get_contact(html_content)
            email_addresses += email_addresses2
            mobile_numbers += mobile_numbers2
    
        obj['email_addresses'] = email_addresses
        obj['mobile_numbers'] = mobile_numbers

        save_to_csv(obj, 'mails_signal3.csv')
        time.sleep(0.2)
        
if __name__ == "__main__":
    main()
