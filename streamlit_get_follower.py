from io import BytesIO
from Parallelizer import make_parallel
from common import Common
import re
import pandas as pd
import time
from urllib.parse import unquote
from utils import *
import json
from math import ceil
import requests
from bs4 import BeautifulSoup
from time import sleep
import streamlit as st
count = 0


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
            script = soup.find(
                'script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
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


def transform(json_obj):
    path = ["__DEFAULT_SCOPE__","webapp.user-detail","userInfo","stats","followerCount"]
    follower_count = Common.get_dict_data_by_path(json_obj, path)
    return follower_count


links = st.sidebar.text_area("Enter links", value="", height=200)
links = links.split(" ")

button = st.sidebar.button("Get followers")


if button:
    with st.empty():
        followers = []
        results = []
        for link in links:
            res = request_tiktok(link)
            st.write(res)
            print(json.dumps(res))
            follower = transform(res)
            results.append({"link": link, "follower": follower})

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
