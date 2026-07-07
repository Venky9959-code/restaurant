from django import forms


class CheckoutForm(forms.Form):

    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Your Name"
        })
    )

    customer_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Mobile Number"
        })
    )

    table_number = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Table Number (Optional)"
        })
    )

    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            "class": "form-check-input"
        }),
        initial="COD"
    )