from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from . models import Turn, User


def index(request):
    latest_turns_list = Turn.objects.order_by('-create_date')
    return render(request, 'index.html', {'latest_turns_list': latest_turns_list})


def detail(request, turn_id):
    try:
        a = Turn.objects.get(id=turn_id)
    except:
        raise Http404("Черга не знайдена!")

    latest_users_list = a.user_set.order_by('id')

    return render(request, 'detail.html', {'turn': a, 'latest_users_list': latest_users_list})


# counter=1


def turn_register(request, turn_id):
    try:
        turn_count = User.objects.count()
        a = Turn.objects.get(id=turn_id)
    except:
        raise Http404("Черга не знайдена!")
    a.user_set.create(user_name=request.POST['name'], position=turn_count + 1, registration_date=timezone.now())
    # a.user_set.create(user_name=request.POST['name'], user_number=counter, registration_date=timezone.now())
    # counter += 1
    return HttpResponseRedirect(reverse('turns:detail', args=(a.id,)))
    # user_number = request.POST['user_number'], registration_date = timezone.now()
