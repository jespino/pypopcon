from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import json

from .models import App, AppVersion, Environment, Installation

class Publish(View):
    @method_decorator(csrf_exempt)
    def put(self, request, uuid):
        env, _ = Environment.objects.get_or_create(uuid=uuid)
        data = json.loads(request.body)
        for data_app in data['apps']:
            app, _ = App.objects.get_or_create(name=data_app['name'])
            version, _ = AppVersion.objects.get_or_create(app=app, version=data_app['version'])
            Installation.objects.get_or_create(environment=env, app_version=version)
        return HttpResponse(json.dumps({'result': 'ok'}))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Publish, self).dispatch(request, *args, **kwargs)

class AppInfo(View):
    def get(self, request, name):
        app = get_object_or_404(App, name=name)
        total = 0
        response = {
            'name': name,
            'versions': []
        }
        for version in app.versions.all():
            count = version.installations.count()
            total += count
            response['versions'].append({
                'version': version.version,
                'installations': count
            })
        response['installations'] = total
        return HttpResponse(json.dumps(response))

class AppsList(View):
    def get(self, request):
        response = []
        for app in App.objects.all().order_by('name'):
            response.append(app.name)
        return HttpResponse(json.dumps(response))

class Ranking(View):
    def get(self, request):
        response = []
        for app in App.objects.all():
            response.append({
                'name': app.name,
                'downloads': Installation.objects.filter(app_version__app=app).count()
            })
        response = sorted(response, lambda x, y: -cmp(x['downloads'], y['downloads']))
        return HttpResponse(json.dumps(response))
