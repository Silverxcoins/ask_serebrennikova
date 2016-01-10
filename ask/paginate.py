from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
import json

def paginate(objects_list, request, objects_on_page, page):
    paginator = Paginator(objects_list, objects_on_page)
    try:
        list_on_page = paginator.page(page or 1)
        return list_on_page
    except EmptyPage:
        raise Http404
        
