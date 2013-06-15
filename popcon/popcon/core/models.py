from django.db import models

class Environment(models.Model):
    uuid = models.CharField(max_length=36, null=False, blank=False)

class App(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

class AppVersion(models.Model):
    version = models.CharField(max_length=20, null=False, blank=False)
    app = models.ForeignKey(App, null=False, blank=False, related_name="versions")

class Installation(models.Model):
    environment = models.ForeignKey(Environment, null=False, blank=False, related_name="installations")
    app_version = models.ForeignKey(AppVersion, null=False, blank=False, related_name="installations")
