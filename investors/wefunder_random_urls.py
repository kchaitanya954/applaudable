import requests
import csv
from bs4 import BeautifulSoup
import re
import json
import time
import subprocess
import names

def save_to_csv(data, filename):
    fieldnames = ['name', 'url']

    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty (to write the header only once)
            file.seek(0, 2)
            if file.tell() == 0:
                writer.writeheader()

            # save the data to the file and add it to the set
            for row in data:
                # print(row['name'])
                writer.writerow(row)
    except IOError:
        print("Error: Could not write to file.")
        
def get_html(name):
    url = f"https://www.google.com/search?q=site%3Awefunder.com%2F+intext%3A{name}"
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
            data['name'] = h3.text
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

    names_set = set()

    # Access the parsed JSON objects
    count = 0
    while True:
        name = names.get_first_name()
        print(name)
        if name not in names_set:
            count += 1
            if count%10==0:
                print(count)

            html_content = get_html(name)
            if html_content == 'skip':
                continue
            items = get_contact(html_content)        
            # print(items)
            save_to_csv(items, f'data/wefunder_random_data.csv')
        
if __name__ == "__main__":
    main()
