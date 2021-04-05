
import datetime
import json
import requests


def get_abnormal_removal_ip_delta():
    """
    根据参数delta(天数)计算属于直播平台的模块中异常剔除次数（在云雀中被剔除的机器数）,共10个平台，统计包括异常剔除、异常反复剔除
    :param delta:
    :param module_name:
    :return:
    """
    delta = 3
    module_name = '[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播平台L1]'
    global zhibo_module_list
    zhibo_module_list = []
    for i in range(1, 10):
        zhibo_module_list.append('[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播平台L' + str(i) + ']')
    zhibo_module_list.append('[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播突发池]')
    module_yunque_list = []
    for i in range(1, 10):
        module_yunque_list.append('[腾讯云直播-OC-国内][L' + str(i) + '][OC]')
    module_yunque_list.append('[腾讯云直播-OC-国内][Ltf][OC]')

    module_yunque = module_yunque_list[zhibo_module_list.index(module_name)]

    url = 'http://10.56.216.194/api/cdn_exception_collection/action_query/'

    new_abnormal_removal = []
    new_abnormal_repeat_removal = []
    # 循环取过去delta天的数据

    for i in range(1, delta + 1):
        start = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 00:00'
        end = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 23:59'
        headers = {
            'qf-api-token': 'iDYt62f3Q_xfFD6otFzsag'
        }
        post_data = {
            'page': 1,
            'limit': 100000,
            'action_type': 1,
            'time_range': f'{start} - {end}',

        }

        response = requests.post(url=url, headers=headers, data=json.dumps(post_data))
        if not response.ok:
            print(module_name, "异常剔除请求异常")
        data = json.loads(response.text)['data']['data_list']
        data = [item for item in data if item['platform_name'] == module_yunque]
        new_abnormal_removal.append(len(data))
        ips = {}
        for item in data:
            ip = item['action_object_name']
            ips[ip] = ips.get(ip, 0) + 1
        # 过滤出反复被剔除的机器，即剔除次数>=2
        ips = {k: v for (k, v) in ips.items() if v >= 2}
        new_abnormal_repeat_removal.append({"count": len(ips), "ips": ips})

        new_abnormal_removal.append(0)
        new_abnormal_repeat_removal.append({"count": 0, "ips": {}})

    # print(module_name, "异常剔除数据统计完成！")
    return new_abnormal_removal[::-1], new_abnormal_repeat_removal[::-1]


if __name__ == "__main__":

    get_abnormal_removal_ip_delta()