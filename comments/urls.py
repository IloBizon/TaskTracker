from django.urls import path
from . import views

urlpatterns= [
    path("", views.CommentView.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', views.CommentView.as_view({
        'get': 'retrieve',
        'delete': 'destroy'})),
    path("<int:pk>/update", views.UpdateComment.as_view())
]