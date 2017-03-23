from django.db import models

from selstagram_server import utils


# Create your models here.


class StringHelperModelMixin(object):
    def __str__(self):
        return str(self.id)

    def field_list_to_string(self, field_list=[]):
        return_string = str(self.id) + ': '
        for string in field_list:
            return_string += str(string) + ', '

        return return_string[:-2]


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class InstagramMedia(StringHelperModelMixin, TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=128)
    source_id = models.BigIntegerField(db_index=True)
    source_url = models.URLField(max_length=256)
    source_date = models.DateTimeField(default=utils.BranchUtil.now)

    # slug
    code = models.CharField(max_length=64)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    thumbnail_url = models.URLField(max_length=256)

    owner_id = models.BigIntegerField()

    caption = models.TextField()
    comment_count = models.PositiveIntegerField()
    like_count = models.PositiveIntegerField()

    def __str__(self):
        return self.field_list_to_string([self.code, self.caption])
