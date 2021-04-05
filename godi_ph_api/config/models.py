from django.db import models
from rest_framework import serializers


# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
# django.setup()
# 解决django环境问题，在测试时引入model时需要
# Create your models here.



class PhConfigUseRange(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.IntegerField(blank=True, null=True)
    stop = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    is_high_load = models.IntegerField(blank=True, null=True)
    is_low_load = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ph_config_use_range'

    @classmethod
    def create_config_use_range(cls, start, stop, type, is_high_load, is_low_load, update_time, sort):
        # 构造方法
        useRange = cls(start=start, stop=stop, type=type, is_high_load=is_high_load, is_low_load=is_low_load,
                       update_time=update_time, sort=sort)
        return useRange




class PhDefinedModule(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=255)
    sort = models.IntegerField(blank=True, null=True)
    is_done = models.IntegerField()
    update_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ph_defined_module'
        # app_label = 'config'

    @classmethod
    def create_defined_module(cls, module, sort, is_done, update_date):
        # 构造方法
        defined_module = cls(module=module, sort=sort, is_done=is_done, update_date=update_date)
        return defined_module


# PhDefinedModule序列化类
class PhDefinedModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhDefinedModule
        fields = ['id', 'module', 'sort', 'is_done', 'update_date']