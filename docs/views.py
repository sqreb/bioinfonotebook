from django.shortcuts import render, Http404
from .models import *
import networkx as nx
from django.utils.safestring import mark_safe

class DocGraph(object):
    doc_graph = nx.DiGraph()
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
        assert max([degree for node, degree in cls.doc_graph.in_degree()]) <= 1

    @classmethod
    def roots(cls):
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
            return """<a class="nav_div_title" href="{node.url}">{node.title}</a>""".format(node=node)
        if node.root:
            return "<div>{0}</div>".format("".join([cls.node2html(G, child, page) for child in children_nodes]))
        else:
            children_html = "".join(
                """<li>{0}</li>""".format(html) for html in [cls.node2html(G, child, page) for child in children_nodes])
            return """
<div id="accordion{node.url}">
    <div class="card">
        <div class="card-header nav_div_header" id="heading{node.url}">
            <h5>
                <button class="btn btn-link nav_div_title" data-toggle="collapse" data-target="#collapse{node.url}" aria-expanded="true" aria-controls="collapse{node.url}">
                {node.title}
                </button>&nbsp;&nbsp;<a class="nav_div_link" href="/{page}/{node.url}">Detail</a>
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

DocGraph.reset()


def docs(request, url_name):
    try:
        doc = Doc.objects.get(url=url_name)
    except Doc.DoesNotExist:
        raise Http404("Not exist")
    except Doc.MultipleObjectsReturned:
        raise Http404("Multi hit")
    if not doc.public:
        raise Http404("No public")
    doc_path = DocGraph.find_root_path(url_name)[::-1]
    subgraph = DocGraph.find_subgraph(url_name)
    nav = DocGraph.node2html(subgraph, doc_path[0], "docs")
    return render(request, 'docs/docs.html',
                  {"doc": doc, "doc_path": doc_path,
                   "nav": mark_safe(nav)})
