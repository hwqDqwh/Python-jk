from django.db import models

# Create your models here.

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment_content = models.CharField(max_length=200)
    agree = models.IntegerField()
    opposition = models.IntegerField()
    sentiment = models.FloatField()
    created_at = models.DateTimeField()

    # 元数据，不属于任何一个字段的数据
    class Meta:
        managed = False
        db_table = 'phone_comments'
