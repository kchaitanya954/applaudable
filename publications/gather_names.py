import requests
import csv

def save_to_csv(data, filename):
    fieldnames = ['name', 'email', 'url', 'facebook', 'twitter', 'linkedIn']
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
        
# Define headers
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'VWO=25.500; client_id=7d1932a8b0565f43531041d20c5169b4446; lux_uid=171566471040314984; pushly.user_puuid=HOQ8TQUiCtiwYLyM1LLfxiiJBEuTGtow; _pnxd=7d1932a8b0565f43531041d20c5169b4446; _hp2_id.657665248={"userId":"6096943653273824","pageviewId":"1492120527323290","sessionId":"6747192975397682","identity":null,"trackerVersion":"4.0"}; _gcl_au=1.1.36720794.1715664711; _fbp=fb.1.1715664711336.933737806; _li_dcdm_c=.forbes.com; _lc2_fpi=1f8b889072fc--01hxtsbvqg1ak0xzmss1s84w14; _lc2_fpi_meta={"w":1715664711408}; AMP_TOKEN=$NOT_FOUND; _ga=GA1.2.1562198211.1715664711; _gid=GA1.2.464083097.1715664711; _dc_gtm_UA-5883199-3=1; _gat_UA-5883199-3=1; __qca=P0-170847806-1715664711303; blaize_session=81c31c47-d637-412a-b6a5-d39f20827176; blaize_tracking_id=07741158-b7a9-454e-b941-707d34512654; rbzid=O8qG/Sezz8/8IfHpjkATzn/RLeAjcUXsRvLKgI4aKfD6TfLVtw35X6SazawXqHQZbgY9C7uUQ/1YsQ5Ct9TriGvAO0gZGEemTT96c0Zud8BXjpg0tdXEqXLyyP3QnGj0+POLX5JtKzEYGllAF/RVOWzGWFHHetlQxaPILaclqJK+q71IOEXl9kddh7NeXiwxfQQrtdF72hGtgZWbae2lsy6RTmtpyjIXPop3NdAZU3I=; rbzsessionid=9c08bb820436d0e915ace9f25c0434b7; _hp2_ses_props.657665248={"r":"https://www.google.com","ts":1715664711100,"d":"www.forbes.com","h":"/social-media/","q":"?sh=7935eb2d410f"}; __gads=ID=558030b5b68383bc:T=1715664711:RT=1715664711:S=ALNI_MZR7MCDlA0pxmdJqsBWfCKbc5jHrg; __gpi=UID=00000e1bd68caa7d:T=1715664711:RT=1715664711:S=ALNI_MYIrF6-VxM9eGO1irBYxytCvOcSNw; __eoi=ID=2213039e26a7a00c:T=1715664711:RT=1715664711:S=AA-AfjZKXB0pqP1Odgs7mFJdjVvW; AWSALB=mh57nRqzHhIYxKVbxrgHwBjlbK0LKAr+lY8F+qO3mZ5YnEpWKfW1G01SrNlJ5wznsmb0jxZBoDq1iHex23BgWb/VYYd4aYTApGli52pTkFhH56u7tH1XF6or30Wc; AWSALBCORS=mh57nRqzHhIYxKVbxrgHwBjlbK0LKAr+lY8F+qO3mZ5YnEpWKfW1G01SrNlJ5wznsmb0jxZBoDq1iHex23BgWb/VYYd4aYTApGli52pTkFhH56u7tH1XF6or30Wc; _li_ss=CjUKBQgKEPUXCgYI3QEQ9RcKBQgGEPUXCgYIpQEQ9RcKBgiBARD1FwoGCKIBEPUXCgUICxD1Fw; _li_ss_meta=^{^"w^":1715664713623^,^"e^":1718256713623^}; _pnfcps=604800; _pnpcs=1|Tue, 21 May 2024 05:31:54 GMT; _pnlspid=31383; ki_t=1715664715889^;1715664715889^;1715664715889^;1^;1; ki_r=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8^; _cb=BaeO32D3xtm-Wl0nO; _chartbeat2=.1715664716129.1715664716129.1.DysamoD7Rvq4CAbx7JzbNAl6s5A5.1; _cb_svref=https^%^3A^%^2F^%^2Fwww.google.com^%^2F; cto_bundle=W7bTLF9WYkw5WVdvaG1xVjRmVko1RWl5REN0RjZBYm52cEgwODlOMG5IT1hGNmpZcjJGRlUlMkI4M1pWNlJhNTNzVWloOXlURiUyQmlWb1E3JTJGNlVCdXklMkIwVDklMkZ0NHFRWTAwJTJGZlpNYUcyU3Jab2VYbVAzTyUyQnolMkZqbnU1TUhhdWFxTDVyVHcxS0JrODFiVTNNenZ4Ykg4Q28xNVUyVDBLUnFhdkRYUEVqJTJGVTExc2UyMHNWTlowZWt6JTJCOUlCJTJCakQlMkZHdVhWdiUyRjBkOEtWNlhrVWYzcFh4TVdRaWFLalpPbnclM0QlM0Q; QSI_HistorySession=https^%^3A^%^2F^%^2Fwww.forbes.com^%^2Fsocial-media^%^2F^%^3Fsh^%^3D7935eb2d410f~1715664716484; _ga_DLD85VJ5QY=GS1.1.1715664711.1.0.1715664721.50.0.0; _pnss=dismissed; _pnpdm=true^',
    'referer': 'https://www.forbes.com/social-media/?sh=7935eb2d410f',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Send GET request

for i in range(3,125):
    j=0
    print(i)
    while True:
        try:
            url = f'https://www.forbes.com/simple-data/chansec/stream/?sourceValue=channel_{i}&start={j}&streamSourceType=channelsection'
            response = requests.get(url, headers=headers)
            data = response.json()['blocks']['items']
            j+=10
            if data:
                if j%1000 == 0:
                    print(i, j)
            else:
                break
            filtered_data = {}
            for item in data:
                email = item.get('author', {}).get('email')
                filtered_item = {
                    "name":item.get('author', {}).get('name'),
                    "email":email,
                    "url":item.get('author', {}).get('url'),
                    "facebook":item.get('social',{}).get('facebook'),
                    "twitter":item.get('social',{}).get('twitter'),
                    "linkedIn":item.get('social',{}).get('linkedIn'),
                }
                filtered_data[email] = filtered_item
            save_to_csv(filtered_data.values(), f"pub_names/forbes_data_{i}.csv")
        except:
            pass