from rest_framework import viewsets
from utils.Response import JsonResponse
import json
from utils.RedisUtil import Redis
from rest_framework.decorators import action
import json
from static.models import TbGlobalScanTaskLog
from config.models import PhDefinedModule
import re
from utils.RedisUtil import Redis
import os
import django
import datetime as dt
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
django.setup()


def get_avg(x, y):
    """
    # 计算x和y的乘积求和并除以y得到平均值
    :param x:
    :param y:
    :return:
    """
    func = lambda x, y: x * y
    if len(y) == 0:
        result = 0
    else:
        result = sum(list(map(func, x, y))) / sum(y)
    return round(result, 1)

# Create your views here.
def get_static_data():
    """
    定时查出所有的modules的静态数据并保存在redis中
    :return:
    """

    redis = Redis("default")
    # module_list = redis.smembers('define_modules')
    # 使用mysql存储define_module
    module_list = PhDefinedModule.objects.filter().all().values('module')

    yesterday = (dt.date.today() + dt.timedelta(days=-1))
    # yesterday = '2020-07-31'

    allCpuData = {}
    allMemData = {}
    allDiskData = {}
    resultCpu = []
    resultMem = []
    resultDisk = []
    result = {}
    for item in module_list:
        module = item['module']
        qs = TbGlobalScanTaskLog.objects.filter(day_time=yesterday, sss_status='success',
                                                om_biz_from_config__contains=module).exclude(show_os_detail_json='')
        qs = qs.values_list('show_os_detail_json__os_cpu_phy_num', 'show_os_detail_json__os_cpu_phy_every_core',
                            'show_os_detail_json__os_mem_GB', 'show_os_detail_json__os_disk_all')
        cpuCore = {}
        memory = {}
        disk = {}
        for i in range(0,100):
            # 计算cpuCore
            item = [random.choice([1,2,4]),random.choice([1,2,4]),random.choice([4,8,16,32,64,128]),random.choice(["32GB","64GB","128GB","256GB","512GB","1024GB"])]
            cpuKey = int(item[0]) * int(item[1])
            cpuCore[cpuKey] = cpuCore.get(cpuKey, 0) + 1
            allCpuData[cpuKey] = allCpuData.get(cpuKey, 0) + 1
            # 计算mem
            memKey = float(item[2])
            memory[memKey] = memory.get(memKey, 0) + 1
            allMemData[memKey] = allMemData.get(memKey, 0) + 1
            # 计算disk
            diskData = item[3]
            diskNum = 0
            if diskData.endswith("GB"):
                diskNum = float(diskData[0:-2])
            elif diskData.endswith("TB"):
                diskNum = diskData[0:-2]
                diskNum = float(diskNum) * 1000
            elif diskData.endswith("PB"):
                diskNum = diskData[0:-2]
                diskNum = float(diskNum) * 1000 * 1000
            disk[diskNum] = disk.get(diskNum, 0) + 1
            allDiskData[diskNum] = allDiskData.get(diskNum, 0) + 1

        cpuCore = dict([(k, cpuCore[k]) for k in sorted(cpuCore.keys())])
        memory = dict([(k, memory[k]) for k in sorted(memory.keys())])
        disk = dict([(k, disk[k]) for k in sorted(disk.keys())])
        resultCpu = {'x': list(cpuCore.keys()), 'y': list(cpuCore.values()),
                     'avg': get_avg(cpuCore.keys(), cpuCore.values())}
        resultMem = {'x': list(memory.keys()), 'y': list(memory.values()),
                     'avg': get_avg(memory.keys(), memory.values())}
        resultDisk = {'x': list(disk.keys()), 'y': list(disk.values()), 'avg': get_avg(disk.keys(), disk.values())}
        result[module] = {'cpu': resultCpu, 'mem': resultMem, 'disk': resultDisk}

    allCpuData = dict([(k, allCpuData[k]) for k in sorted(allCpuData.keys())])
    allCpuData = {'x': list(allCpuData.keys()), 'y': list(allCpuData.values()),
                  'avg': get_avg(allCpuData.keys(), allCpuData.values())}
    allMemData = dict([(k, allMemData[k]) for k in sorted(allMemData.keys())])
    allMemData = {'x': list(allMemData.keys()), 'y': list(allMemData.values()),
                  'avg': get_avg(allMemData.keys(), allMemData.values())}

    allDiskData = dict([(k, allDiskData[k]) for k in sorted(allDiskData.keys())])
    allDiskData = {'x': list(allDiskData.keys()), 'y': list(allDiskData.values()),
                   'avg': get_avg(allDiskData.keys(), allDiskData.values())}
    # result.append({'all': {'cpu': allCpuData, 'mem': allMemData, 'disk': allDiskData}})
    result['汇总数据'] = {'cpu': allCpuData, 'mem': allMemData, 'disk': allDiskData}
    # print(result)
    redis.delete('SDODefined')
    redis.set('SDODefined', json.dumps(result))
    print(str(dt.datetime.now()) + "统计现有模块静态数据完成！")

class StaticViewSet(viewsets.GenericViewSet):
    """
        从redis中获取静态资源统计数据
    """

    @action(methods=['get'], detail=False, url_path='getStaticData')
    def getStaticData(self, request, *args, **kwargs):
        get_static_data()
        redis = Redis("default")
        SDODefined = redis.get('SDODefined')
        static_data = json.loads(SDODefined)
        if len(static_data) == 1:
            return JsonResponse(1, '没有数据')

        return JsonResponse(20000, '查询成功！', static_data)
