import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess

def save_to_csv(data, filename):
    fieldnames = ['Student Name', 'parent_name', 'parent_email', 'parent_phones', 'info']

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
        
def get_html(first_name, last_name, username, phone_number):
    url = f"https://www.google.com/search?q='intext%3A{username}%20%7C%20intext%3A{phone_number}%20%7C%20%28intitle%3A{first_name}%20AND%20intitle%3A{last_name}%29"
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
    items = []
    # Regular expressions for email addresses and mobile numbers
    soup = BeautifulSoup(html_content, 'html.parser')

    for a in soup.find_all('a', href=True):
        data = {}
        h3 = a.find('h3')
        if h3:
            data['heading'] = h3.text
            data['url'] = a['href']
            items.append(data)
    return items




def start_vpn():
    vpn_command = "expressvpn connect"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def stop_vpn():
    vpn_command = "expressvpn disconnect"  # Replace with the actual command
    subprocess.run(vpn_command, shell=True)

def main():

    json_data = []
    with open('asb_data.csv') as file:
        # Read each line as a separate JSON object
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            json_data.append(
                {
                    "Student Name": row['Student Name'],
                    "parent_name": row['parent_name'],
                    "parent_email": row['parent_email'],
                    "parent_phones": row['parent_phones']
                }
                )

    # Access the parsed JSON objects
    count = 130
    for obj in json_data[130:]:
        count += 1
        if count%10==0:
            print(count)
        try:
            if ',' in obj['parent_name']:
                first_name = obj["parent_name"].lower().split(',')[0]
                last_name = obj["parent_name"].lower().split(',')[-1]
            else:
                first_name = obj["name"].lower()
                last_name = None
        except:
            continue
            
        if row["parent_email"]:
            username = row["parent_email"].split('@')[0]
        else:
            username = None
        
        if row["parent_phones"]:
            phone_number = row["parent_phones"]
        else:
            phone_number = None
        print(first_name, last_name, username, phone_number)
        
        html_content = get_html(first_name, last_name, username, phone_number)
        if html_content == 'skip':
            continue
        items = get_contact(html_content) 
        obj['info'] = items
        # for data in items:
        #     obj['url'] = data['url']
        #     obj['heading'] = data['heading']
        save_to_csv(obj, f'abs_urls.csv')
        
if __name__ == "__main__":
    main()
