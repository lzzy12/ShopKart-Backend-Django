from django.urls import path

from .views import ProductsListView, ProductItemView, LoginView, SignUpView

urlpatterns = [
    path('products/', ProductsListView.as_view()),
    path('products/<str:pk>', ProductItemView.as_view()),
    path('login/', LoginView.as_view()),
    path('signup/', SignUpView.as_view()),
]
