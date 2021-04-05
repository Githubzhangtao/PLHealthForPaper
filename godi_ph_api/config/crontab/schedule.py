from static.models import TbGlobalScanTaskLog
from utils.RedisUtil import Redis
import os
import django
import datetime as dt
from dynamic.crontab import schedule as dynamicSchedule
from static.crontab import schedule as staticSchedule

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
django.setup()


# Create your views here.


def get_all_module():
    """
    # 每日从数据库中获取所有的三级模块保存在redis中
    :return:
    """
    yesterday = (dt.date.today() + dt.timedelta(days=-1))
    yesterday = '2020-08-27'
    qs = TbGlobalScanTaskLog.objects.filter(day_time=yesterday, sss_status='success').exclude(
        show_os_detail_json='')
    qs = qs.values_list('om_biz_from_config')
    moduleList = []
    for item in qs:
        modules = str(item[0]).split(";")
        for module in modules:
            moduleList.append(module)


    conn = Redis("default")
    conn.delete('all_modules_yesterday')
    for module in moduleList:
        conn.sadd('all_modules_yesterday', module)

    # a = conn.smembers('all_modules_yesterday')
    # for item in a:
    #     print(item)
    print(str(dt.datetime.now()) + "获取所有三级模块完成!")


def generate_define_module():
    """
    # 生成已有的module
    :return:
    """

    redis = Redis("default")
    redis.delete('define_modules')

    for i in range(1, 2):
        name = '[腾讯云][国内CDN]-[视频云CDN][OC]-[腾讯云][直播平台L' + str(i) + ']'
        redis.sadd('define_modules', name)

    # a = redis.smembers('define_modules')
    # for item in a:
    #     print(item)
    schedule_all_in_one

    print(dt.datetime.now() + "生成已有模块完成！")


def schedule_all_in_one():
    get_all_module()
    staticSchedule.get_static_data()
    dynamicSchedule.get_dynamic_data()


if __name__ == "__main__":
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'godi_ph_api.settings')
    get_all_module()
    # generate_define_module()
    # get_static_data()
