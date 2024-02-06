import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess

def save_to_csv(data, filename):
    fieldnames = ['name', 'email_addresses', 'mobile_numbers']
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
        
def get_html(first_name, university, linkedin=True):
    if linkedin:
        url = f"https://www.google.com/search?q=site%3Ahttps%3A%2F%2Fwww.linkedin.com%2Fin%2F+%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com%7C+intext%3A%40.com%7C+intext%3A%40+%29+AND+%28intext%3A%27{first_name}%27%29+AND+%28intext%3A%27{university}%27%29"
    else:
        url = f"https://www.google.com/search?q=%28intext%3A%40gmail.com+%7C+intext%3A%40icloud.com+%7C+intext%3A%40yahoo.com+%7C+intext%3A%40outlook.com+%7C+intext%3A%40hotmail.com%7C+intext%3A%40.com%7C+intext%3A%40+%29+AND+%28intext%3A%27{first_name}%27%29+AND+%28intext%3A%27{university}%27%29"
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
    vpn_command = "echo -ne '\n' | surfshark-vpn attack"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def stop_vpn():
    vpn_command = "surfshark-vpn down"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def main():
    json_names = []
    with open('names.csv', 'r') as file:
        # Read each line as a separate JSON object
        reader = csv.DictReader(file)
        for row in reader:
            json_names.append(
                {
                    "name": row["name"],
                }
            )

    # Access the parsed JSON objects
    
    companies = [
                    'Massachusetts Institute of Technology (MIT)',
                    'University of Cambridge',
                    'University of Oxford',
                    'Harvard University',
                    'Stanford University',
                    'Imperial College London',
                    'ETH Zurich',
                    'National University of Singapore',
                    'University College London',
                    'University of California, Berkeley',
                    'University of Chicago',
                    'University of Pennsylvania',
                    'Cornell University',
                    'University of Melbourne',
                    'California Institute of Technology',
                    'Yale University',
                    'Peking University',
                    'Princeton University',
                    'University of New South Wales',
                    'University of Sydney'
                ]
    for company in companies:
        count = 0
        print(company)
        if company == 'adobe':
            json_names = json_names[2900:]
        for obj in json_names:
            count += 1
            if count%10==0:
                print(count)
            name = obj['name']
            university  =' microsoft'
            html_content = get_html(name, company)
            if html_content == 'skip':
                continue
            email_addresses, mobile_numbers = get_contact(html_content)

            html_content = get_html(name, university, linkedin=False)
            if html_content == 'skip':
                continue
            email_addresses2, mobile_numbers2 = get_contact(html_content)
            email_addresses += email_addresses2
            mobile_numbers += mobile_numbers2
            
            obj['email_addresses'] = email_addresses
            obj['mobile_numbers'] = mobile_numbers

            save_to_csv(obj, f'data/mails_{company}.csv')
            time.sleep(0.2)
        
if __name__ == "__main__":
    main()
