from django.contrib import admin
from .models import *


class MenuItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "rating",
        "preparation_time",
        "is_available",
        "is_vegetarian",
    )

    list_filter = (
        "category",
        "is_available",
        "is_vegetarian",
    )

    search_fields = (
        "name",
        "description",
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "customer_phone",
    )

    inlines = [OrderItemInline]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "discount",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "subtitle",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "rating",
        "is_visible",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_visible",
    )

    search_fields = (
        "customer_name",
        "comment",
    )

admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
