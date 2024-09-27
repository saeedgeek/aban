from django.db import models
from django.utils import timezone


class Tracks(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField with primary_key=True creates an auto-incrementing primary key

    user_type = models.CharField(max_length=255)  # Example primary key field
    user_id = models.CharField(max_length=255)
    request_type = models.CharField(max_length=255)
    request = models.CharField(max_length=255)
    response = models.CharField(max_length=50)
    duration = models.IntegerField()  # Duration in seconds
    time_stamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Tracks'  # The actual table name in the QuestDB database
        managed = False

    @staticmethod
    def get_database():
        return 'questdb'

    def save(self, *args, **kwargs):
        kwargs['using'] = self.get_database()
        super(Tracks, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['using'] = self.get_database()
        super(Tracks, self).delete(*args, **kwargs)

    @classmethod
    def get_queryset(cls):
        return super(Tracks, cls).get_queryset().using(cls.get_database())
