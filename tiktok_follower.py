import requests

url = "https://www.tiktok.com/api/user/detail/?WebIdLastTime=1673495373&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-GB&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F119.0.0.0%20Safari%2F537.36%20Edg%2F119.0.0.0&channel=tiktok_web&cookie_enabled=true&device_id=7187607819578230278&device_platform=web_pc&focus_state=true&from_page=user&history_len=2&is_fullscreen=false&is_page_visible=true&language=en&os=windows&priority_region=VN&referer=&region=VN&screen_height=864&screen_width=1536&secUid=MS4wLjABAAAAUPRpL0F6cospoO4n3PyleV9plhc9mYFGWaUnTsxD3Ykjh2jYjl_wXOEpMEBzPpZP&tz_name=Asia%2FSaigon&uniqueId=norinpham_m4&webcast_language=en&msToken=_2svmzV-dNCAC_MQ1WRUe4brNGfmOt08ctSFmYlaj4qOi__k86iGMgr3mT_zMvFky-tfCyhlM1TU_de8b1y1xQ4pgHZMoLyJ5T-OAFrWxecJ89TlpXHGZJD6Iiz7veamqr0TakwaylES7ewUn7U=&X-Bogus=DFSzswVYsgJANcR2tzlsBU9WcBjK&_signature=_02B4Z6wo000015Ddm3gAAIDDkN2bePcKDLuQ3Z.AAIFc5c"

payload = {}
headers = {
  'authority': 'www.tiktok.com',
  'accept': '*/*',
  'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
  'referer': 'https://www.tiktok.com/^@norinpham_m4',
  'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
