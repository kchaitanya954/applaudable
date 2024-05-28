import requests
from lxml import html
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def save_to_csv(data, filename):
    fieldnames = ['name', 'section', 'date', 'link']
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

def get_data(url):
    response = requests.get(url)

    # Parse the content of the response with lxml
    tree = html.fromstring(response.content)
    data = []
    # Use XPath to find the relevant elements
    articles = tree.xpath("//article[@class='item-search-listing result-article']")
    # print(articles)
    for article in articles:
        # Extract <p> class
        author = article.xpath(".//div[@class='text with-image']/p[@class='author']/text()")
        date = article.xpath(".//div[@class='text with-image']/p[@class='author']/span[@class = 'date']/text()")
        # Extract <a> href
        link = article.xpath(".//div[@class='text with-image']/a/@href")
        item = {
            'name': author[0] if author else '',
            'date': date[0] if date else '',
            'link': link[0] if link else ''
        }
        data.append(item)
    return data
    
def main():
    json_sections = []
    with open('keywords.csv', 'r') as file:
        # Read each line as a separate JSON object
        reader = csv.DictReader(file)
        for row in reader:
            json_sections.append(
                {
                    "section": row["spanish"]
                }
            )
    for obj in json_sections:
        section = obj['section'].lower()
        print(section)
        section_sh = section.replace(' ', '%20')
        page = 1
        while True:
            print(page)
            url='https://www.publico.es/search/'+section_sh + f'/{page}'
            data = get_data(url)
            page +=1
            if data:
                data_list = [{**item, 'section':section} for item in data]
                save_to_csv(data_list, 'pub_names/publico_names.csv')
            else:
                break
            
if __name__ == "__main__":
    main()
      
