""""
    验证请求模块
"""
import hashlib
import requests
from urllib.parse import unquote
import time


def _sig(url_params, body):
    data = url_params + '&' + body
    data = unquote(data)
    array = data.split("&")
    array.sort()
    string = ''.join(array) + "382700b563f4"
    strs = hashlib.md5()
    strs.update((string).encode('utf8'))
    sig = strs.hexdigest()
    return sig


def photo_info(id):
    url = "http://103.107.217.65/rest/n/photo/info2?"
    url_params = ("isp=CMCC&mod=Xiaomi%20%28MI%205%20%29&lon=116.41025&country_code=cn&kpf=ANDROID_PHONE&did={did}"
                  "&kpn=KUAISHOU&net=WIFI"
                  "&app=0&oc=GENERIC&ud={ud}&hotfix_ver=&c=GENERIC&sys=ANDROID_5.1.1&appver=6.4.0.9003&ftt="
                  "&language=zh-cn&iuid=&lat=39.916411"
                  "&ver=6.4&max_memory=192").format(did="ANDROID_a775335f13ecb3ae", ud='')
    _body = ("photoInfos=%5B%7B%22photoId%22%3A%22{photo_Id}%22%7D%5D&client_key=3c2cd3f3"
             "&token={token}&os=android").format(photo_Id=id, token='')
    sig = _sig(url_params, _body)
    body = _body + "&sig={sig}".format(sig=sig)
    headers = {
        "Cookie": "token={token}".format(token=''),
        "User-Agent": "kwai-android",
        "X-REQUESTID": "109294749",
        "Connection": "close",
        "Accept-Language": "zh-cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "608",
        "Host": "apissl.gifshow.com"
    }
    url = url + url_params
    try:
        time.sleep(0.15)
        res = requests.post(url, data=body, headers=headers, timeout=1, verify=False)
        data_json = res.json()
        result = data_json.get('result', None)
        if result == 2:
            error_msg = data_json.get('error_msg', None)
            return {'status': 404, 'msg': error_msg}

        if result == 224:
            error_msg = data_json.get('error_msg', None)
            return {'status': 404, 'msg': error_msg}

        view_count = data_json.get('photos')[0].get('view_count')
        photo_id = data_json.get('photos')[0].get('photo_id')
        user_id = data_json.get('photos')[0].get('user_id')
        user_name = data_json.get('photos')[0].get('user_name')
        return {
            'status': 200,
            'view_count': view_count,
            'photo_id': photo_id,
            'user_id': user_id,
            'user_name': user_name
        }
    except Exception as e:
        return {'status': 404, 'msg': e}


if __name__ == '__main__':
    res1 = photo_info("3x3mu65sh4ww3q2")
    print(res1)
