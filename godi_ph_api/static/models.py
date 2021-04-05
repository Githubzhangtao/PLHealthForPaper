from django.db import models
from django_mysql.models import JSONField

# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
# django.setup()


class TbGlobalScanTaskLog(models.Model):
    day_time = models.CharField(max_length=30, blank=True, null=True)
    task_id = models.IntegerField(blank=True, null=True)
    sss_status = models.CharField(max_length=10, blank=True, null=True)
    sss_info = models.CharField(max_length=1000, blank=True, null=True)
    om_fixed_assets_sn = models.CharField(max_length=50, blank=True, null=True)
    om_internal_ip = models.CharField(db_column='om_Internal_ip', max_length=50, blank=True, null=True)  # Field name made lowercase.
    om_external_ip = models.CharField(db_column='om_External_ip', max_length=500, blank=True, null=True)  # Field name made lowercase.
    om_ipv6 = models.CharField(max_length=500, blank=True, null=True)
    om_idc = models.CharField(db_column='om_IDC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    om_biz_from_config = models.CharField(db_column='om_Biz_from_config', max_length=1000, blank=True, null=True) # Field name made lowercase.
    om_admin = models.CharField(max_length=50, blank=True, null=True)
    om_bak_admin = models.CharField(max_length=500, blank=True, null=True)
    om_device_type = models.CharField(db_column='om_Device_type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    om_device_model = models.CharField(db_column='om_Device_model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    om_opoperationname = models.CharField(db_column='om_OpOperationName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    om_serverusetime = models.CharField(db_column='om_serverUsetime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    om_groupname = models.CharField(db_column='om_groupName', max_length=50, blank=True, null=True)  # Field namemade lowercase.
    show_os_version = models.CharField(max_length=100, blank=True, null=True)
    show_os_kernal_simple = models.CharField(max_length=100, blank=True, null=True)
    show_os_kernal_detail = models.CharField(max_length=100, blank=True, null=True)
    show_os_ipv6 = models.CharField(max_length=100, blank=True, null=True)
    # show_os_detail_json = models.TextField(blank=True, null=True)
    show_os_detail_json = JSONField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        # app_label = 'check_system'
        db_table = 'tb_global_scan_task_log'
