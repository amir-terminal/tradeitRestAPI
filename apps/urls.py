from django.urls import path
from .views import CategoryListView, CurrentUserAPIView, EmailCheck, LoginAPIView, ProductAPIDetailView, RegisterAPIView, ProductAPIPostView,ProductsAPIListView,CategoryProductsView,UserProductListView
app_name= 'app'
urlpatterns = [
    path('register', RegisterAPIView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path("fetchuser",EmailCheck.as_view(),name='email_check'),
    path("profile",CurrentUserAPIView.as_view(),name='profile'),
    # path('auth-token/',)
    path("categories", CategoryListView.as_view(), name="categories_list"),
    path("categories/<str:general>", CategoryProductsView.as_view(), name="categorie_products"),
    path("categories/<slug:general>/<slug:subcategory>",CategoryProductsView.as_view(),name='subcategory_products'),
    path('products',ProductsAPIListView.as_view(),name='products_list'),
    path('product',ProductAPIDetailView.as_view(),name='product_detail'),
    path('user/products',UserProductListView.as_view(),name='user_products'),
    path('addproduct',ProductAPIPostView.as_view(),name='product_register'),
]
