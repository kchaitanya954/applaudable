import requests
from lxml import html
import csv

urls = [
        # 'https://techcrunch.com/category/transportation/',
        # 'https://techcrunch.com/category/transportation/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/commerce/',
        # 'https://techcrunch.com/category/enterprise/',
        # 'https://techcrunch.com/category/social/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/enterprise/',
        # 'https://techcrunch.com/category/transportation/',
        # 'https://techcrunch.com/category/commerce/',
        # 'https://techcrunch.com/category/security/',
        # 'https://techcrunch.com/category/transportation/',
        # 'https://techcrunch.com/category/fundraising/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/startups/',
        'https://techcrunch.com/category/startups/',
        # 'https://techcrunch.com/category/artificial-intelligence/',
        # 'https://techcrunch.com/category/transportation/',
        'https://techcrunch.com/category/market-analysis/',
        # 'https://techcrunch.com/category/security/',
        # 'https://techcrunch.com/category/social/'
        ]

def get_names(url):
    response = requests.get(url)

    # Parse the HTML content of the webpage
    tree = html.fromstring(response.content)

    # Extract all elements matching the XPath
    elements = tree.xpath("/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/text()")

    # Extract the text (names) from the elements
    names = [element.strip() for element in elements]
    
    # Print the extracted names
    return list(set(names))

import csv

def save_to_csv(data, filename):
    fieldnames = ['name', 'section']
    global names

    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty (to write the header only once)
            file.seek(0, 2)
            if file.tell() == 0:
                writer.writeheader()

            # save the data to the file and add it to the set
            for item in data:
                writer.writerow(item)
    except IOError:
        print("Error: Could not write to file.")
        
def main():      
    for url in urls:
        section = url.split('/')[-2]
        print(section)
        i = 1
        while True:
            page_url = url + f'page/{i}/'
            print(page_url)
            names =  get_names(page_url)
            i+=1
            if not names:
                break
            names_dict = [{"section": section, "name": name} for name in names]
            save_to_csv(names_dict, "techcrunch_names.csv")
        print("*"*10)
        
if __name__ == "__main__":
    main()
