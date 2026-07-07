from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

def update_order_status_by_time(order):
    from django.utils import timezone
    elapsed = timezone.now() - order.created_at
    elapsed_minutes = elapsed.total_seconds() / 60.0
    est = order.estimated_time or 20
    
    if elapsed_minutes >= est:
        if order.payment_method == "ONLINE" or order.payment_status == "PAID":
            new_status = "DELIVERED"
        else:
            new_status = "READY"
    elif elapsed_minutes >= est * 0.75:
        new_status = "READY"
    elif elapsed_minutes >= est * 0.25:
        new_status = "PREPARING"
    else:
        new_status = "RECEIVED"
        
    status_order = ["RECEIVED", "PREPARING", "READY", "DELIVERED"]
    if status_order.index(new_status) > status_order.index(order.status):
        order.status = new_status
        order.save()

from .models import (
    Category,
    MenuItem,
    Offer,
    Review,
    Order,
    OrderItem,
)

from .forms import CheckoutForm


def home(request):

    categories = Category.objects.prefetch_related("items").all()

    featured_items = (
    MenuItem.objects
    .filter(is_available=True)
    .order_by("-rating")[:8]
)

    menu_items = (
    MenuItem.objects
    .filter(is_available=True)
    .select_related("category")
    .order_by("category__name", "name")
)

    offers = Offer.objects.filter(
        is_active=True
    )[:3]
    reviews = Review.objects.filter(
    is_visible=True
    )[:6]

    return render(
    request,
    "home.html",
    {

        "categories": categories,

        "featured_items": featured_items,

        "menu_items": menu_items,

        "offers": offers,
        
        "reviews": reviews,
    }
)


@login_required(login_url="/accounts/login/")
def checkout(request):

    profile = getattr(request.user, "profile", None)
    initial_data = {}
    if profile:
        initial_data["customer_name"] = profile.full_name
        initial_data["customer_phone"] = profile.mobile_number

    form = CheckoutForm(initial=initial_data)

    return render(
        request,
        "checkout.html",
        {
            "form": form
        }
    )

def place_order(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False
        })

    data = json.loads(request.body)

    customer = data["customer"]

    cart = data["cart"]

    # Safe parsing for table number (optional) to prevent ValueError crashes
    table_number = customer.get("table")
    if not table_number or str(table_number).strip() == "":
        table_number = None
    else:
        try:
            table_number = int(table_number)
        except ValueError:
            table_number = None

    payment_method = customer.get("payment_method", "COD")
    payment_status = "PAID" if payment_method == "ONLINE" else "PENDING"

    order = Order.objects.create(

        user=request.user,

        customer_name=customer.get("name") or request.user.profile.full_name,

        customer_phone=customer.get("phone") or request.user.profile.mobile_number,

        table_number=table_number,

        total_amount=customer["total"],

        payment_method=payment_method,

        payment_status=payment_status

    )

    total = 0

    for item in cart:

        menu = MenuItem.objects.get(id=item["id"])

        OrderItem.objects.create(

            order=order,

            menu_item=menu,

            quantity=item["quantity"],

            price_at_order=item["price"]

        )

        total += item["price"] * item["quantity"]

    order.total_amount = total

    order.save()

    return JsonResponse({

        "success": True,

        "order_id": order.id

    })


def order_success(request, order_id):

    order = Order.objects.get(id=order_id)

    return render(

        request,

        "success.html",

        {

            "order": order

        }

    )

def track_order(request, order_id):

    order = Order.objects.prefetch_related(
        "items"
    ).get(id=order_id)

    update_order_status_by_time(order)

    return render(

        request,

        "tracking.html",

        {

            "order": order

        }

    )

@login_required(login_url="/accounts/login/")
def order_history(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items")
        .order_by("-created_at")
    )

    return render(
        request,
        "order_history.html",
        {
            "orders": orders
        }
    )


def kitchen_dashboard(request):

    if request.method == "POST":

        order = Order.objects.get(

            id=request.POST["order_id"]

        )

        if "action" in request.POST and request.POST["action"] == "mark_paid":
            order.payment_status = "PAID"
            order.save()
        else:
            order.status = request.POST["status"]
            order.save()

        return redirect("kitchen_dashboard")

    orders = Order.objects.prefetch_related(

        "items"

    ).order_by("-created_at")

    return render(

        request,

        "kitchen_dashboard.html",

        {

            "orders": orders

        }

    )

def order_status_api(request, order_id):
    order = Order.objects.get(id=order_id)
    update_order_status_by_time(order)
    return JsonResponse({
        "status": order.status,
        "status_display": order.get_status_display(),
        "estimated_time": order.estimated_time
    })