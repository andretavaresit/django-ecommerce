
from django.urls import path

app_name = "search"

from .views import (
                        SearchServiceView, 
                    )
urlpatterns = [
    path('', SearchServiceView.as_view(), name='query'),
]