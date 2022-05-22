from .views import CategoryView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# app_name = 'blog_api'
app_name = 'tata'

router = DefaultRouter()
router.register('category', CategoryView, basename='category')
urlpatterns = router.urls
urlpatterns += [
    path('category/<int:pk>/level/<int:level>/', CategoryView.as_view({"get": "retrieve_category_with_level"})),
    path('get-parents/<int:pk>/', CategoryView.as_view({"get": "retrieve_parents"})),
    path('delete-category-without-child/<int:pk>/', CategoryView.as_view({"delete": "delete_parent_without_child"}))
]