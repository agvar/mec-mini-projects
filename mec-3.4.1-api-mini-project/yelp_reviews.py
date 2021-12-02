import os
import requests
import json
import csv
from dotenv import load_dotenv


def get_business(params,counter):
    data=[]
    search_url=base_url+search_business_endpoint
    headers={'Authorization': 'Bearer ' + API_KEY}

    if (not os.path.exists(response_file)) or (not os.path.getsize(response_file)) :
            response=requests.get(search_url,params=params,headers=headers)
            print(f"api enpoint used{response.url}")
            with open(response_file,'wb') as f:
                f.write(response.content)
    with open(response_file,'rb') as f:
       shops=json.load(f)
    #response = requests.get(search_url, params=params, headers=headers)
    #shops=json.loads(response.content)
    total_records=shops['total']
    page_length=len(shops['businesses'])

    column_list=['id','alias','name','image_url','is_closed','url','review_count','category_alias','category_title','rating','latitude','longitude','delivery','pickup','price',
                 'address1','address2','address3','city','zip_code','state','country','distance']

    if counter==1:
        with open(output_file,'w') as f:
            wr=csv.writer(f)
            wr.writerow(column_list)
        with open(output_file, 'a') as f:
            wr = csv.writer(f)
            for shop in shops['businesses']:
                data = list(shop.get('id', None), shop.get('alias', None), shop.get('name', None),
                        shop.get('image_url', None), shop.get('is_closed', None), shop.get('url', None),
                        shop.get('review_count', None)#, shop.get('categories'[0]['alias'], None),
                        #shop.get('categories'[0]['title'],None)
                        , shop.get('rating', None),
                        shop.get('coordinates'['latitude'], None), shop.get('coordinates'['longitude'], None),
                        bool(shop.get('transactions'[0], 0)), bool(shop.get('transactions'[1], 0)),
                                  shop.get('price',None),
                        shop.get('location'['address1'], None), shop.get('location'['address2'], None),
                        shop.get('location'['address3'], None), shop.get('location'['city'], None),
                        shop.get('location'['zip_code'], None), shop.get('location'['state'], None),
                        shop.get('location'['country'], None), shop.get('distance', None))
                print(data)
                wr.writerow(data)
                counter+=1
    return page_length,total_records,counter

if __name__=="__main__":
    offset=1
    total_records=2
    counter=1
    load_dotenv()
    API_KEY = os.getenv('YELP_API_KEY')
    response_file='response.json'
    output_file='yelp_business.csv'
    base_url = "https://api.yelp.com/v3"
    search_business_endpoint = "/businesses/search"
    reviews_endpoint = "/businesses/{id}/reviews"
    while offset<total_records :
        params = {'location': 'San Francisco', 'term': 'food', 'offset': offset-1}
        page_length, total_records,counter = get_business(params,counter)
        offset=offset-1 +page_length
        print(f"total records:{total_records},offset:{offset},counter:{counter}")
