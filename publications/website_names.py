import requests
from lxml import html
import csv
from datetime import datetime, timedelta


urls = ['https://tech.eu/category/acquisition/',
 'https://tech.eu/category/biotech/',
 'https://tech.eu/category/crypto/',
 'https://tech.eu/category/cybersecurity/',
 'https://tech.eu/category/deep-tech/',
 'https://tech.eu/category/fintech/',
 'https://tech.eu/category/general/',
 'https://tech.eu/category/health-tech/',
 'https://tech.eu/category/medtech/',
 'https://tech.eu/category/mobility/',
 'https://tech.eu/category/podcast/',
 'https://tech.eu/category/proptech/',
 'https://tech.eu/category/quantum-computing/',
 'https://tech.eu/category/saas/',
 'https://tech.eu/category/spacetech/',
 'https://tech.eu/category/sustainability/']


# Define start and end dates
start_date = datetime(2020, 4, 1)  # April 1, 2011
end_date = datetime(2024, 5, 12)    # April 1, 2024


# Initialize a list to store formatted dates
formatted_dates = []

# Generate dates and format them
current_date = start_date
while current_date < end_date:
    # Format the date as "YYYY/M/D"
    formatted_date = "{}/{}/{}".format(current_date.year, current_date.month, current_date.day)
    formatted_dates.append(formatted_date)
    
    # Move to the next day
    current_date += timedelta(days=1)

def get_names(url):
    response = requests.get(url)

    # Parse the HTML content of the webpage
    tree = html.fromstring(response.content)

    # Extract all elements matching the XPath
    xpath = "//span[1]/a[1]/span[1]/text()"
    elements = tree.xpath(xpath)
    # Extract the text (names) from the elements
    names = [element.strip() for element in elements]
    
    # Print the extracted names
    return list(set(names))


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
        count =0
        for date in formatted_dates:
            page_url = url + date + '/'
            names =  get_names(page_url)
            names_dict = [{"section": section, "name": name} for name in names]
            save_to_csv(names_dict, "pub_names/theverge_names.csv")
            count +=1
            if count %365==0:
                print(count)
        print("*"*10)
        
if __name__ == "__main__":
    main()
