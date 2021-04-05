import os
import django
from utils.RedisUtil import Redis
from influxdb import InfluxDBClient
import datetime
import json
from anomaly_analysis.models import PhAnomalyAnalysis
import requests
from config.models import PhDefinedModule


def count_anomaly_analysis():
    """
    统计平台异常数据
    :return:
    """
    redis = Redis("default")
    # module_list = redis.smembers('define_modules')
    module_list = PhDefinedModule.objects.filter().all().values('module')

    today = datetime.date.today()

    global zhibo_module_list
    zhibo_module_list = []
    for i in range(1, 10):
        zhibo_module_list.append('[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播平台L' + str(i) + ']')
    zhibo_module_list.append('[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播突发池]')

    # module_list = ['[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播平台L2]']
    for item in module_list:
        module_name = item['module']
        module_data = PhAnomalyAnalysis.objects.filter(module=module_name).all()
        # 该模块的数据已经存在，按照日期更新缺少的数据
        if len(module_data) > 0:
            module_data = module_data.get()
            update_date = module_data.update_date

            delta = (today - update_date).days
            # load data old
            # old_high_load_cpu = module_data.high_load_cpu

            old_high_load_cpu = json.loads(json.dumps(eval(module_data.high_load_cpu)))
            old_high_load_mem = json.loads(json.dumps(eval(module_data.high_load_mem)))
            old_high_load_eth0_in = json.loads(json.dumps(eval(module_data.high_load_eth0_in)))
            old_high_load_eth0_out = json.loads(json.dumps(eval(module_data.high_load_eth0_out)))

            old_low_load_cpu = json.loads(json.dumps(eval(module_data.low_load_cpu)))
            old_low_load_mem = json.loads(json.dumps(eval(module_data.low_load_mem)))
            old_low_load_eth0_in = json.loads(json.dumps(eval(module_data.low_load_eth0_in)))
            old_low_load_eth0_out = json.loads(json.dumps(eval(module_data.low_load_eth0_out)))

            # offline_device data old
            old_offline_device = json.loads(json.dumps(eval(module_data.offline_device)))

            # alarm data load
            old_alarm_ping = json.loads(json.dumps(eval(module_data.alarm_ping)))
            old_alarm_flow = json.loads(json.dumps(eval(module_data.alarm_flow)))
            old_alarm_performance = json.loads(json.dumps(eval(module_data.alarm_performance)))
            old_alarm_port = json.loads(json.dumps(eval(module_data.alarm_ping)))
            old_alarm_process_port = json.loads(json.dumps(eval(module_data.alarm_process_port)))
            old_alarm_process = json.loads(json.dumps(eval(module_data.alarm_process)))
            old_alarm_report_time_out = json.loads(json.dumps(eval(module_data.alarm_report_time_out)))
            old_alarm_disk = json.loads(json.dumps(eval(module_data.alarm_disk)))
            old_alarm_disk_ro = json.loads(json.dumps(eval(module_data.alarm_disk_ro)))
            old_alarm_disk_ro_full = json.loads(json.dumps(eval(module_data.alarm_disk_ro_full)))

            # load del
            del old_high_load_cpu[0:delta]
            del old_high_load_mem[0:delta]
            del old_high_load_eth0_in[0:delta]
            del old_high_load_eth0_out[0:delta]
            del old_low_load_cpu[0:delta]
            del old_low_load_mem[0:delta]
            del old_low_load_eth0_in[0:delta]
            del old_low_load_eth0_out[0:delta]

            # offline_device del
            del old_offline_device[0:delta]

            # alarm del
            del old_alarm_ping[0:delta]
            del old_alarm_flow[0:delta]
            del old_alarm_performance[0:delta]
            del old_alarm_port[0:delta]
            del old_alarm_process_port[0:delta]
            del old_alarm_process[0:delta]
            del old_alarm_report_time_out[0:delta]
            del old_alarm_disk[0:delta]
            del old_alarm_disk_ro[0:delta]
            del old_alarm_disk_ro_full[0:delta]

            # count data
            new_high_load_cpu, new_high_load_mem, new_high_load_eth0_in, new_high_load_eth0_out \
                , new_low_load_cpu, new_low_load_mem, new_low_load_eth0_in, new_low_load_eth0_out \
                = get_load_ip_delta(delta, module_name)
            new_offline_device = get_offline_device_ip_delta(delta, module_name)

            new_alarm_ping, new_alarm_flow, new_alarm_performance, new_alarm_port, new_alarm_process_port \
                , new_alarm_process, new_alarm_report_time_out, new_alarm_disk, new_alarm_disk_ro, new_alarm_disk_ro_full \
                = get_alarm_ip_delta(delta, module_name)

            # 如果模块属于直播平台的模块，统计异常剔除数
            if module_name in zhibo_module_list:
                old_abnormal_removal = json.loads(json.dumps(eval(module_data.abnormal_removal)))
                old_abnormal_repeat_removal = json.loads(json.dumps(eval(module_data.abnormal_repeat_removal)))

                del old_abnormal_removal[0:delta]
                del old_abnormal_repeat_removal[0:delta]
                new_abnormal_removal, new_abnormal_repeat_removal = get_abnormal_removal_ip_delta(delta, module_name)
                old_abnormal_removal.extend(new_abnormal_removal)
                old_abnormal_repeat_removal.extend(new_abnormal_repeat_removal)
                module_data.abnormal_removal = old_abnormal_removal
                module_data.abnormal_repeat_removal = old_abnormal_repeat_removal

            # load extend
            old_high_load_cpu.extend(new_high_load_cpu)
            old_high_load_mem.extend(new_high_load_mem)
            old_high_load_eth0_in.extend(new_high_load_eth0_in)
            old_high_load_eth0_out.extend(new_high_load_eth0_out)
            old_low_load_cpu.extend(new_low_load_cpu)
            old_low_load_mem.extend(new_low_load_mem)
            old_low_load_eth0_in.extend(new_low_load_eth0_in)
            old_low_load_eth0_out.extend(new_low_load_eth0_out)

            # offline_device extend
            old_offline_device.extend(new_offline_device)

            # alarm extend
            old_alarm_ping.extend(new_alarm_ping)
            old_alarm_flow.extend(new_alarm_flow)
            old_alarm_performance.extend(new_alarm_performance)
            old_alarm_port.extend(new_alarm_port)
            old_alarm_process_port.extend(new_alarm_process_port)
            old_alarm_process.extend(new_alarm_process)
            old_alarm_report_time_out.extend(new_alarm_report_time_out)
            old_alarm_disk.extend(new_alarm_disk)
            old_alarm_disk_ro.extend(new_alarm_disk_ro)
            old_alarm_disk_ro_full.extend(new_alarm_disk_ro_full)

            module_data.high_load_cpu = old_high_load_cpu
            module_data.high_load_mem = old_high_load_mem
            module_data.high_load_eth0_in = old_high_load_eth0_in
            module_data.high_load_eth0_out = old_high_load_eth0_out
            module_data.low_load_cpu = old_low_load_cpu
            module_data.low_load_mem = old_low_load_mem
            module_data.low_load_eth0_in = old_low_load_eth0_in
            module_data.low_load_eth0_out = old_low_load_eth0_out

            module_data.alarm_ping = old_alarm_ping
            module_data.alarm_flow = old_alarm_flow
            module_data.alarm_performance = old_alarm_performance
            module_data.alarm_port = old_alarm_port
            module_data.alarm_process_port = old_alarm_process_port
            module_data.alarm_process = old_alarm_process
            module_data.alarm_report_time_out = old_alarm_report_time_out
            module_data.alarm_disk = old_alarm_disk
            module_data.alarm_disk_ros = old_alarm_disk_ro
            module_data.alarm_disk_ro_full = old_alarm_disk_ro_full

            module_data.offline_device = old_offline_device

            module_data.update_date = today
            module_data.save()

        else:
            new_high_load_cpu, new_high_load_mem, new_high_load_eth0_in, new_high_load_eth0_out \
                , new_low_load_cpu, new_low_load_mem, new_low_load_eth0_in, new_low_load_eth0_out \
                = get_load_ip_delta(30, module_name)

            new_offline_device = get_offline_device_ip_delta(30, module_name)
            new_alarm_ping, new_alarm_flow, new_alarm_performance, new_alarm_port, new_alarm_process_port \
                , new_alarm_process, new_alarm_report_time_out, new_alarm_disk, new_alarm_disk_ro, new_alarm_disk_ro_full \
                = get_alarm_ip_delta(30, module_name)
            module_data = PhAnomalyAnalysis.createPhAnomalyAnalysis(module_name, new_high_load_cpu, new_high_load_mem,
                                                                    new_high_load_eth0_in, new_high_load_eth0_out,
                                                                    new_low_load_cpu,
                                                                    new_low_load_mem, new_low_load_eth0_in,
                                                                    new_low_load_eth0_out,
                                                                    new_offline_device, new_alarm_ping, new_alarm_flow,
                                                                    new_alarm_performance, new_alarm_port,
                                                                    new_alarm_process_port,
                                                                    new_alarm_process, new_alarm_report_time_out,
                                                                    new_alarm_disk, new_alarm_disk_ro,
                                                                    new_alarm_disk_ro_full,
                                                                    today)
            if module_name in zhibo_module_list:
                new_abnormal_removal, new_abnormal_repeat_removal = get_abnormal_removal_ip_delta(30, module_name)
                module_data.abnormal_removal = new_abnormal_removal
                module_data.abnormal_repeat_removal = new_abnormal_repeat_removal
            module_data.save()
    print(str(datetime.datetime.now()) + "异常数据统计完成！")


def get_abnormal_removal_ip_delta(delta, module_name):
    """
    根据参数delta(天数)计算属于直播平台的模块中异常剔除次数（在云雀中被剔除的机器数）,共10个平台，统计包括异常剔除、异常反复剔除
    :param delta:
    :param module_name:
    :return:
    """
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
        if i == 1:
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
        else:
            new_abnormal_removal.append(0)
            new_abnormal_repeat_removal.append({"count": 0, "ips": {}})

    # print(module_name, "异常剔除数据统计完成！")
    return new_abnormal_removal[::-1], new_abnormal_repeat_removal[::-1]


def get_alarm_ip_delta(delta, module_name):
    """
    根据参数delta(天数)计算某个模块的单机告警数据，Ping告警、单机流量告警、单机性能告警、端口告警、进程端口配置告警
    进程告警、上报超时告警、硬盘告警、硬盘只读告警、硬盘只读告警[磁盘满]
    :param delta:
    :param module_name:
    :return:
    """
    alarm_type_list = ['Ping告警', '单机流量告警', '单机性能告警', '端口告警', '进程端口配置告警', '进程告警', '上报超时告警', '硬盘告警', '硬盘只读告警',
                       '硬盘只读告警[磁盘满]']
    # alarm_type_list = ['硬盘告警', '硬盘只读告警',
    #                    '硬盘只读告警[磁盘满]']
    service_group, service, module = module_name.split("-")
    all = []
    for alarm_type in alarm_type_list:
        alarm_data_list = []
        # 循环取过去delta天的数据
        for i in range(1, delta + 1):
            start = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 00:00:00'
            end = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 23:59:59'
            url = 'http://100.119.153.135/new_api/alarm.get_alarm_info'
            params = {
                "type": alarm_type,
                "end_time": end,
                "begin_time": start,
                "dept": "架构平台部",
                "service_group": service_group,
                "service": service,
                "module": module,
                "show_children": "false",
                "subalarm": "false",
                "start": 0,
                "pagesize": 10000
            }
            if i == 1:
                res = requests.get(url, params=params)
                if res.ok:
                    # print(module_name,res.text)
                    data = json.loads(res.text)
                    if not data or data[0] == 0:
                        alarm_data_list.append({"count": 0, "ips": []})
                    else:
                        ips = []
                        for item in data[2]:
                            ips.append(item["ci_name"])
                        alarm_data_list.append({"count": data[0], "ips": ips})
                else:
                    print(module_name, ":alarm_type", "请求异常")
            else:
                alarm_data_list.append({"count": 0, "ips": []})
        all.append(alarm_data_list[::-1])
    # print(module_name, "单机告警数据统计完成！")
    return all


def get_offline_device_ip_delta(delta, module_name):
    """
    根据参数delta(天数)计算某个模块的离线设备数据
    只能统计到当天的数据，所以如果delta > 1，那么今天之前的数据都为空
    :param delta:
    :param module_name:
    :return:
    """
    all_offline_device_ip = []
    for i in range(1, delta):
        all_offline_device_ip.append({'count': 0, 'ips': [],"sns":[]})

    url = 'http://9.25.14.137:8081/api/cgi_gzglv2/auto_deal_offline_v2_get'
    params = {
        'continueStart': 1,
        'continueEnd': 999,
        'groupName': '视频运维组',
        'setType': 2,
        'type': 'notapi',
        'plat_biz': module_name,
        'today_input': datetime.date.today()
    }
    if delta > 0:
        result = requests.get(url, params=params)
        if result.status_code == 200:
            content = json.loads(result.content)
            ips = []
            sns = []
            for item in content['data']:
                ips.append(item['om_eth1IP'])
                sns.append(item['om_sn'])
            all_offline_device_ip.append({"count": len(ips), "ips": ips, "sns": sns})
        else:
            all_offline_device_ip.append({"count": 0, "ips": []})

    # print(module_name, "离线设备数据统计完成！")
    return all_offline_device_ip


def get_load_ip_delta(delta, module_name):
    """
    根据参数delta(天数)计算某个模块的高负载与低负载数据
    :param delta:
    :param module_name:
    :return:
    """
    client = InfluxDBClient(host='vot.oa.com', port=8081, database='tnm2')

    all_new_high_load_cpu = []
    all_new_high_load_mem = []
    all_new_high_load_eth0_in = []
    all_new_high_load_eth0_out = []

    all_new_low_load_cpu = []
    all_new_low_load_mem = []
    all_new_low_load_eth0_in = []
    all_new_low_load_eth0_out = []
    # 循环取过去delta天的数据
    for i in range(1, delta + 1):

        start = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 20:00:00'
        end = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 22:00:00'
        new_high_load_cpu = []
        new_high_load_mem = []
        new_high_load_eth0_in = []
        new_high_load_eth0_out = []
        new_low_load_cpu = []
        new_low_load_mem = []
        new_low_load_eth0_in = []
        new_low_load_eth0_out = []
        count_machine = 0
        if i == 1:
            query_sql = 'SELECT max(cpu),max(mem),max(mem_total), max(eth0_in),max(eth0_out) FROM "machine" WHERE (module =\'' + module_name + '\'  ) AND time >= \'' + start + '\' AND time <= \'' + end + '\'   GROUP BY lan_ip tz(\'Asia/Shanghai\')'
            query_data = client.query(query_sql)
            series = query_data.raw['series']

            # 遍历每个oc机器
            count_machine = len(series)
            for serie in series:
                cpuUse = serie['values'][0][1] if serie['values'][0][1] else 0
                if (serie['values'][0][2] == None) or (serie['values'][0][3] == None):
                    memUse = 0
                else:
                    memUse = (serie['values'][0][2] * 1024 * 100) / serie['values'][0][3]
                eth0InUse = serie['values'][0][4] * 8 / 60 / 1000 if serie['values'][0][4] else 0
                eth0OutUse = serie['values'][0][5] * 8 / 60 / 1000 if serie['values'][0][5] else 0

                if cpuUse >= 80:
                    new_high_load_cpu.append(serie['tags']['lan_ip'])
                elif cpuUse < 20:
                    new_low_load_cpu.append(serie['tags']['lan_ip'])

                if memUse >= 80:
                    new_high_load_mem.append(serie['tags']['lan_ip'])
                elif memUse < 20:
                    new_low_load_mem.append(serie['tags']['lan_ip'])

                if eth0InUse >= 3000:
                    new_high_load_eth0_in.append(serie['tags']['lan_ip'])
                elif eth0InUse < 100:
                    new_low_load_eth0_in.append(serie['tags']['lan_ip'])

                if eth0OutUse >= 3000:
                    new_high_load_eth0_out.append(serie['tags']['lan_ip'])
                elif eth0OutUse < 100:
                    new_low_load_eth0_out.append(serie['tags']['lan_ip'])

        all_new_high_load_cpu.append(
            {"count": len(new_high_load_cpu),
             "count_all": count_machine,
             "ips": new_high_load_cpu})
        all_new_low_load_cpu.append(
            {"count": len(new_low_load_cpu),
             "count_all": count_machine,
             "ips": new_low_load_cpu})
        all_new_high_load_mem.append(
            {"count": len(new_high_load_mem),
             "count_all": count_machine,
             "ips": new_high_load_mem})
        all_new_low_load_mem.append(
            {"count": len(new_low_load_mem),
             "count_all": count_machine,
             "ips": new_low_load_mem})
        all_new_high_load_eth0_in.append(
            {"count": len(new_high_load_eth0_in),
             "count_all": count_machine, "ips": new_high_load_eth0_in})
        all_new_low_load_eth0_in.append(
            {"count": len(new_low_load_eth0_in),
             "count_all": count_machine, "ips": new_low_load_eth0_in})
        all_new_high_load_eth0_out.append(
            {"count": len(new_high_load_eth0_out),
             "count_all": count_machine, "ips": new_high_load_eth0_out})
        all_new_low_load_eth0_out.append(
            {"count": len(new_low_load_eth0_out),
             "count_all": count_machine, "ips": new_low_load_eth0_out})
    # print(module_name, "高负载与低负载数据统计完成！")
    return all_new_high_load_cpu[::-1], all_new_high_load_mem[::-1], all_new_high_load_eth0_in[
                                                                     ::-1], all_new_high_load_eth0_out[::-1] \
        , all_new_low_load_cpu[::-1], all_new_low_load_mem[::-1], all_new_low_load_eth0_in[
                                                                  ::-1], all_new_low_load_eth0_out[::-1]
