# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VDbApi(models.Model):
    site_name = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    wind_speed_10m_mps = models.FloatField(blank=True, null=True)
    wind_direction_in_deg = models.FloatField(blank=True, null=True)
    temp_c = models.FloatField(blank=True, null=True)
    nowcast_ghi_wpm2 = models.FloatField(blank=True, null=True)
    swdown2 = models.FloatField(blank=True, null=True)
    cs_data = models.FloatField(blank=True, null=True)
    ci_data = models.FloatField(blank=True, null=True)
    tz = models.TextField(blank=True, null=True)
    ct_data = models.FloatField(blank=True, null=True)
    ct_flag_data = models.TextField(blank=True, null=True)
    forecast_method = models.TextField(blank=True, null=True)
    log_ts = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'v_db_api'
