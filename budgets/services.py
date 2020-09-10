from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic.base import View

from .models import Budget


class DailyCosts(View):
    pass
