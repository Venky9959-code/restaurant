from django.urls import path
from . import views
from . import payment

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Place Order (COD only / after verification)
    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),

    # Razorpay
    path(
        "create-payment/",
        payment.create_payment,
        name="create_payment"
    ),

    path(
        "verify-payment/",
        payment.verify_payment,
        name="verify_payment"
    ),

    # Success
    path(
        "success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),

    # Tracking
    path(
        "track/<int:order_id>/",
        views.track_order,
        name="track_order"
    ),

    # Customer Orders
    path(
        "orders/",
        views.order_history,
        name="order_history"
    ),

    path(
        "orders/<int:order_id>/status/",
        views.order_status_api,
        name="order_status_api"
    ),

    # Kitchen
    path(
        "kitchen/",
        views.kitchen_dashboard,
        name="kitchen_dashboard"
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )