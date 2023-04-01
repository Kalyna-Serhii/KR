from django.utils import timezone
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from . models import Turn


def index(request):
    latest_turns_list = Turn.objects.order_by('-create_date')
    return render(request, 'turns/index.html', {'latest_turns_list': latest_turns_list})


def detail(request, turn_id):
    try:
        a = Turn.objects.get(id=turn_id)
    except:
        raise Http404("Черга не знайдена!")

    latest_users_list = a.user_set.order_by('registration_date')

    return render(request, 'turns/detail.html', {'turn': a, 'latest_users_list': latest_users_list})


def turn_register(request, turn_id):
    user = request.user
    try:
        a = Turn.objects.get(id=turn_id)
    except:
        raise Http404("Черга не знайдена!")

    a.user_set.create(first_name=user.first_name, last_name=user.last_name, registration_date=timezone.now())
    return HttpResponseRedirect(reverse('detail', args=(a.id,)))

