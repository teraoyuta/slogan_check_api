from django.db import models
from  api.base_model import BaseManager

# Create your models here.


class SlogansManager(BaseManager):
    pass

class Slogans(models.Model):
    slogan_sentence = models.CharField(max_length=200)
    slogan_kana = models.CharField(max_length=200)
    vector = models.BinaryField()
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    deleted_at = models.DateTimeField('削除日時', blank=True, null=True)
    objects = SlogansManager()
    all_objects = SlogansManager(alive_only=False)

    class Meta:
        db_table = 'slogans'
