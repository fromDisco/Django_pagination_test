from django.urls import path
from . import views 

app_name = "pages"
urlpatterns = [
    path("", views.AllKeyWords.as_view(), name="all_keywords"),
    path("<int:page_num>/", views.json_paginated, name="json"),
    path("page/<int:page_num>", views.PaginatorTryouts.as_view(), name="page_view"),
]
