# backend/core/admin.py - С ПОДДЕРЖКОЙ SHORT_DESCRIPTION
import csv
import io
import json
from datetime import datetime

from django.contrib import admin, messages
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.html import format_html
from django.utils.safestring import mark_safe

