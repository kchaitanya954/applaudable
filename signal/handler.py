import requests
import pandas as pd


slugs = [
 'biotech-pre-seed',
 'transportationtech-seed',
 'future-of-work-pre-seed',
 'boston-new-england',
 'new-york-city',
 'digital-health-pre-seed',
 'canada',
 'retail-seed',
 'social-networks-pre-seed',
 'london',
 'raleigh-durham-southeast-us',
 'data-services-seed',
 'seattle-portland',
 'real-estate-proptech-pre-seed',
 'fashion-seed',
 'climatetech-cleantech-seed',
 'saas-seed',
 'israel',
 'washington-d-c',
 'latam-latin-america',
 'consumer-internet-seed',
 'ai-seed-israel',
 'hardware-seed',
 'who-invested-in-diverse-founders',
 'impact-seed',
 'advertising-seed',
 'digital-health-seed',
 'transportationtech-pre-seed',
 'fintech-pre-seed',
 'san-francisco-bay-area',
 'future-of-work-seed',
 'marketplaces-seed',
 'austin',
 'deeptech-pre-seed',
 'deeptech-seed',
 'los-angeles-southern-california',
 'food-and-beverage-seed',
 'fintech-seed',
 'gaming-esports-pre-seed',
 'midwest',
 'enterprise-pre-seed',
 'constructiontech-pre-seed',
 'angel-scout-and-solo-capitalists',
 'biotech-seed',
 'british-columbia',
 'who-were-founders',
 'advertising-pre-seed',
 'games-pre-seed',
 'ai-pre-seed',
 'female',
 'colorado-utah',
 'gaming-esports-seed',
 'diverse',
 'fashion-pre-seed',
 'enterprise-applications-pre-seed',
 'real-estate-proptech-seed',
 'data-services-pre-seed',
 'cloud-infrastructure-pre-seed',
 'retail-pre-seed',
 'energytech-seed',
 'enterprise-seed',
 'impact-pre-seed',
 'saas-pre-seed',
 'logistics-seed',
 'food-and-beverage-pre-seed',
 'games-seed',
 'marketplaces-pre-seed',
 'creator-passion-economy-seed',
 'who-invested-in-female-founders',
 'enterprise-applications-seed',
 'ai-pre-seed-israel',
 'constructiontech-seed',
 'cloud-infrastructure-seed',
 'hardware-pre-seed',
 'energytech-pre-seed',
 'consumer-internet-pre-seed',
 'climatetech-cleantech-pre-seed',
 'e-commerce-pre-seed']

url= "https://signal-api.nfx.com/graphql"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}



def save_data_from_slug(slug):
    payload = {"operationName":"vclInvestors",
               "variables":{"slug":slug,
                            "order":[{}],
                            "after":"OA"},
               "query":"query vclInvestors($slug: String!, $after: String) {\n  list(slug: $slug) {\n    id\n    slug\n    investor_count\n    vertical {\n      id\n      display_name\n      kind\n      __typename\n    }\n    location {\n      id\n      display_name\n      __typename\n    }\n    stage\n    firms {\n      id\n      name\n      slug\n      __typename\n    }\n    scored_investors(first: 8, after: $after) {\n      pageInfo {\n        hasNextPage\n        hasPreviousPage\n        endCursor\n        __typename\n      }\n      record_count\n      edges {\n        node {\n          ...investorListInvestorProfileFields\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment investorListInvestorProfileFields on InvestorProfile {\n  id\n  person {\n    id\n    first_name\n    last_name\n    name\n    slug\n  linkedin_url\n  twitter_url\n  is_me\n    is_on_target_list\n   __typename\n  }\n  image_urls\n  position\n  min_investment\n  max_investment\n  target_investment\n  areas_of_interest_freeform\n is_preferred_coinvestor\n  firm {\n    id\n  current_fund_size\n  name\n    slug\n    __typename\n  }\n  investment_locations {\n    id\n    display_name\n    location_investor_list {\n   stage_name\n   id\n      slug\n      __typename\n    }\n    __typename\n  }\n  investor_lists {\n    id\n    stage_name\n    slug\n    vertical {\n   kind\n   id\n      display_name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}

    results = pd.DataFrame()
    hasNextPage = True
    after = ''

    while hasNextPage == True:
        payload['variables']['after'] = after
        try:
            jsonData = requests.post(url, headers=headers, json=payload ).json()
            data = jsonData['data']['list']['scored_investors']['edges']
            df = pd.json_normalize(data)
            results = pd.concat([results, df], ignore_index=True)
            # results = results.append(df, sort=False).reset_index(drop=True)

            count = len(results) 
            tot = jsonData['data']['list']['investor_count']

            print(f'{count} of {tot}')

            hasNextPage = jsonData['data']['list']['scored_investors']['pageInfo']['hasNextPage']
            after = jsonData['data']['list']['scored_investors']['pageInfo']['endCursor']
        except:
            pass
    
    results.to_csv(f'data/{slug}.csv',  index=False)
    
if __name__ == "__main__":
    for slug in slugs[2:]:
        print(slug)
        save_data_from_slug(slug)