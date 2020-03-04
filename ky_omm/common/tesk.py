import requests
import re

class Tesk_digg():
    def __init__(self, url):
        self.dy_url = url
        # self.proxies = {'https':'https://{}:{}'.format('58.218.200.229','9157'),
        #                 'http':'http://{}:{}'.format('58.218.200.229','9157')}


    def get_item_id(self):
        try:
            if self.dy_url.isdigit():
                self.item_id = self.dy_url
            elif "www.dyshortvideo.com" in self.dy_url:
                self.item_id = self.dy_url.split("/")[5]
            elif "v.douyin.com" in self.dy_url:
                self.item_id = self.__short_url_to_item_id(
                    self.dy_url.split("/")[3]
                )
            else:
                raise RuntimeError("order`s dy_url is error, {}".format(
                    self.dy_url
                ))
            return self.item_id
        except:
            return False

    def __short_url_to_item_id(self, short_url_key):
        try:
            url = "http://v.douyin.com/{}/".format(short_url_key)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close',
                'Upgrade-Insecure-Requests': '1',
            }
            res = requests.get(
                url,
                headers=headers,
                # proxies=self.proxies,
                allow_redirects=False
            )
            if res.status_code == 302:
                return res.headers["Location"].split("/")[5]
        except:
            return False

    def get_order_digg_number(self):
        try:
            url = "https://www.dyshortvideo.com/share/video/{}/".format(
                self.item_id
            )
            headers = {
                'Connection': 'close',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; EVA-AL10 Build/HUAWEIEVA-AL10; wv) AppleWebKit/537.36 ('
                              'KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 aweme_710 '
                              'JsSdk/1.0 NetType/WIFI Channel/tianzhuo_dy_dsg app_version/7.1.0 ByteLocale/zh-Hans-CN '
                              'Region/CN',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.9',
                'X-Requested-With': 'com.ss.android.ugc.aweme'
            }
            res = requests.get(
                url,
                headers=headers,
                timeout=1
                # proxies=self.proxies
            )
            dytk = re.search(
                re.compile('dytk: "(.*?)" }\);', re.S),
                res.text
            ).group(1)
            digg_num_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&dytk={}".format(
                self.item_id, dytk
            )
            digg_num_headers = {
                'Connection': 'close',
                'Pragma': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; EVA-AL10 Build/HUAWEIEVA-AL10; wv) AppleWebKit/537.36 ('
                              'KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 aweme_710 '
                              'JsSdk/1.0 NetType/WIFI Channel/tianzhuo_dy_dsg app_version/7.1.0 ByteLocale/zh-Hans-CN '
                              'Region/CN',
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.9'
            }
            res = requests.get(digg_num_url,
                               headers=digg_num_headers,
                               timeout=1
                               )
            if res.status_code == 200:
                json_data = res.json()
                if json_data["status_code"] == 0:
                    item_list = res.json()["item_list"]
                    if item_list:
                        return item_list
        except Exception as e:
            # print(e)
            return False


# item_id = Tesk_digg(6726834427676069128)
# item_id.get_item_id()
# data = item_id.get_order_digg_number()
# print(data)


