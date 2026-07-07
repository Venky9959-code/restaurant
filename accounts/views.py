from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],

                email=form.cleaned_data["email"],

                password=form.cleaned_data["password1"]

            )

            profile = user.profile

            profile.full_name = form.cleaned_data["full_name"]

            profile.mobile_number = form.cleaned_data["mobile_number"]

            if form.cleaned_data["profile_photo"]:
                profile.profile_photo = form.cleaned_data["profile_photo"]

            profile.save()

            login(request, user)

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

    return render(
        request,
        "auth/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            login(request, form.get_user())

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

    return render(
        request,
        "auth/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def profile_view(request):

    return render(
        request,
        "auth/profile.html"
    )