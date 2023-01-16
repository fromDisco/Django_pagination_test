# django imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse

# project imports
from . import models


class AllKeyWords(ListView):
    model = models.Keyword 
    template_name = "pages/all-keywords.html"
    context_object_name = "keywords"
    paginate_by = 5


def json_paginated(request, page_num=1):
    if request.method == "GET":
        per_page = request.GET.get("per_page", 5)

        object_list = models.Keyword.objects.all()
        paginator = Paginator(object_list, per_page)

        page_obj = paginator.get_page(page_num)

        data = [{"name": kw.name } for kw in page_obj.object_list]

        payload = {
            "page": {
                "current": page_obj.number,
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next(),
            },
            "data": data
        }

    return JsonResponse(payload)


class PaginatorTryouts(TemplateView):
    template_name = "pages/keywords-page.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # read get parameters
        startswith = self.kwargs.get("startswith", "")
        per_page = self.kwargs.get("per_page", 5)
        page_num = self.kwargs.get("page_num", 1)

        # create filtered query
        keywords = models.Keyword.objects.filter(name__startswith=startswith)
        paginator = Paginator(keywords, per_page=per_page)
        page_obj = paginator.get_page(page_num)

        context["keywords"] = [ keyword.name for keyword in page_obj.object_list]

        payload = {
            "page": {
                "current": page_obj.number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            },
            "data": context["keywords"],
        }

        return payload
    
