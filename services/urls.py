from django.urls import path

app_name = "services"

from .views import (
                        ServiceListView, 
                        ServiceDetailSlugView,
                    )

urlpatterns = [
    path('', ServiceListView.as_view()),
    path('<slug:slug>/', ServiceDetailSlugView.as_view(), name='detail')
]