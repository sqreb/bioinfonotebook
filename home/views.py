# -*- coding: utf-8 -*-
from django.shortcuts import render, Http404
from django.views.decorators.cache import cache_page
from docs.views import DocInfo


@cache_page(60 * 15)
def about_us(request, url_name):
    if not DocInfo.doc_graph.nodes:
        DocInfo.reset()
    try:
        assert url_name in ["about_us", "help_us", "duty"]
        return render(request, 'about/{0}.html'.format(url_name), {"mata_nav": DocInfo.mata_nav})
    except:
        Http404()


@cache_page(60 * 15)
def main(request):
    if not DocInfo.doc_graph.nodes:
        DocInfo.reset()
    try:
        return render(request, 'main.html', {"mata_nav": DocInfo.mata_nav})
    except:
        Http404()

