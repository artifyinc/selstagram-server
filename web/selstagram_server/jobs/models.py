from django.db import models

from selstagram_server.utils import BranchUtil

# Create your models here.
from selstagram_server.model_mixins import StringHelperModelMixin, TimeStampedModel


class BaseJob(StringHelperModelMixin, TimeStampedModel):
    class JobStatus:
        IN_PROGRESS = 'InProgress'
        SUCCESS = 'Success'
        FAIL = 'Fail'

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=32,
                              choices=((JobStatus.IN_PROGRESS, JobStatus.IN_PROGRESS),
                                       (JobStatus.SUCCESS, JobStatus.SUCCESS),
                                       (JobStatus.FAIL, JobStatus.FAIL)))
    params = models.CharField(max_length=512)

    class Meta:
        abstract = True


class CrawlJob(BaseJob):
    tag = models.CharField(max_length=256)
    limit_count = models.IntegerField(default=-1)

