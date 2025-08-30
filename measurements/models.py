from django.db import models


class Measurement(models.Model):
    user_id = models.CharField(max_length=128)
    sbp = models.IntegerField()              # 收缩压
    dbp = models.IntegerField()              # 舒张压
    hr = models.IntegerField(null=True)      # 心率（可空）
    timestamp = models.DateTimeField()       # ISO8601 时间
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'timestamp']),
        ]

    def __str__(self):
        return f'{self.user_id} {self.sbp}/{self.dbp} @ {self.timestamp}'
