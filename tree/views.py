from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
import json
import controller
import inspect


def who_am_i():
    return inspect.stack()[1][3]


def render_tree(request):
    context = RequestContext(request, {'max_depth': controller.get_max_level()})
    return render(request, 'tree/tree.html', context_instance=context)


def ajax_get_tree(request):
    res = HttpResponse(json.dumps({}), content_type='application/json')
    if request.is_ajax():
        depth = request.GET.get('depth', None)
        node_name = request.GET.get('q', None)
        data = {'msg': who_am_i()}
        nodes = controller.select_level(depth, node_name)
        nodes = format_tree(nodes)
        data['nodes'] = nodes
        res = HttpResponse(json.dumps(data), content_type='application/json')
    return res


def ajax_update_name(request):
    res = HttpResponse(json.dumps({}), content_type='application/json')
    if request.is_ajax():
        id = request.GET.get('id', None)
        new_name = request.GET.get('name', None)
        updated = controller.update_name_by_id(id, new_name)
        if updated is not None:
            data = {'res': True, 'name': updated}
        else:
            data = {'res': False}
        res = HttpResponse(json.dumps(data), content_type='application/json')
    return res


def format_tree(records):
    res = list()
    for r in records:
        parent = r[2][-1]
        node = {
            'id': str(r[0]),
            'parent': parent,
            'text': r[1],
            'level': len(r[2]),
        }
        res.append(node)
    return res


def ajax_remove_subtree(request):
    res = HttpResponse(json.dumps({}), content_type='application/json')
    if request.is_ajax():
        element_id = request.GET.get('id', None)
        deleted_number = controller.remove_subtree(element_id)
        data = {'msg': 'Deleted {} element[s]'.format(deleted_number),
                'res': deleted_number}
        res = HttpResponse(json.dumps(data), content_type='application/json')
    return res
