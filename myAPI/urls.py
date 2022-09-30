from django.urls import path
from myAPI import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('countries/', views.country_list),
    path('countries/<int:id>', views.country_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
