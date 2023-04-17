from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from turns.models import Turn
from turns.forms import TurnForm


def index(request):
    latest_turns_list = Turn.objects.order_by('-create_date')
    return render(request, 'turns/index.html', {'latest_turns_list': latest_turns_list})


def create_turn(request):
    if request.method == 'POST':
        form = TurnForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.creator = request.user.id
            form.save()
            turn_id = form.instance.id
            return redirect(f'../{turn_id}/')

    form = TurnForm()
    data = {'form': form}
    return render(request, 'turns/create.html', data)


def open_turn(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    if request.user.id == turn.creator or request.user.username == 'admin':
        if not turn.status:
            turn.status = True
            turn.save()
        else:
            raise Http404('Черга вже відкрита')
    else:
        raise Http404('Ви не хазяїн черги!')
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def close_turn(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    if request.user.id == turn.creator or request.user.username == 'admin':
        if turn.status:
            turn.status = False
            turn.save()
        else:
            raise Http404('Черга вже закрита')
    else:
        raise Http404('Ви не хазяїн черги!')
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def delete_turn(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    if request.user.id == turn.creator or request.user.username == 'admin':
        turn.delete()
        return redirect('index')
    else:
        raise Http404('Ви не хазяїн черги!')


def turn_register(request, turn_id):
    user = request.user
    try:
        turn = Turn.objects.get(id=turn_id)
    except:
        raise Http404('Черга не знайдена!')
    turn.user_set.create(username=user.username, first_name=user.first_name, last_name=user.last_name,
                         registration_date=timezone.now(), id=user.id)
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def turn_unregister(request, turn_id):
    user = request.user
    try:
        turn = Turn.objects.get(id=turn_id)
    except:
        raise Http404('Ви не в черзі!')

    user_in_turn = turn.user_set.filter(id=user.id)
    if user_in_turn.exists():
        user_in_turn.first().delete()
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def detail(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except:
        raise Http404('Черга не знайдена!')

    latest_users_list = turn.user_set.order_by('registration_date')
    users_id_list = [i.id for i in latest_users_list]
    return render(request, 'turns/detail.html', {'turn': turn, 'latest_users_list': latest_users_list,
                                                 'users_id_list': users_id_list})


def next_turn_user(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    if request.user.id == turn.creator or request.user.username == 'admin':
        latest_users_list = turn.user_set.order_by('registration_date')
        latest_users_list[0].delete()
        return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
    else:
        raise Http404('Ви не хазяїн черги!')


def delete_turn_user(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    if request.user.id == turn.creator or request.user.username == 'admin':
        if request.method == 'POST':
            user_id = request.POST['user']
            turn.user_set.filter(id=user_id).delete()
            return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
    else:
        raise Http404('Ви не хазяїн черги!')
