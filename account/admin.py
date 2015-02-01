from django.contrib import admin
from django.db.models import get_models, get_app

for model in get_models(get_app('account')):
    admin.site.register(model)

for model in get_models(get_app('base')):
    admin.site.register(model)

for model in get_models(get_app('page')):
    admin.site.register(model)