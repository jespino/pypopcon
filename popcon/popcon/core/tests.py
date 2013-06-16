from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import App, Installation, AppVersion, Environment

import json


class ViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env1 = Environment.objects.create(uuid="00000000000000000000000000000000")
        cls.env2 = Environment.objects.create(uuid="00000000000000000000000000000001")
        cls.app1 = App.objects.create(name="test-app-1")
        cls.app2 = App.objects.create(name="test-app-2")
        cls.app1version1 = AppVersion.objects.create(version="1", app=cls.app1)
        cls.app1version2 = AppVersion.objects.create(version="2", app=cls.app1)
        cls.app2version1 = AppVersion.objects.create(version="1", app=cls.app2)
        cls.app2version2 = AppVersion.objects.create(version="2", app=cls.app2)
        cls.installation1 = Installation.objects.create(app_version=cls.app1version1, environment=cls.env1)
        cls.installation2 = Installation.objects.create(app_version=cls.app2version2, environment=cls.env1)
        cls.installation3 = Installation.objects.create(app_version=cls.app1version2, environment=cls.env2)

    @classmethod
    def tearDownClass(cls):
        cls.app1version1.delete()
        cls.app1version2.delete()

        cls.app2version1.delete()
        cls.app2version2.delete()

        cls.app1.delete()
        cls.app2.delete()

        cls.env1.delete()
        cls.env2.delete()

        cls.installation1.delete()
        cls.installation2.delete()
        cls.installation3.delete()

    def test_ranking(self):
        response = self.client.get(reverse('ranking'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'test-app-1')
        self.assertEqual(data[0]['downloads'], 2)
        self.assertEqual(data[1]['name'], 'test-app-2')
        self.assertEqual(data[1]['downloads'], 1)

    def test_list(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], 'test-app-1')
        self.assertEqual(data[1], 'test-app-2')

    def test_app_info(self):
        response = self.client.get(reverse('info', args=['test-app-1']))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['name'], 'test-app-1')
        self.assertEqual(len(data['versions']), 2)
        self.assertEqual(data['versions'][0]['version'], '1')
        self.assertEqual(data['versions'][0]['installations'], 1)
        self.assertEqual(data['installations'], 2)

    def test_publish_existing_environment(self):
        data = {
            'apps': [
                {
                    'name': 'test-app-1',
                    'version': '1',
                },
                {
                    'name': 'test-app-2',
                    'version': '2',
                }
            ]
        }
        response = self.client.put(reverse('publish', args=["00000000000000000000000000000000"]), data=json.dumps(data))
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'result': 'ok'})
        self.assertEqual(Installation.objects.all().count(), 3)
        self.assertEqual(App.objects.all().count(), 2)
        self.assertEqual(AppVersion.objects.all().count(), 4)
        self.assertEqual(Environment.objects.all().count(), 2)

    def test_publish_new_environment(self):
        data = {
            'apps': [
                {
                    'name': 'test-app-1',
                    'version': '1',
                },
                {
                    'name': 'test-app-2',
                    'version': '2',
                },
                {
                    'name': 'test-app-3',
                    'version': '1',
                }
            ]
        }
        response = self.client.put(reverse('publish', args=["00000000000000000000000000000003"]), data=json.dumps(data))
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'result': 'ok'})
        self.assertEqual(Installation.objects.all().count(), 6)
        self.assertEqual(App.objects.all().count(), 3)
        self.assertEqual(AppVersion.objects.all().count(), 5)
        self.assertEqual(Environment.objects.all().count(), 3)

        Environment.objects.filter(uuid="00000000000000000000000000000003").delete()
        App.objects.filter(name='test-app-3').delete()

    def test_publish_with_invalid_data(self):
        response = self.client.put(reverse('publish', args=["00000000000000000000000000000003"]), data=json.dumps('invalid-data'))
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'result': 'ko'})
