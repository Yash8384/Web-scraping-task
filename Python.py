import requests
from lxml import html
from PIL import Image
from io import BytesIO
import json

class TinxsysScraper:
    def __init__(self, tin_number):
        self.tin_number = tin_number
        self.url = 'https://tinxsys.com/TinxsysInternetWeb/searchByTin_Inter.jsp'
        self.session = requests.Session()

    def fetch_captcha(self):
        response = self.session.get(self.url)
        tree = html.fromstring(response.content)
        captcha_img_url = tree.xpath('//img[@id="captchaImg"]/@src')[0]
        captcha_img_response = self.session.get(f'https://tinxsys.com/TinxsysInternetWeb/{captcha_img_url}')
        img = Image.open(BytesIO(captcha_img_response.content))
        img.show()
        captcha_value = input("Enter CAPTCHA value: ")
        return captcha_value

    def get_dealer_info(self):
        captcha_value = self.fetch_captcha()
        payload = {
            'tinNumber': self.tin_number,
            'captchaCode': captcha_value,
            'searchType': 'Search'
        }
        response = self.session.post(self.url, data=payload)
        tree = html.fromstring(response.content)
        data = {
            'tin_number': self.tin_number,
            'cst_number': tree.xpath('//td[text()="CST Number"]/following-sibling::td/text()')[0].strip(),
            'dealer_name': tree.xpath('//td[text()="Dealer Name"]/following-sibling::td/text()')[0].strip(),
            'dealer_address': tree.xpath('//td[text()="Dealer Address"]/following-sibling::td/text()')[0].strip(),
            'state_name': tree.xpath('//td[text()="State Name"]/following-sibling::td/text()')[0].strip(),
            'pan_number': tree.xpath('//td[text()="PAN Number"]/following-sibling::td/text()')[0].strip(),
            'registration_date': tree.xpath('//td[text()="Date of Registration"]/following-sibling::td/text()')[0].strip(),
            'valid_upto': tree.xpath('//td[text()="Valid Upto"]/following-sibling::td/text()')[0].strip(),
            'registration_status': tree.xpath('//td[text()="Registration Status"]/following-sibling::td/text()')[0].strip()
        }
        return data

    def to_json(self):
        data = self.get_dealer_info()
        return json.dumps(data, indent=4)

if __name__ == '__main__':
    tin_number = '21711100073'
    scraper = TinxsysScraper(tin_number)
    print(scraper.to_json())
