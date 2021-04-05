from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from utils.Response import JsonResponse
import json
from anomaly_analysis.models import PhAnomalyAnalysis
from config.models import PhDefinedModule
from config.crontab import schedule
import random
import numpy as np


def deal_with_abnormal_removal_repeat(abnormal_removal_repeat_data):
    """
    处理重复剔除数据
    :param abnormal_removal_repeat_data:
    :return:
    """
    count = []
    ips = []
    repeat_count = []
    for item in abnormal_removal_repeat_data:
        count.append(item['count'])
        ips_with_count = item['ips']
        repeat_count.append(ips_with_count.values())
        ips.append(ips_with_count.keys())
    res = {'count': count, 'ips': ips, 'repeat_count': repeat_count}
    return res


def deal_with_offline_data(offline_data):
    """
    处理离线设备数据
    :return:
    """
    count = []
    ips = []
    sns = []
    for item in offline_data:
        count.append(item['count'])
        ips.append(item['ips'])
        sns.append(item['sns'])

    res = {'count': count, 'ips': ips, 'sns': sns}
    return res


def deal_with_load_data(old_load_data):
    """
    处理负载数据
    :param old_load_data:
    :return:
    """

    ratio = []
    ips = []
    for item in old_load_data:
        if item['count_all'] == 0:
            ratio.append(0)
            ips.append([])
        else:
            r = (item['count'] * 100) / item['count_all']
            ratio.append(round(r, 2))
            ips.append(item['ips'])
    res = {'ratio': ratio, 'ips': ips}
    return res


def deal_with_alarm_data(old_alarm_ping):
    """
    处理告警数据
    :param old_alarm_ping:
    :return:
    """
    count = []
    ips = []
    for item in old_alarm_ping:
        count.append(item['count'])
        ips.append(item['ips'])
    res = {'count': count, 'ips': ips}
    return res


class AnomalyAnalysisViewSet(viewsets.ModelViewSet):
    """
    异常分析数据获取
    """

    def __init__(self, **kwargs):

        module_list = PhDefinedModule.objects.filter().all().values('module')
        moduleList = []
        for item in module_list:
            moduleList.append(item['module'])
        self.abnormal_list = PhAnomalyAnalysis.objects.filter(module__in=moduleList,
                                                              abnormal_removal__isnull=False).values_list('module',
                                                                                                          'abnormal_removal',
                                                                                                          'abnormal_repeat_removal')
        self.anomalyList = PhAnomalyAnalysis.objects.filter(module__in=moduleList).values_list('module',
                                                                                               'high_load_cpu',
                                                                                               'high_load_mem',
                                                                                               'high_load_eth0_in',
                                                                                               'high_load_eth0_out',
                                                                                               'low_load_cpu',
                                                                                               'low_load_mem',
                                                                                               'low_load_eth0_in',
                                                                                               'low_load_eth0_out',
                                                                                               'offline_device',
                                                                                               'alarm_ping',
                                                                                               'alarm_flow',
                                                                                               'alarm_performance',
                                                                                               'alarm_port',
                                                                                               'alarm_process_port',
                                                                                               'alarm_process',
                                                                                               'alarm_report_time_out',
                                                                                               'alarm_disk',
                                                                                               'alarm_disk_ro',
                                                                                               'alarm_disk_ro_full',
                                                                                               )

        self.moduleList = moduleList

    # /godi_ph_api/anomaly_analysis/getAnomalAnalysis
    @action(methods=['get'], detail=False, url_path='getAnomalAnalysis')
    def get_anomal_analysis(self, request, *args, **kwargs):
        res = {}

        high_load_res = {}
        low_load_res = {}
        offline_device_res = {}
        alarm_res = {}
        abnormal_removal_res = {}
        abnormal_removal_repeat_res = {}

        define_modules = PhDefinedModule.objects.filter(is_done=1).all()
        for d_module in define_modules:
            module_name = d_module.module
            high_load_res[module_name] = {'cpu': np.random.randint(100,size=30), 'mem': np.random.randint(100,size=30),
                                          'eth0_in': np.random.randint(100,size=30), 'eth0_out': np.random.randint(100,size=30)}
            low_load_res[module_name] = {'cpu': np.random.randint(100,size=30), 'mem': np.random.randint(100,size=30),
                                         'eth0_in': np.random.randint(100,size=30), 'eth0_out': np.random.randint(100,size=30)}
            offline_device_res[module_name] = np.random.randint(100,size=30)
            alarm_res[module_name] = {'alarm_ping': np.random.randint(100,size=30), 'alarm_flow': np.random.randint(100,size=30),
                                      'alarm_performance': np.random.randint(100,size=30),
                                      'alarm_port': np.random.randint(100,size=30), 'alarm_process_port': np.random.randint(100,size=30),
                                      'alarm_process': np.random.randint(100,size=30),
                                      'alarm_report_time_out': np.random.randint(100,size=30), 'alarm_disk': np.random.randint(100,size=30),
                                      'alarm_disk_ro': np.random.randint(100,size=30),
                                      'alarm_disk_ro_full': np.random.randint(100,size=30)}
            abnormal_removal_res[module_name] = np.random.randint(100, size=30)
            abnormal_removal_repeat_res[module_name] = np.random.randint(100, size=30)

        res['high_load'] = high_load_res
        res['low_load'] = low_load_res
        res['offline_device'] = offline_device_res
        res['abnormal_removal'] = abnormal_removal_res
        res['abnormal_repeat_removal'] = abnormal_removal_repeat_res
        res['alarm'] = alarm_res
        print(res)
        return JsonResponse(20000, '查询成功！', res)

    @action(methods=['get'], detail=False, url_path='getTodayData')
    def getTodayData(self, request, *args, **kwargs):
        high_load_res = {'cpu': random.randint(0,100), 'mem': random.randint(0,100), 'eth0_in': random.randint(0,100), 'eth0_out': random.randint(0,100)}
        low_load_res = {'cpu': random.randint(0,100), 'mem': random.randint(0,100), 'eth0_in': random.randint(0,100), 'eth0_out': random.randint(0,100)}
        offline_device_res = random.randint(0,100)
        alarm_ping_res = random.randint(0,100)
        alarm_flow_res = random.randint(0,100)
        alarm_performance_res = random.randint(0,100)
        alarm_port_res = random.randint(0,100)
        alarm_process_port_res = random.randint(0,100)
        alarm_process_res = random.randint(0,100)
        alarm_report_time_out_res = random.randint(0,100)
        alarm_disk_res = random.randint(0,100)
        alarm_disk_ro_res = random.randint(0,100)
        alarm_disk_ro_full_res = random.randint(0,100)

        abnormal_removal =  random.randint(0,100)
        abnormal_removal_repeat =  random.randint(0,100)


        res = {'high_load': high_load_res, 'low_load': low_load_res, 'offline_device': offline_device_res,
               'abnormal_removal': abnormal_removal, 'abnormal_removal_repeat': abnormal_removal_repeat,
               'alarm_ping_res': alarm_ping_res,
               'alarm_flow_res': alarm_flow_res, 'alarm_performance_res': alarm_performance_res,
               'alarm_port_res': alarm_port_res,
               'alarm_process_port_res': alarm_process_port_res, 'alarm_process_res': alarm_process_res,
               'alarm_report_time_out_res': alarm_report_time_out_res,
               'alarm_disk_res': alarm_disk_res, 'alarm_disk_ro_res': alarm_disk_ro_res,
               'alarm_disk_ro_full_res': alarm_disk_ro_full_res}
        return JsonResponse(20000, "查询成功", res)

    def get_abnormal_removal_today(self):
        abnormal_removal = 0
        abnormal_removal_repeat = 0
        for anomalyItem in self.abnormal_list:
            module_name = anomalyItem[0]
            old_abnormal_removal = json.loads(json.dumps(eval(anomalyItem[1])))
            old_abnormal_repeat_removal = json.loads(json.dumps(eval(anomalyItem[2])))

            abnormal_removal = abnormal_removal + old_abnormal_removal[-1]
            abnormal_removal_repeat = abnormal_removal_repeat + old_abnormal_repeat_removal[-1]['count']
        return abnormal_removal, abnormal_removal_repeat

    def get_abnormal_removal_res(self, *args, **kwargs):

        abnormal_removal_res = {}
        abnormal_removal_repeat_res = {}

        for anomalyItem in self.abnormal_list:
            module_name = anomalyItem[0]
            old_abnormal_removal = json.loads(json.dumps(eval(anomalyItem[1])))
            old_abnormal_repeat_removal = json.loads(json.dumps(eval(anomalyItem[2])))
            old_abnormal_repeat_removal = deal_with_abnormal_removal_repeat(old_abnormal_repeat_removal)
            abnormal_removal_res[module_name] = old_abnormal_removal
            abnormal_removal_repeat_res[module_name] = old_abnormal_repeat_removal

        return abnormal_removal_res, abnormal_removal_repeat_res
