import random
import time
import requests
from urllib.parse import urlencode
from pymongo import MongoClient
from libs.agency.config_helper import IniFileHelper
from libs.agency.too import Proxy_supplier, ProxyCityInfo, ProxyIPType, ProxyProtocol, ProxyTime, ProxyYYS

# 阻止requests警告
requests.packages.urllib3.disable_warnings()


def find_city_in_city_info(region):
    '''
    获取城市
    :param region: 城市
    :return:
    '''
    try:
        return ProxyCityInfo[region].value[0], ProxyCityInfo[region].value[1], region
    except:
        region = (random.choice(list(ProxyCityInfo))).name
        return ProxyCityInfo[region].value[0], ProxyCityInfo[region].value[1], region


class ProxyHelper:
    def __init__(self, Proxy_supplier: Proxy_supplier = Proxy_supplier.ZHIMA):
        # 配文件
        self.__config = IniFileHelper()  # 文件名
        self.__database = MongoClient(self.__config.get_val('DBClientInfo.host'),
                                      self.__config.get_val('DBClientInfo.port', True))[
            self.__config.get_val('DBClientInfo.databasename')]

        self.__proxy_s5_client = self.__database[self.__config.get_val('ProxyInfo.s5tablename')]  # 成功后的IP
        self.__proxy_s5_err_client = self.__database[self.__config.get_val('ProxyInfo.s5etablename')]  # 失败的IP
        self.__proxy_tcp_client = self.__database[self.__config.get_val('ProxyInfo.tcptablename')]  # http IP 库
        self.__proxy_supplier = Proxy_supplier  # 获取来源

    def __update_database_proxy_infos(self,
                                      region: str = None,
                                      ip_type: ProxyIPType = ProxyIPType.IP_Dircet,  # 直连
                                      time: ProxyTime = ProxyTime.Minute5_25,
                                      yys=ProxyYYS.UnLimited,
                                      protocol: ProxyProtocol = ProxyProtocol.HTTPS,
                                      ):
        # 如果1个都没找到就获取
        url = ProxyHelper.__get_url_for_type(ip_type)
        if yys is str:
            yys = ProxyYYS[yys]
        pro, city, region = find_city_in_city_info(region)
        if url != "":
            param = {
                "num": 10,  # 每次获取100个IP
                "pro": pro,
                "city": city,
                "yys": 0,  # yys.value,
                "port": protocol.value,
                "time": time.value[0],
                "type": 2,  # 返回类型为JSON
                "ts": 1,  # 显示IP过期时间
                "ys": 1,  # 显示IP运营商
                "cs": 1,  # 显示IP位置
                "mr": 2  # 单日去重
            }
            try:
                # 将字典编码成URL ?xxx=xxx
                url += urlencode(param)
                result = requests.get(url)
                if result.status_code == 200:
                    data_json = result.json()
                    if data_json["success"]:
                        for data in data_json["data"]:
                            proxy_info = {
                                "ip": data["ip"],
                                "port": data["port"],
                                "expire_time": data["expire_time"],
                                "city": data["city"],
                                "isp": data["isp"]
                            }
                            self.__proxy_tcp_client.insert(proxy_info)
                        return True
                else:
                    print(result.text)
            except Exception as ex:
                print('err:'+ ex)

    def __get_proxy_s5(self):
        '''
        单个s5代理提取
        :return: 查看 proxy_return_format 方法  Ctrl + F
        '''

        # 穷举数据库内的数据直到无数据返回None
        for data in self.__proxy_s5_client.find():
            try:
                proxies = {"http": "socks5://{}:{}@{}:{}".format(data['user'], data['pwd'], data['ip'], data['port']),
                           "https": "socks5://{}:{}@{}:{}".format(data['user'], data['pwd'], data['ip'], data['port'])}
                res = requests.get(url="https://www.douyin.com/",
                                   proxies=proxies,
                                   verify=False,
                                   timeout=10)
                if res.status_code == 200:
                    # 返回统一格式的proxy数据
                    return self.proxy_return_format(data['ip'], data['port'], user=data['user'], pwd=data['pwd'])
            except Exception as ep:
                print(ep)
                self.__proxy_s5_err_client.insert_one(data)
                self.__proxy_s5_client.find_one_and_delete(data)
        return None

    def __get_proxy_tcp(self):
        """
        从数据库中随机获取 http 代理
        :return: 查看 proxy_return_format 方法  Ctrl + F
        """
        proxy_infos = self.__proxy_tcp_client.find()
        if proxy_infos:
            for data in proxy_infos:
                expire_time = data["expire_time"]
                # 检测时间,如果时间不足3分钟就剔除
                if time.mktime(time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")) - time.time() < 60 * 3:
                    self.__proxy_tcp_client.delete_one(data)
                else:
                    self.__proxy_tcp_client.delete_one(data)
                    # 返回统一格式的proxy数据
                    return self.proxy_return_format(data['ip'], data['port'], data['expire_time'], data['city'],
                                                    data['isp'])

        if self.__update_database_proxy_infos():
            return self.__get_proxy_tcp()
        return False

    def __get_proxy_tcp_by_region(self, region):
        """
        从数据库中按城市获取 http 代理
        :param region:
        :return: 查看 proxy_return_format 方法  Ctrl + F
        """
        proxy_infos = self.__proxy_tcp_client.find({"city": region})
        if proxy_infos:
            for data in proxy_infos:
                expire_time = data["expire_time"]
                # 检测时间,如果时间不足3分钟就剔除
                if time.mktime(time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")) - time.time() < 60 * 3:
                    self.__proxy_tcp_client.delete_one(data)
                else:
                    self.__proxy_tcp_client.delete_one(data)
                    # 返回统一格式的proxy数据
                    return self.proxy_return_format(data['ip'], data['port'], data['expire_time'], data['city'],
                                                    data['isp'])

        if self.__update_database_proxy_infos(region):
            return self.__get_proxy_tcp_by_region(region)

    def get_proxy_ip_random(self):
        """
        暴露的集成方法—随机获取代理
        :return: 查看 proxy_return_format 方法  Ctrl + F
        """

        # 按类型获取
        if self.__proxy_supplier == Proxy_supplier.SOCKS5:
            return self.__get_proxy_s5()
        else:
            return self.__get_proxy_tcp()

    # 规定地区取代理，不传值就随便取值
    def get_proxy_ip_by_region(self, region: str):
        '''
        暴露的集成方法—在制定城市地址中随机获取代理
        :param region:城市
        :return: 查看 proxy_return_format 方法  Ctrl + F
        '''
        # 保持接口的一致性，socks5无地区所以同等于调用 get_proxy_ip_random()
        if self.__proxy_supplier == Proxy_supplier.SOCKS5:
            return self.__get_proxy_s5()

        else:
            # 首先检测数据库中是否有指定地区的IP
            if not region:
                region = find_city_in_city_info(region)[2]
            return self.__get_proxy_tcp_by_region(region)

    @staticmethod
    def __get_url_for_type(ip_type):
        url = ""
        if ip_type == ProxyIPType.IP_Dircet:
            url = "http://webapi.http.zhimacangku.com/getip?"
        elif ip_type == ProxyIPType.IP_Tunnel:
            url = "http://http.tiqu.alicdns.com/getip3?"
        elif ip_type == ProxyIPType.IP_Debicated:
            url = "http://http.tiqu.alicdns.com/getip3?"
        return url

    @staticmethod
    def get_random_city():
        return (random.choice(list(ProxyCityInfo))).name

    def proxy_return_format(self, ip, port, expire_time=None, city=None, isp=None, user=None, pwd=None):
        return {'ip': ip, 'port': port, 'expire_time': expire_time, 'city': city, 'isp': isp,
                'user': user, 'pwd': pwd}


if __name__ == '__main__':
    proxy = ProxyHelper(Proxy_supplier=Proxy_supplier.ZHIMA)
    print(proxy.get_proxy_ip_random())
