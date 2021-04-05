# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from utils.Response import JsonResponse
import numpy as np

from utils.RedisUtil import Redis
from influxdb import InfluxDBClient
import datetime
import json
from dynamic.models import PhAvgMonthData
from config.models import PhConfigUseRange
import copy
from config.models import PhDefinedModule
import random

np.seterr(divide='ignore', invalid='ignore')


def range_to_dict(stop_list):
    """
    通过start和stop得到初始dict
    :param stop_list:
    :return:
    """
    result = {}
    for item in stop_list:
        result[item] = 0
    return result


def count_use_range(all_use_dict, use_dict, use_value):
    """
    计算value是否在dict的key中，在则加1
    :param all_use_dict:
    :param use_dict:
    :param use_value:
    :return:
    """
    for key in use_dict:
        if key[0] <= use_value < key[1]:
            use_dict[key] = use_dict[key] + 1
            all_use_dict[key] = all_use_dict[key] + 1
    return all_use_dict, use_dict


def update_key_dict(use_dict):
    keys = copy.copy(use_dict)
    for key in keys:
        new_key = '[' + str(key[0]) + ',' + str(key[1]) + ')'
        use_dict.update({new_key: use_dict.pop(key)})
    return use_dict


def multiple_list(x, y):
    return np.array(x) * np.array(y)


def get_dynamic_data():
    """
    生成已有模块的动态数据信息，存入redis，改进，通过设置的利用率范围来统计动态数据信息
    而不是写死的范围
    :return:
    """

    # 设置晚高峰期时间段
    start = str(datetime.date.today() + datetime.timedelta(days=-1)) + ' 20:00:00'
    end = str(datetime.date.today() + datetime.timedelta(days=-1)) + ' 22:00:00'

    # 连接redis数据库，获取要统计的模块
    redis = Redis("default")
    # moduleList = redis.smembers('define_modules')
    moduleList = PhDefinedModule.objects.filter().all().values('module')
    # 连接时序数据库influxDB
    client = InfluxDBClient(host='vot.oa.com', port=8081, database='tnm2')

    # 从数据库中取出利用率范围
    cpuRange = PhConfigUseRange.objects.filter(type='cpu').order_by('sort').all().values_list('start', 'stop')
    memRange = PhConfigUseRange.objects.filter(type='mem').order_by('sort').all().values_list('start', 'stop')
    eth0InRange = PhConfigUseRange.objects.filter(type='eth0_in').order_by('sort').all().values_list('start', 'stop')
    eth0OutRange = PhConfigUseRange.objects.filter(type='eth0_out').order_by('sort').all().values_list('start', 'stop')

    result = {}

    allCpuUseDis = range_to_dict(cpuRange)
    allMemUseDis = range_to_dict(memRange)
    allEth0InUseDis = range_to_dict(eth0InRange)
    allEth0OutUseDis = range_to_dict(eth0OutRange)

    for item in moduleList:
        module = item['module']
        # query_sql = 'SELECT max(cpu),max(mem),max(mem_total), max(eth0_in),max(eth0_out) FROM "machine" WHERE (module =\'' + module + '\'  ) AND time >= \'' + start + '\' AND time <= \'' + end + '\'   GROUP BY lan_ip tz(\'Asia/Shanghai\')'
        # query_data = client.query(query_sql)
        # print(cpuData.raw)
        # series = query_data.raw['series']
        cpuUseDis = range_to_dict(cpuRange)
        memUseDis = range_to_dict(memRange)
        eth0InUseDis = range_to_dict(eth0InRange)
        eth0OutUseDis = range_to_dict(eth0OutRange)
        for i in range(0, 200):
            serie = [random.randint(1, 100), random.randint(1, 100), random.randint(1, 100000), random.randint(1, 100000), ]
            cpuUse = serie[0]
            memUse = serie[1]
            eth0InUse = serie[2]
            eth0OutUse = serie[3]
            allCpuUseDis, cpuUseDis = count_use_range(allCpuUseDis, cpuUseDis, cpuUse)
            allMemUseDis, memUseDis = count_use_range(allMemUseDis, memUseDis, memUse)
            allEth0InUseDis, eth0InUseDis = count_use_range(allEth0InUseDis, eth0InUseDis, eth0InUse)
            allEth0OutUseDis, eth0OutUseDis = count_use_range(allEth0OutUseDis, eth0OutUseDis, eth0OutUse)

        # 修改dict的key
        cpuUseDis = update_key_dict(cpuUseDis)
        memUseDis = update_key_dict(memUseDis)
        eth0InUseDis = update_key_dict(eth0InUseDis)
        eth0OutUseDis = update_key_dict(eth0OutUseDis)

        cpuUseDis = {'x': list(cpuUseDis.keys()), 'y': list(cpuUseDis.values())}
        memUseDis = {'x': list(memUseDis.keys()), 'y': list(memUseDis.values())}
        eth0InUseDis = {'x': list(eth0InUseDis.keys()), 'y': list(eth0InUseDis.values())}
        eth0OutUseDis = {'x': list(eth0OutUseDis.keys()), 'y': list(eth0OutUseDis.values())}
        result[module] = {'cpuUseDis': cpuUseDis, 'memUseDis': memUseDis, 'eth0InUseDis': eth0InUseDis,
                          'eth0OutUseDis': eth0OutUseDis}

    allCpuUseDis = update_key_dict(allCpuUseDis)
    allMemUseDis = update_key_dict(allMemUseDis)
    allEth0InUseDis = update_key_dict(allEth0InUseDis)
    allEth0OutUseDis = update_key_dict(allEth0OutUseDis)
    allCpuUseDis = {'x': list(allCpuUseDis.keys()), 'y': list(allCpuUseDis.values())}
    allMemUseDis = {'x': list(allMemUseDis.keys()), 'y': list(allMemUseDis.values())}
    allEth0InUseDis = {'x': list(allEth0InUseDis.keys()), 'y': list(allEth0InUseDis.values())}
    allEth0OutUseDis = {'x': list(allEth0OutUseDis.keys()), 'y': list(allEth0OutUseDis.values())}

    result['汇总数据'] = {'cpuUseDis': allCpuUseDis, 'memUseDis': allMemUseDis, 'eth0InUseDis': allEth0InUseDis,
                      'eth0OutUseDis': allEth0OutUseDis}
    redis.delete('DDODefined')
    redis.set('DDODefined', json.dumps(result))
    print(str(datetime.datetime.now()) + "统计现有模块动态数据完成！")


class DynamicViewSet(viewsets.GenericViewSet):
    """
    取出已定义模块的动态资源数据以及平均值数据，并统计发送给前端
    """

    @action(methods=['get'], detail=False, url_path='getDynamicData')
    def get(self, request, *args, **kwargs):
        get_dynamic_data()
        result = {}
        redis = Redis("default")
        # 从redis中取出动态资源展示分布图数据DDODefined
        DDODefined = redis.get('DDODefined')
        dynamic_data = json.loads(DDODefined)
        result['dynamicData'] = dynamic_data

        redis = Redis("default")
        # moduleList = redis.smembers('define_modules')
        module_list = PhDefinedModule.objects.filter().all().values('module')
        moduleList = []
        for item in module_list:
            moduleList.append(item['module'])

        # 从mysql中查询出每个已定义模块的高峰期平均值趋势数据
        # avgList = PhAvgMonthData.objects.filter(module__in=moduleList).values_list('cpu', 'mem', 'eth0_in', 'eth0_out',
        #                                                                            'machine_count', 'module')

        avgResult = {}  # 保存平均值数据总结果的对象

        # 遍历每一个模块的数据进行处理
        for module in moduleList:
            avgResult[module] = {'cpu': np.random.randint(100, size=30),
                                 'mem': np.random.randint(100, size=30),
                                 'eth0InMonth': np.random.randint(100, size=30),
                                 'eth0OutMonth': np.random.randint(100, size=30), }

        avgResult['汇总数据'] = {'cpu': np.random.randint(100, size=30),
                             'mem': np.random.randint(100, size=30),
                             'eth0InMonth': np.random.randint(100, size=30),
                             'eth0OutMonth': np.random.randint(100, size=30), }
        result['avgData'] = avgResult
        return JsonResponse(20000, '查询成功！', result)
