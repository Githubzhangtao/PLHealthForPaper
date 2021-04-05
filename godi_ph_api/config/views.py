from rest_framework.views import APIView
from utils.Response import JsonResponse
import json
from utils.RedisUtil import Redis
from static.crontab import schedule as staticSchedule
from dynamic.crontab import schedule as dynamicSchedule
from config.models import PhDefinedModule, PhDefinedModuleSerializer
from anomaly_analysis.crontab import schedule as anomalySchedule
from config.models import PhConfigUseRange
from rest_framework import viewsets
from rest_framework.decorators import action

import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='APScheduler.txt',
                    filemode='a')
scheduler = BackgroundScheduler()
scheduler.start()


# Create your views here.
def update_dynamic_data():
    """
    更新利用率范围配置时，需要更新动态资源数据
    :return:
    """
    redis = Redis("default")
    dynamicSchedule.get_dynamic_data()
    redis.set('count_over', "1")


def update_all_data():
    """
    已定义模块变更时，需要更新静态、动态、平均值数据以及异常分析数据
    """
    redis = Redis("default")
    anomalySchedule.count_anomaly_analysis()
    dynamicSchedule.get_monthly_avg_data()
    dynamicSchedule.get_dynamic_data()
    staticSchedule.get_static_data()
    doneList = PhDefinedModule.objects.filter(is_done=0).all()
    for doneItem in doneList:
        doneItem.is_done = 1
        doneItem.save()
    redis.set('count_over', "1")


class ConfigViewSet(viewsets.ViewSet):
    """
     config 配置模块的viewset
    """

    @action(methods=['get'], detail=False, url_path='modules/getAllModuleList')
    def get_all_module_list(self, request, *args, **kwargs):
        """
        获取所有的module列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        all_modules_yesterday = []

        for i in range(0,21):
            all_modules_yesterday.append("模块"+str(i))

        return JsonResponse(20000, '查询成功', all_modules_yesterday)


    @action(methods=['put'], detail=False, url_path='modules/putModules')
    def put_modules(self, request, *args, **kwargs):
        param = request.query_params
        redis = Redis('default')
        # for item in param:
        #     name = param[item]
        #     redis.sadd('define_modules', name)

        for item in param:
            name = param[item]
            saveItem = PhDefinedModule.create_defined_module(name, 0, 0, datetime.date.today())
            saveItem.save()
        return JsonResponse(20000, '添加成功！', "ok")

    @action(methods=['delete'], detail=False, url_path='modules/deleteModules')
    def delete_modules(self, request, *args, **kwargs):
        param = request.query_params
        for item in param:
            deleteId = json.loads(param[item])
            print(type(deleteId))
            deleteItem = PhDefinedModule.objects.get(pk=deleteId['id'])
            deleteItem.delete()
        return JsonResponse(20000, '删除成功！', "ok")

    # 获取已定义得统计完成模块的列表
    @action(methods=['get'], detail=False, url_path='modules/getDoneDefineModuleList')
    def getDoneDefineModuleList(self, request, *args, **kwargs):
        # redis = Redis("default")
        define_modules = PhDefinedModule.objects.filter(is_done=1).all()
        serData = PhDefinedModuleSerializer(instance=define_modules, many=True)
        if len(define_modules) == 0:
            return JsonResponse(1, '没有添加模块！')

        return JsonResponse(20000, '查询成功', serData.data)

    # 获取已定义得所有模块的列表
    @action(methods=['get'], detail=False, url_path='modules/getDefineModuleList')
    def getDefineModuleList(self, request, *args, **kwargs):
        # redis = Redis("default")
        define_modules = PhDefinedModule.objects.all()
        serData = PhDefinedModuleSerializer(instance=define_modules, many=True)
        return JsonResponse(20000, '查询成功', serData.data)

    @action(methods=['get'], detail=False, url_path='useRange/getUseRangeData')
    def getUseRangeData(self, request, *args, **kwargs):
        # 查询时根据sort排序
        param = request.query_params
        rangeType = param['type']
        cpuRangeList = PhConfigUseRange.objects.filter(type=rangeType).order_by('sort').all().values('id', 'start',
                                                                                                     'stop', 'type',
                                                                                                     'is_high_load',
                                                                                                     'is_low_load',
                                                                                                     'update_time')
        return JsonResponse(20000, '查询成功！', cpuRangeList)

    @action(methods=['put'], detail=False, url_path='useRange/saveUseRangeData')
    def saveUseRangeData(self, request, *args, **kwargs):

        param = request.query_params
        saveData = json.loads(param['saveData'])
        dataType = saveData['type']
        data = saveData['data']

        idList = []

        for index, item in enumerate(data, 1):
            if 'id' in item:
                idList.append(item['id'])
                # 存在id表示数据存在，需要更新数据库
                updateItem = PhConfigUseRange.objects.get(pk=item['id'])
                updateItem.start = item['start']
                updateItem.stop = item['stop']
                updateItem.type = item['type']
                updateItem.is_high_load = item['is_high_load']
                updateItem.is_low_load = item['is_low_load']
                updateItem.update_time = datetime.datetime.now()
                updateItem.sort = index
                updateItem.save()

            else:
                # 不存在需要创建数据
                newItem = PhConfigUseRange.create_config_use_range(item['start'], item['stop'], item['type'],
                                                                   item['is_high_load'], item['is_low_load'],
                                                                   datetime.datetime.now(), index)
                newItem.save()
                idList.append(newItem.id)

        typeOfData = PhConfigUseRange.objects.filter(type=dataType).all().values_list('id')
        for item in typeOfData:

            if item[0] not in idList:
                deleteItem = PhConfigUseRange.objects.get(pk=item[0])
                deleteItem.delete()

        update_dynamic_data()
        return JsonResponse(20000, '保存成功！', 'success')

    @action(methods=['get'], detail=False, url_path='countStatus')
    def countStatus(self, request, *args, **kwargs):
        # redis = Redis("default")
        # count_over = redis.get("count_over")
        return JsonResponse(20000, '查询成功！', 1)


class InitModuleData(APIView):
    """
    # 初始化模块数据
    """

    def get(self, request, *args, **kwargs):
        staticSchedule.get_all_module()
        # schedule.generate_define_module()
        staticSchedule.get_static_data()
        return JsonResponse(20000, '初始化成功', None)

