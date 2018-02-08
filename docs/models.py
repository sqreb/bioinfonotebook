# -*- coding: utf-8 -*-

from django.db import models


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

    class Meta:
        abstract = True


class SearchTag(Tag):
    pass


level = (("Pri", "Primary"),
         ("Sec", "Secondary"),
         ("S", "Success"),
         ("Dag", "Danger"),
         ("E", "Warning"),
         ("If", "Info"),
         ("Lt", "Light"),
         ("Dk", "Dark"),
         ("Lk", "Link"))


class InfoTag(Tag):
    level = models.CharField(max_length=3, choices=level)


class MataTag(Tag):
    pass


class Doc(models.Model):
    doc_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    doc = models.TextField()
    mata_tag = models.ForeignKey(MataTag, on_delete=models.SET_NULL, null=True)
    search_tags = models.ManyToManyField(SearchTag)
    info_tags = models.ManyToManyField(InfoTag)
    priority = models.IntegerField(default=0)
    url = models.CharField(max_length=255, null=True, unique=True)
    public = models.BooleanField(default=False)
    root = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class DocRel(models.Model):
    parent = models.ForeignKey(Doc, on_delete=models.CASCADE,
                               related_name="parent", related_query_name="parent")
    child = models.ForeignKey(Doc, on_delete=models.CASCADE,
                              related_name="child", related_query_name="child")