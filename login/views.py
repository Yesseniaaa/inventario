from django.contrib.auth.views import LoginView


# Create your views here.
class Login(LoginView):
    template_name = "login/login_page.html"
    next = "index"