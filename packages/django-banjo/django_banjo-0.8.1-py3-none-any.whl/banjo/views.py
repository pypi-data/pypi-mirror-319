from django.shortcuts import render, reverse
from django.conf import settings
from django.http import JsonResponse

def describe_route(urlpattern):
    """Introspects data from a url pattern"""
    p = urlpattern
    f = p.callback
    return {
        "name": p.name,
        "human_name": p.name.replace("_", " ").capitalize(),
        "description": f.__doc__ or "",
        "arguments": {param: type_.__name__ for param, type_ in f.args.items()},
        "url": reverse(p.name),
        "api_url": reverse("api_" + p.name),
        "method": f.method,
    }

def get_routes():
    """Returns a list of dicts, each describing a route in the app.
    """
    from banjo.urls import user_defined_routes
    return [describe_route(r) for r in user_defined_routes]

def api(request):
    """A view which renders the API index page.
    """
    return render(request, "banjo/api.html", {"routes": get_routes()})
    
def api_json(request):
    "Returns a JSON representation of available API routes"
    routes = {'routes': get_routes()}
    return JsonResponse(routes)
