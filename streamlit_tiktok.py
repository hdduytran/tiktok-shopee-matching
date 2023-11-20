from Parallelizer import make_parallel
from common import  Common
import re
import pandas as pd
import time
from urllib.parse import unquote
from utils import *
import json
from math import ceil
import streamlit as st
import requests
from bs4 import BeautifulSoup
from time import sleep
from io import BytesIO

count = 0

# @make_parallel
def request_tiktok(url):
    payload = {}
    headers = {
        'authority': 'oec-api.tiktokv.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'
    }
    try_time = 0
    json_obj = None
    while not json_obj:
        
        # url = f"https://oec-api.tiktokv.com/view/product/{product_id}"
        response = requests.request("GET", url, headers=headers, data=payload)
        try_time += 1
        print(f"{try_time}: {url}")
        try:
            soup = BeautifulSoup(response.text, 'html.parser')

            # get content of script id = RENDER_DATA
            script = soup.find('script', id='RENDER_DATA')
            # get content of script
            script_content = script.contents[0]
            # get data from script
            # print(response.text)
            json_obj = json.loads(unquote(script_content))
            # print(json_obj)
        except Exception as e:
            print(e)
            json_obj = None
            print(f"fail: {url} {response.text}")
            sleep(2)
    return json_obj
# @make_parallel
def transform(response, results=[]):

    product_transformed = {
        "product_id": "failed",
        "name": "failed",
        "link": "failed",
        "type": "Sp lẻ",
        "min_price": "failed",
        "max_price": "failed",
        "sold_count": "failed",
        "min_original_price": "failed",
        "max_original_price": "failed",
    }
    
    for i in range(5):
        product_transformed[f"image_{i+1}"] = "failed"

    try:
        product_base = response['2']['initialData']['productInfo']['product_base']
        mapping_product_base = {
            "real_price": ["price", "real_price"],
            "original_price": ["price", "original_price"],
            "images": ["images"],
            "sold_count": ["sold_count"],
            "title": ["title"]
        }
        transformed_product_base = Common.mapping_data(
            product_base, mapping_product_base)
        product_id = response['2']['initialData']['productInfo']['product_id']
        print(product_id)
        name = transformed_product_base['title']
        price_pattern = re.compile(r'(\d+\.?\d*)')
        prices = price_pattern.findall(transformed_product_base['real_price'])
        if len(prices) == 2:
            min_price = int(prices[0].replace('.', ''))
            max_price = int(prices[1].replace('.', ''))
        else:
            min_price = None
            max_price = int(prices[0].replace('.', ''))

        original_price = price_pattern.findall(
            transformed_product_base['original_price'])
        if len(original_price) == 2:
            min_original_price = int(original_price[0].replace('.', ''))
            max_original_price = int(original_price[1].replace('.', ''))
        else:
            min_original_price = None
            if len(original_price) == 0:
                max_original_price = None
            else:
                max_original_price = int(original_price[0].replace('.', ''))

        sold_count = transformed_product_base['sold_count']

        images = [None]*5
        for i,image in enumerate(transformed_product_base["images"][:5]):
            images[i] = f'=image("{image["thumb_url_list"][0]}")'

        product_transformed = {
            "product_id": product_id,
            "name": name,
            "link": f"https://oec-api.tiktokv.com/view/product/{product_id}",
            "type": "Sp lẻ",
            "min_price": min_price,
            "max_price": max_price,
            "sold_count": sold_count,
            "min_original_price": min_original_price,
            "max_original_price": max_original_price,
        }
        
        for i in range(5):
            product_transformed[f"image_{i+1}"] = images[i]
            
    except Exception as e:
        print(e)
        if product_id:=response['_location'].split('/')[-1]:
            product_transformed["product_id"] = product_id
            product_transformed['link'] =  f"https://oec-api.tiktokv.com/view/product/{product_id}"
            print(f"failed {product_id}")

    results.append(product_transformed)
    
state = st.session_state
    
    
links = st.text_area("Nhập link sản phẩm cần lấy thông tin mỗi link một dòng",
                     "https://oec-api.tiktokv.com/view/product/1729652819415631982\nhttps://oec-api.tiktokv.com/view/product/1729572702090856558", 
                     height=200).strip().split('\n')
btn_get_info = st.button("Lấy thông tin")



if btn_get_info:
    with st.empty():
        product_infos = []
        results = []
        for link in links:
            product = request_tiktok(link)
            product_infos.append(product)
            print(len(product_infos))
            transform(product, results)
            df = pd.DataFrame(results)  
            st.dataframe(df)
            
    output = BytesIO()
    df.to_csv(output, index=False)        
        
    st.download_button(
        label="Download data as CSV",
        data=output.getvalue(),
        file_name='tiktok.csv',
        mime='text/csv'
    )
    
    st.markdown("""
                - Copy table and past to google sheet (Ctrl + A -> Ctrl + C -> Ctrl + V)
                - Or download csv file and upload to google sheet (File -> Import -> Upload)
                - Warning: should not open csv file with excel
                """)