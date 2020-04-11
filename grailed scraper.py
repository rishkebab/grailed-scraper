import pandas as pd
import requests
import json

designer_list = pd.read_csv('/Users/rish/PycharmProjects/Grailed Scraper/designers_cleaned.csv')

url = 'https://mnrwefss2q-2.algolianet.com/1/indexes/*/queries'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

params = {
    'x-algolia-agent': 'Algolia for vanilla JavaScript 3.35.1;instantsearch.js 6.3.0;JS Helper 3.1.0',
    'x-algolia-application-id': 'MNRWEFSS2Q',
    'x-algolia-api-key': 'a3a4de2e05d9e9b463911705fb6323ad'}

for n in range(0,874):
    start = n*10
    finish = (n+1)*10

    all_df = pd.DataFrame()

    for i in range(start,finish):

        designer = (designer_list.iloc[i]['name'])
        page_limit = (designer_list.iloc[i]['pages'])
        term = (designer_list.iloc[i]['term'])

        data = {"requests": [{"indexName": "Listing_by_heat_production",
                              "params": "highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight"
                                        "-0000000000%3E&maxValuesPerFacet=100&hitsPerPage=1000&filters=&page=0&query=&facets=%5B%22designers.name%22%2C%22category_size%22%2C%22category_path%22%2C%22price_i"
                                        "%22%2C%22condition%22%2C%22location%22%2C%22badges%22%2C%22strata%22%5D&tagFilters"
                                        "=&facetFilters=%5B%5B%22designers.name%3A" + term + "%22%5D%5D&numericFilters=%5B%2"
                                        "2price_i%3E%3D0%22%2C%22price_i%3C%3D99999%22%5D"}]}

        jsondata = json.dumps(data)

        json_object = requests.post(url, data=jsondata, params=params).json()

        foo = pd.json_normalize(json_object['results'][0]['hits'])
        foo = pd.DataFrame(foo)

        all_df = all_df.append(foo)
        all_df.to_csv("/Users/rish/PycharmProjects/Grailed Scraper/datasets/raw/product_info " + str(start) + "-" + str(finish) + ".csv")
        print("Designer " + str(i) + "/" + str(finish) + ": " + designer + " Complete!")