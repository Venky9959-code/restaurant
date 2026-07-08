from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    # Bootstrap Icon Class
    icon = models.CharField(
        max_length=50,
        default="bi bi-grid-fill"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="foods/",
        blank=True,
        null=True,
    )

    is_vegetarian = models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)

    preparation_time = models.PositiveIntegerField(
        default=15,
        help_text="Preparation Time (Minutes)"
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.8
    )

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        """Return image URL, falling back to static file served by WhiteNoise."""
        if self.image and self.image.name:
            try:
                return self.image.url
            except Exception:
                pass
        # Fall back to the git-tracked static image (always available on Render)
        static_name = self.name.replace(" ", "_") + ".jpg"
        return f"/static/images/foods/{static_name}"


class Offer(models.Model):

    title = models.CharField(max_length=100)

    subtitle = models.CharField(max_length=200)

    discount = models.CharField(
        max_length=30,
        help_text="Example: 50% OFF"
    )

    image = models.ImageField(
        upload_to="offers/",
        blank=True,
        null=True,
    )

    button_text = models.CharField(
        max_length=30,
        default="Order Now"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """Return image URL or a static placeholder if no image is set."""
        if self.image and self.image.name:
            try:
                return self.image.url
            except Exception:
                pass
        return "/static/images/no-food.png"

class Order(models.Model):

    STATUS_CHOICES = [
        ("RECEIVED", "Order Received"),
        ("PREPARING", "Preparing"),
        ("READY", "Ready For Pickup"),
        ("DELIVERED", "Delivered"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("COD", "Cash On Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders"
    )

    customer_name = models.CharField(max_length=100)

    customer_phone = models.CharField(max_length=15)

    table_number = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    estimated_time = models.PositiveIntegerField(
        default=20
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="RECEIVED"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="COD"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    invoice_number = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    invoice = models.FileField(
        upload_to="invoices/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price_at_order = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def subtotal(self):

        return self.quantity * self.price_at_order

    def __str__(self):

        return f"{self.quantity} x {self.menu_item.name}"

class Review(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    customer_name = models.CharField(
        max_length=100
    )

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    comment = models.TextField()

    is_visible = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"