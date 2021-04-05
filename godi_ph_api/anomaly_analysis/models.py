from django.db import models


# Create your models here.
class PhAnomalyAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    high_load_cpu = models.TextField(blank=True, null=True)
    high_load_mem = models.TextField(blank=True, null=True)
    high_load_eth0_in = models.TextField(blank=True, null=True)
    high_load_eth0_out = models.TextField(blank=True, null=True)
    low_load_cpu = models.TextField(blank=True, null=True)
    low_load_mem = models.TextField(blank=True, null=True)
    low_load_eth0_in = models.TextField(blank=True, null=True)
    low_load_eth0_out = models.TextField(blank=True, null=True)
    offline_device = models.TextField(blank=True, null=True)
    abnormal_removal = models.TextField(blank=True, null=True)
    abnormal_repeat_removal = models.TextField(blank=True, null=True)
    alarm_ping = models.TextField(blank=True, null=True)
    alarm_flow = models.TextField(blank=True, null=True)
    alarm_performance = models.TextField(blank=True, null=True)
    alarm_port = models.TextField(blank=True, null=True)
    alarm_process_port = models.TextField(blank=True, null=True)
    alarm_process = models.TextField(blank=True, null=True)
    alarm_report_time_out = models.TextField(blank=True, null=True)
    alarm_disk = models.TextField(blank=True, null=True)
    alarm_disk_ro = models.TextField(blank=True, null=True)
    alarm_disk_ro_full = models.TextField(blank=True, null=True)

    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ph_anomaly_analysis'

    @classmethod
    def createPhAnomalyAnalysis(cls, module, high_load_cpu, high_load_mem, high_load_eth0_in, high_load_eth0_out,
                                low_load_cpu, low_load_mem, low_load_eth0_in, low_load_eth0_out, offline_device,
                                new_alarm_ping, new_alarm_flow, new_alarm_performance, new_alarm_port,
                                new_alarm_process_port, new_alarm_process, new_alarm_report_time_out, new_alarm_disk,
                                new_alarm_disk_ro, new_alarm_disk_ro_full, update_date):
        phAnomalyAnalysis = cls(high_load_cpu=high_load_cpu, high_load_mem=high_load_mem,
                                high_load_eth0_in=high_load_eth0_in, high_load_eth0_out=high_load_eth0_out
                                , low_load_cpu=low_load_cpu, low_load_mem=low_load_mem,
                                low_load_eth0_in=low_load_eth0_in, low_load_eth0_out=low_load_eth0_out,
                                module=module, update_date=update_date, offline_device=offline_device,alarm_ping=new_alarm_ping, alarm_flow=new_alarm_flow
                                , alarm_performance=new_alarm_performance, alarm_port=new_alarm_port,
                                alarm_process_port=new_alarm_process_port, alarm_process=new_alarm_process, alarm_report_time_out=new_alarm_report_time_out, alarm_disk=new_alarm_disk,
                                alarm_disk_ro=new_alarm_disk_ro, alarm_disk_ro_full=new_alarm_disk_ro_full)
        return phAnomalyAnalysis
