from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
import base64


UserModel = get_user_model()
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form = UserRegisterForm(request.POST)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            image_file = user.profile.image.open("rb")
            encoded_base64 = base64.b64encode(image_file.read())
            encoded_str = encoded_base64.decode('utf-8')
            user.profile.blob_image = encoded_str
            user.profile.save()
            current_site = get_current_site(request)
            mail_subject = "Verify your email and start using our platform!"
            uid1 = urlsafe_base64_encode(force_bytes(user.pk))
            token1= default_token_generator.make_token(user)
            message = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid1,
                    "token": token1
                },
            )
            message_html = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid1,
                    "token": token1
                },
            )
            to_email = form.cleaned_data.get("email")
            send_mail(mail_subject, message, "noreply@dissertationexchange.com", [to_email], html_message=message_html)
            return render(request, "users/complete_register.html")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.last_login = None
        user.save()
        return render(request, "users/success_link.html")
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            image_file = p_form.instance.image.open("rb")
            encoded_base64 = base64.b64encode(image_file.read())
            encoded_str = encoded_base64.decode('utf-8')
            p_form.instance.blob_image = encoded_str
            u_form.save()
            p_form.save()
            messages.success(request, "Account settings updated!")
            return redirect("user-posts", username=request.user)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        print("D" + str(self.request.user.last_login))
        user = self.request.user.profile
        if user.first == 0:
            print("D" + str(self.request.user.last_login))
            messages.success(self.request, "Welcome to Dissertation Exchange! Head over to your profile to customise it!")
            user.first = 1
            user.save()
        return resolve_url('blog-home')