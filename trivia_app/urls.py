from django.urls import path
from .views import Index

urlpatterns = [
    # path to trivia app's functionality
    path('', Index.as_view(), name='index'),
]
