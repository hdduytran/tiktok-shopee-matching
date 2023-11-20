
import re
def convert_price(price):
    if price and type(price) == str:
        price_characters = ["K", "M", "B"]
        for i, character in enumerate(price_characters):
            if character in price or character.lower() in price:
                price = price.replace(character, "0" * (3 - i))
                price = price.replace(character.lower(), "0" * (3 - i))
                break
        if "," in price:
            price = price.replace(",", "")
            price = price[:-1]
    return price


def parse_input(path_string):
    output = []
    for i in path_string.split('.'):
        if '[' in i:
            output += map(lambda x: int(x) if x.isdigit() else x, i.replace(']', '').split('['))
        else:
            output.append(i)
    return output

def transform_link(input, shop_id, product_id):
    # input: str = "Áo Thun Ngắn Tay Nam ATINO chất liệu 100% Cotton thoáng mát form Regular - Áo Phông Cộc Tay AP2.2103"
    # output: str = "Áo-Thun-Ngắn-Tay-Nam-ATINO-chất-liệu-100-Cotton-thoáng-mát-form-Regular-Áo-Phông-Cộc-Tay-AP2.2103-i.439115986.12098818105"

    # remove special characters
    input = re.sub(r'[^\w\s\.]', '', input)
    # remove multiple spaces
    input = re.sub(r'\s+', '-', input)
    # remove last - if exist
    input = re.sub(r'-+$', '', input)

    return f"https://shopee.vn/{input}-i.{shop_id}.{product_id}"

    