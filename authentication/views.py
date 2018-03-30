from django.views.generic.base import View, RedirectView
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from .forms import UserCreationForm, UserLoginForm


class Register(View):

    @staticmethod
    def post(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            result = {
                'status': 1
            }
            newUser = form.save()
            login(request, newUser)
        else:
            result = {
                'status': 0,
                'errors': form.errors,
            }
        return JsonResponse(result)


class Login(View):

    @staticmethod
    def post(request):
        form = UserLoginForm(request.POST)
        result = {
            'status': 0,
        }
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    result = {
                        'status': 1,
                    }
                    login(request, user)
                else:
                    form.errors['email'] = ['您的账户已被禁用']
            else:
                form.errors['email'] = ['']
                form.errors['password'] = ['Email 或 密码 错误']
        result['errors'] = form.errors
        return JsonResponse(result)


class Logout(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.META.get('HTTP_REFERER', '/')
        logout(self.request)
        return super(Logout, self).get_redirect_url(*args, **kwargs)
