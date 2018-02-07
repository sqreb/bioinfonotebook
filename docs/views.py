from django.shortcuts import render
from .models import *


def docs(request, *args):
    url_name = "STAR"
    doc = Doc.objects.get(url=url_name)
    docmd_text = doc.doc
    # docmd = markdown2.markdown(force_bytes(docmd_text), extras=["code-friendly"])
    # print(docmd_text)
    # print(docmd)
    return render(request, 'docs/docs.html', {"docmd": docmd_text})
