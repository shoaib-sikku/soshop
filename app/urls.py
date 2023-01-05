from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,ResetForm


urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('buynow/', views.buynow, name='buynow'),
    path('cart/', views.show_cart, name='cart'),
    path("pluscart", views.plus_cart),
    path("minuscart", views.minus_cart),
    path("removecart", views.remove_cart),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"),name='passwordchangedone'),
    # paswword reset 4 steps ..................
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="app/password_reset.html",form_class=ResetForm),name="password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html",),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html",),name="password_reset_complete"),
    path('mobile/', views.mobile, name='mobile'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('laptop/', views.laptop, name='laptop'),
    path('mobile/<slug:data>', views.mobile, name='mobileslug'),
    path('laptop/<slug:data>', views.laptop, name='laptopslug'),
    path('topwear/<slug:data>', views.topwear, name='topwearslug'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomwearslug'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.RegistraionView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.paymentdone , name='paymentdone')
]
