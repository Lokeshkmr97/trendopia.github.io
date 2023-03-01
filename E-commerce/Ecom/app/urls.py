from django.urls import path
from app import views
from django.conf import settings                # IMAGE UPLOAD KARNE K LIYE YE 2 LINE LIKHNA HOTA HAI
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
 
urlpatterns = [
    # path('', views.home),

    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(),name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),

    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),

    # path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobiledata/<slug:data>', views.mobile, name='mobiledata'),
    path('bottomwear/', views.bottom_wear, name='bottomwear'),
    path('bottomweardata/<slug:data>', views.bottom_wear, name='bottomweardata'),
    path('topwear/', views.top_wear, name='topwear'),
    path('topweardata/<slug:data>', views.top_wear, name='topweardata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptopdata/<slug:data>', views.laptop, name='laptopdata'),

    # ==========    User Authentication Url Start ====================
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
     
     # ==========    User Authentication Url End ====================

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/',views.payment_done,name='paymentdone'),



    #================ Footer url =================================
    path('contact/',views.contact,name='contact'),
    path('privacypolicy/',views.privacypolicy,name='privacypolicy'),
    path('returnrefund/',views.return_refund_policy,name='returnrefund'),
    path('shipping_policy/',views.shipping_policy,name='shippingpolicy'),
    path('termcondition/',views.term_condition,name='termcondition')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # IMAGE UPLOAD KARNE K LIYE YE SETTING KARNA HOTA HAI

