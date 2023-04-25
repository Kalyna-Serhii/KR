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


def detail(request, turn_id):
    try:
        users_check(request, turn_id)
        turn = Turn.objects.get(id=turn_id)
        latest_users_list = turn.user_set.order_by('registration_date')
        users_id_list = [i.id for i in latest_users_list]
        if users_id_list:
            first_in_the_turn = users_id_list[0]
        else:
            first_in_the_turn = -1
        if not latest_users_list:
            turn.time_at_the_top = None
            turn.save()
        return render(request, 'turns/detail.html', {'turn': turn, 'latest_users_list': latest_users_list,
                                                     'users_id_list': users_id_list,
                                                     'first_in_the_turn': first_in_the_turn})
    except:
        raise Http404('Черга не знайдена!')


def open_turn(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    user = request.user
    if user.id == turn.creator or user.username == 'admin':
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
    user = request.user
    if user.id == turn.creator or user.username == 'admin':
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
    user = request.user
    if user.id == turn.creator or user.username == 'admin':
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
    latest_users_list = turn.user_set.order_by('registration_date')
    if user.id == latest_users_list[0].id:
        position_check(request, turn_id)
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def turn_unregister(request, turn_id):
    user = request.user
    try:
        turn = Turn.objects.get(id=turn_id)
        latest_users_list = turn.user_set.order_by('registration_date')
    except:
        raise Http404('Черга не знайдена!')

    try:
        if user.id == latest_users_list[0].id:
            flag = True
        else:
            flag = False
        latest_users_list[0].delete()
        if flag is True:
            if latest_users_list:
                position_check(request, turn_id)
    except:
        raise Http404('Ви не в черзі!')

    users_check(request, turn_id)
    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def next_turn_user(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    user = request.user
    if user.id == turn.creator or user.username == 'admin':
        latest_users_list = turn.user_set.order_by('registration_date')
        time_check(request, turn_id)
        latest_users_list[0].delete()
        if latest_users_list:
            position_check(request, turn_id)
        users_check(request, turn_id)
        return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
    else:
        raise Http404('Ви не хазяїн черги!')


def delete_turn_user(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    user = request.user
    if user.id == turn.creator or user.username == 'admin':
        if request.method == 'POST':
            latest_users_list = turn.user_set.order_by('registration_date')
            user_id = request.POST['user']
            try:
                if user.id == latest_users_list[0].id:
                    flag = True
                else:
                    flag = False
                for i in range(len(latest_users_list)):
                    if user_id == str(latest_users_list[i].id):
                        latest_users_list[i].delete()
                        break
                if flag is True:
                    if latest_users_list:
                        position_check(request, turn_id)
                users_check(request, turn_id)
                return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
            except:
                raise Http404('Такого очікувача не існує!')
    else:
        raise Http404('Ви не хазяїн черги!')


def position_check(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    turn.time_at_the_top = timezone.now()
    turn.save()


def time_check(request, turn_id):
    turn = Turn.objects.get(id=turn_id)

    service_time = timezone.now() - turn.time_at_the_top
    service_time_seconds = service_time.seconds + service_time.days * 86400

    turn.all_service_time += service_time_seconds
    turn.all_waiting += 1
    turn.save()

    users_check(request, turn_id)


def users_check(request, turn_id):
    turn = Turn.objects.get(id=turn_id)
    user = request.user
    latest_users_list = turn.user_set.order_by('registration_date')
    users_in_the_turn_before_user = 0
    if latest_users_list:
        for i in latest_users_list:
            if i.id == user.id:
                break
            else:
                users_in_the_turn_before_user += 1
    if turn.all_waiting == 0:
        pass
    else:
        average_service_time = turn.all_service_time // turn.all_waiting
        expected_waiting_time = average_service_time * users_in_the_turn_before_user
        expected_hours, remainder = divmod(expected_waiting_time, 3600)
        expected_minutes, average_seconds = divmod(remainder, 60)

        if expected_minutes == 0 and average_seconds != 0:
            expected_minutes = 1

        turn.expected_hours = expected_hours
        turn.expected_minutes = expected_minutes
        turn.save()
