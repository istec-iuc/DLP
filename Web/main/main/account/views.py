from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EditUserUpdateForm, UserUpdateForm, ChangeUserPasswordForm

# Create your views here.


def login_views(request):
    if request.user.is_authenticated:
        return redirect("dlp:dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dlp:dashboard")
        else:
            return render(request, "account/login.html", {
                "error": "Check your username or password!"
            })

    return render(request, "account/login.html")


@login_required
def logout_views(request):
    logout(request)
    return redirect("account:login")


@login_required
def profile_views(request):
    return render(request, "account/profile.html")


@login_required
def users_views(request):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")
    context = {
        'users': User.objects.all()
    }
    return render(request, "account/users.html", context)


@login_required
def add_user_views(request):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        super_user = request.POST.get("super_user", None)

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/post/add_user.html",
                              {
                                  "error": "Username is already used!",
                                  "username": username,
                                  "email": email,
                                  "firstname": firstname,
                                  "lastname": lastname
                              })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/post/add_user.html",
                                  {
                                      "error": "Email is already used!",
                                      "username": username,
                                      "email": email,
                                      "firstname": firstname,
                                      "lastname": lastname
                                  })
                else:
                    if super_user == "on":
                        user = User.objects.create_user(
                            username=username, email=email, first_name=firstname, last_name=lastname, password=password, is_staff=True,
                            is_active=True,
                            is_superuser=True)
                    else:
                        user = User.objects.create_user(
                            username=username, email=email, first_name=firstname, last_name=lastname, password=password)
                    user.save()
                    messages.success(request, 'User created successfully!')
                    return redirect("account:users")
        else:
            return render(request, "account/post/add_user.html", {
                "error": "Passwords does not match!",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname
            })
    return render(request, "account/post/add_user.html")


@login_required
def update_user_profile_views(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('account:profile')
        else:
            return render(request, 'account/post/update_profile.html', {'form': user_form})

    return render(request, 'account/post/update_profile.html', {'form': user_form})


@login_required
def change_password_views(request):
    form = ChangeUserPasswordForm(data=request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = authenticate(
                request, username=request.user.username, password=form.new_password2)
            login(request, user)
            messages.success(
                request, 'Your password has been successfully updated.')
            return redirect("account:profile")

    context = {
        'form': form
    }
    return render(request, 'account/post/change_password.html', context)

# only superuser


@login_required
def user_delete_views(request, username):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(username=username)
        try:
            user.delete()
            messages.success(request, "User has been successfully deleted.")
        except:
            messages.error(request, "User could not be deleted!")

    return redirect('account:users')

# errr


@login_required
def edit_user_views(request, username):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    if request.user.username == username:
        return redirect("account:update_user_profile")

    user = User.objects.get(username=username)
    user_form = EditUserUpdateForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile has been updated!')
            return redirect('account:users')
        else:
            return render(request, 'account/post/edit_user.html', {'form': user_form})
    return render(request, 'account/post/edit_user.html', {'user': user, 'form': user_form})
