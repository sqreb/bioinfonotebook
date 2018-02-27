from django.shortcuts import render, Http404
from django.views.decorators.cache import cache_page
from .models import *
import networkx as nx
from django.utils.safestring import mark_safe
import re

def text2word(text):
    text = text.upper()
    return list(filter(lambda x: x, re.split(re.compile("\s"), text)))

class DocInfo(object):
    doc_graph = nx.DiGraph()
    roots = list()
    search_dict = dict()
    mata_nav = list()

    @classmethod
    def reset(cls):
        cls.doc_graph = nx.DiGraph()
        rel_li = list()
        for doc_rel in DocRel.objects.all():
            parent_doc = doc_rel.parent
            child_doc = doc_rel.child
            if parent_doc.public and child_doc.public:
                rel_li.append([parent_doc, child_doc])
        cls.doc_graph.add_edges_from(rel_li)
        if cls.doc_graph.nodes:
            assert max([degree for node, degree in cls.doc_graph.in_degree()]) <= 1
        cls.roots = cls.find_roots()
        cls.search_dict = cls.build_search_dict()
        cls.mata_nav = cls.find_mata_nav()

    @classmethod
    def find_roots(cls):
        return [node for node in cls.doc_graph.nodes if node.root]

    @classmethod
    def find_root_path(cls, url_name):
        path = list()
        doc = Doc.objects.get(url=url_name)
        path.append(doc)
        while not doc.root:
            doc = list(cls.doc_graph.predecessors(doc))[0]
            path.append(doc)
        return path

    @classmethod
    def find_root(cls, url_name):
        return cls.find_root_path(url_name)[-1]

    @classmethod
    def find_subgraph(cls, url_name):
        root = cls.find_root(url_name)
        subgraph = cls.doc_graph.subgraph(list(nx.descendants(cls.doc_graph, root))+[root])
        return subgraph

    @classmethod
    def node2html(cls, G, node, page):
        children_nodes = sorted([c for p, c in G.edges(node)], key=lambda x: x.priority)
        if not children_nodes:
            return """<li class="no_dot"><a class="nav_div_title black nav-link" href="{node.url}">{node.title}</a></li>""".format(node=node)

        children_html = "".join([cls.node2html(G, child, page) for child in children_nodes])
        return """
        <div id="accordion{node.url}">
            <div class="card bg_grey">
                <div class="card-header nav_div_header" id="heading{node.url}">
                    <h5>
                        <button class="btn btn-link nav_div_title black" data-toggle="collapse" data-target="#collapse{node.url}" aria-expanded="true" aria-controls="collapse{node.url}">
                        {node.title}
                        </button>&nbsp;&nbsp;<a class="nav_div_link black" href="/{page}/{node.url}">View</a>
                    </h5>
                </div>

                <div id="collapse{node.url}" class="collapse" aria-labelledby="heading{node.url}" data-parent="#accordion{node.url}">
                    <div class="card-body nav_div_body">
                        <ul class="nav_ul">
                        {children_html}
                        </ul>
                    </div>
                </div>
            </div>
        </div>""".format(node=node, page=page, children_html=children_html)

    @classmethod
    def build_search_dict(cls):
        search_dict = dict()
        for node in cls.doc_graph.nodes:
            for tag in node.search_tags.all():
                tag_str = str(tag.tag)
                tag_str = tag_str.upper()
                if tag_str == "NA":
                    continue
                for word in text2word(tag_str):
                    if word not in search_dict.keys():
                        search_dict[word] = set()
                    search_dict[word].add(node)

            title_str = str(node.title)
            title_str = title_str.upper()
            for word in text2word(title_str):
                if word not in search_dict.keys():
                    search_dict[word] = set()
                search_dict[word].add(node)
        return search_dict

    @classmethod
    def find_mata_nav(cls):
        mata_dict = dict()
        for root in cls.roots:
            mata = root.mata_tag.tag
            if mata not in mata_dict.keys():
                mata_dict[mata] = list()
            mata_dict[mata].append(root)
        for li in mata_dict.values():
            li.sort(key=lambda x: x.title)
        matas = sorted(mata_dict.items())
        return matas

@cache_page(60 * 15)
def docs(request, url_name):
    if not DocInfo.doc_graph.nodes:
        DocInfo.reset()
    try:
        doc = Doc.objects.get(url=url_name)
    except Doc.DoesNotExist:
        raise Http404("Not exist")
    except Doc.MultipleObjectsReturned:
        raise Http404("Multi hits")
    if not doc.public:
        raise Http404("No public")
    doc_path = DocInfo.find_root_path(url_name)[::-1]
    subgraph = DocInfo.find_subgraph(url_name)
    nav = DocInfo.node2html(subgraph, doc_path[0], "docs")

    search_docs = list()
    search_tag = False
    if "search-input" in request.POST.keys():
        search_text = request.POST["search-input"]
        doc_dict = dict()
        for word in text2word(search_text):
            search_tag = True
            if word not in DocInfo.search_dict.keys():
                continue
            for doc in DocInfo.search_dict[word]:
                if doc not in doc_dict.keys():
                    doc_dict[doc] = 0
                doc_dict[doc] += 1
        search_docs = [doc for doc, cnt in sorted(doc_dict.items(), key=lambda x: (x[1], x[0].title), reverse=True)]

    return render(request, 'docs/docs.html',
                  {"doc": doc, "doc_path": doc_path,
                   "nav": mark_safe(nav),
                   "search_tag": search_tag,
                   "search_docs": search_docs,
                   "mata_nav": DocInfo.mata_nav})

