import os
import django
from utils.RedisUtil import Redis
from influxdb import InfluxDBClient
import datetime
import json
from dynamic.models import PhAvgMonthData
from config.models import PhConfigUseRange
import copy
from config.models import PhDefinedModule
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
django.setup()


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


def get_monthly_avg_data():
    """
    统计已有模块的高峰期最大使用率平均数据，如果已存在该模块的数据则更新到昨天，如果不存则统计30天的数据并新增
    :return:
    """

    redis = Redis("default")
    # module_list = redis.smembers('define_modules')
    module_list = PhDefinedModule.objects.filter().all().values('module')
    today = datetime.date.today()
    for item in module_list:
        module_name = item['module']
        module_data = PhAvgMonthData.objects.filter(module=module_name).all()
        # 该模块的数据已经存在，按照日期更新缺少的数据
        if len(module_data) > 0:
            module_data = module_data.get()
            update_date = module_data.update_date

            delta = (today - update_date).days

            old_cpu_list = json.loads(module_data.cpu)
            old_mem_list = json.loads(module_data.mem)
            old_eth0_in_list = json.loads(module_data.eth0_in)
            old_eth0_out_list = json.loads(module_data.eth0_out)
            old_machine_count_list = json.loads(module_data.machine_count)

            new_cpu_list, new_mem_list, new_eth0_in_list, new_eth0_out_list, new_machine_count_list = get_avg_data_of_delta(
                delta, module_name)

            del old_cpu_list[0:delta]
            del old_mem_list[0:delta]
            del old_eth0_in_list[0:delta]
            del old_eth0_out_list[0:delta]
            del old_machine_count_list[0:delta]
            old_cpu_list.extend(new_cpu_list)
            old_mem_list.extend(new_mem_list)
            old_eth0_in_list.extend(new_eth0_in_list)
            old_eth0_out_list.extend(new_eth0_out_list)
            old_machine_count_list.extend(new_machine_count_list)

            module_data.cpu = old_cpu_list
            module_data.mem = old_mem_list
            module_data.eth0_in = old_eth0_in_list
            module_data.eth0_out = old_eth0_out_list
            module_data.machine_count = old_machine_count_list

            module_data.update_date = today
            module_data.save()
        # 该模块的数据不存在，需要计算最近30天的数据，插入新的数据
        else:
            new_cpu_list, new_mem_list, new_eth0_in_list, new_eth0_out_list, new_machine_count_list = get_avg_data_of_delta(
                30, module_name)
            module_data = PhAvgMonthData.createPhAvgMonthData(new_cpu_list, new_mem_list, new_eth0_in_list,
                                                              new_eth0_out_list, new_machine_count_list, module_name,
                                                              today)
            module_data.save()

    print(str(datetime.datetime.now()) + "平均值数据统计完成！")


def get_avg_data_of_delta(delta, module_name):
    """
    根据参数delta(天数)计算某个模块的数据
    :param delta:
    :param module_name:
    :return:
    """

    client = InfluxDBClient(host='vot.oa.com', port=8081, database='tnm2')
    cpuMonthlyAvgList = []
    memMonthlyAvgList = []
    eth0InMonthlyAvgList = []
    eth0OutMonthlyAvgList = []
    machineCountList = []
    # 循环取过去delta天的数据
    for i in range(1, delta + 1):
        start = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 20:00:00'
        end = str(datetime.date.today() + datetime.timedelta(days=-i)) + ' 22:00:00'
        query_sql = 'SELECT max(cpu),max(mem),max(mem_total), max(eth0_in),max(eth0_out) FROM "machine" WHERE (module =\'' + module_name + '\'  ) AND time >= \'' + start + '\' AND time <= \'' + end + '\'   GROUP BY lan_ip tz(\'Asia/Shanghai\')'
        query_data = client.query(query_sql)
        series = query_data.raw['series']

        allCpuData = 0
        allMemData = 0
        allEth0InData = 0
        allEth0OutData = 0
        machineCount = len(series)
        # if machineCount > 0:
        for serie in series:

            cpuUse = serie[1] if serie[1] else 0
            if (serie[2] == None) or (serie[3] == None):
                memUse = 0
            else:
                memUse = (serie[2] * 1024 * 100) / serie[3]
            eth0InUse = serie[4] * 8 / 60 / 1000 if serie[4] else 0
            eth0OutUse = serie[5] * 8 / 60 / 1000 if serie[5] else 0
            allCpuData = allCpuData + cpuUse
            allMemData = allMemData + memUse
            allEth0InData = allEth0InData + eth0InUse
            allEth0OutData = allEth0OutData + eth0OutUse
        cpuMonthlyAvgList.append(round(allCpuData / machineCount, 2) if machineCount > 0 else 0)
        memMonthlyAvgList.append(round(allMemData / machineCount, 2) if machineCount > 0 else 0)
        eth0InMonthlyAvgList.append(round(allEth0InData / machineCount, 2) if machineCount > 0 else 0)
        eth0OutMonthlyAvgList.append(round(allEth0OutData / machineCount, 2) if machineCount > 0 else 0)
        machineCountList.append(machineCount)

    return cpuMonthlyAvgList[::-1], memMonthlyAvgList[::-1], eth0InMonthlyAvgList[::-1], eth0OutMonthlyAvgList[
                                                                                         ::-1], machineCountList[::-1]


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
            serie = [random.randint(1,100), random.randint(1,100),random.randint(1,100),random.randint(1,100),]
            cpuUse = serie[1]
            memUse = serie[2]
            eth0InUse = serie[3]
            eth0OutUse = serie[4]
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


