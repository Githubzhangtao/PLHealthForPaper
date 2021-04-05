from django.db import models
# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godi_ph_api.settings")  # project_name 项目名称
# django.setup()

# Create your models here.
class PhAvgMonthData(models.Model):
    id = models.IntegerField(primary_key=True)
    cpu = models.CharField(max_length=1000, blank=True, null=True)
    mem = models.CharField(max_length=1000, blank=True, null=True)
    eth0_in = models.CharField(max_length=1000, blank=True, null=True)
    eth0_out = models.CharField(max_length=1000, blank=True, null=True)
    machine_count = models.CharField(max_length=1000, blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ph_avg_month_data'

    @classmethod
    def createPhAvgMonthData(cls, cpu, mem, eth0_in, eth0_out, machine_count, module, update_date):
        phAvgMonthData = cls(cpu=cpu, mem=mem, eth0_in=eth0_in, eth0_out=eth0_out, machine_count=machine_count,
                             module=module, update_date=update_date)
        return phAvgMonthData
