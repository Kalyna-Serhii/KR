from myfirst.apps.turns.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View


def main(request):
    return render(request, 'main.html')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {"form": UserCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            User = authenticate(username=username, password=password)
            login(request, User)
            return redirect('main')
        context = {'form': form}
        return render(request, self.template_name, context)
