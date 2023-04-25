from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from turns.models import Turn
from turns.forms import TurnForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError


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
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        latest_users_list = turn.user_set.order_by('registration_date')
        users_id_list = [i.id for i in latest_users_list]
        if users_id_list:
            first_in_the_turn = users_id_list[0]
        else:
            first_in_the_turn = -1
        if not latest_users_list:
            turn.time_at_the_top = None
            turn.save()
        expected_hours, expected_minutes = users_check(request, turn_id)
        return render(request, 'turns/detail.html', {'turn': turn, 'latest_users_list': latest_users_list,
                                                     'users_id_list': users_id_list,
                                                     'first_in_the_turn': first_in_the_turn,
                                                     'expected_hours': expected_hours,
                                                     'expected_minutes': expected_minutes})


def open_turn(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        user = request.user
        if user.id == turn.creator or user.username == 'admin':
            if not turn.status:
                turn.status = True
                turn.save()
            else:
                return render(request, 'error.html', {'error_message': 'Черга вже відкрита!'})
        else:
            return render(request, 'error.html', {'error_message': 'Ви не хазяїн черги!'})
        return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def close_turn(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        user = request.user
        if user.id == turn.creator or user.username == 'admin':
            if turn.status:
                turn.status = False
                turn.save()
            else:
                return render(request, 'error.html', {'error_message': 'Черга вже закрита!'})
        else:
            return render(request, 'error.html', {'error_message': 'Ви не хазяїн черги!'})
        return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def delete_turn(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        user = request.user
        if user.id == turn.creator or user.username == 'admin':
            turn.delete()
            return redirect('index')
        else:
            return render(request, 'error.html', {'error_message': 'Ви не хазяїн черги!'})


def turn_register(request, turn_id):
    user = request.user
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        try:
            turn.user_set.create(username=user.username, first_name=user.first_name, last_name=user.last_name,
                                 registration_date=timezone.now(), id=user.id)
        except IntegrityError:
            return render(request, 'error.html', {'error_message': 'Ви вже зареєстровані в іншій черзі!'})
        else:
            latest_users_list = turn.user_set.order_by('registration_date')
            if user.id == latest_users_list[0].id:
                position_check(request, turn_id)
            return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def turn_unregister(request, turn_id):
    user = request.user
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        latest_users_list = turn.user_set.order_by('registration_date')
        if user.id == latest_users_list[0].id:
            flag = True
        else:
            flag = False
        try:
            latest_users_list[0].delete()
        except IndexError:
            return render(request, 'error.html', {'error_message': 'Ви не в черзі!'})
        else:
            if flag is True:
                if latest_users_list:
                    position_check(request, turn_id)
        users_check(request, turn_id)
        return HttpResponseRedirect(reverse('detail', args=(turn.id,)))


def next_turn_user(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        user = request.user
        if user.id == turn.creator or user.username == 'admin':
            latest_users_list = turn.user_set.order_by('registration_date')
            if not latest_users_list:
                return render(request, 'error.html', {'error_message': 'Черга порожня!'})
            time_check(request, turn_id)
            latest_users_list[0].delete()
            if latest_users_list:
                position_check(request, turn_id)
            users_check(request, turn_id)
            return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
        else:
            return render(request, 'error.html', {'error_message': 'Ви не хазяїн черги!'})


def delete_turn_user(request, turn_id):
    try:
        turn = Turn.objects.get(id=turn_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {'error_message': 'Черга не знайдена!'})
    else:
        user = request.user
        if user.id == turn.creator or user.username == 'admin':
            if request.method == 'POST':
                latest_users_list = turn.user_set.order_by('registration_date')
                user_id = request.POST['user']
                if user_id == str(latest_users_list[0].id):
                    flag = True
                else:
                    flag = False
                try:
                    for i in range(len(latest_users_list)):
                        if user_id == str(latest_users_list[i].id):
                            latest_users_list[i].delete()
                            break
                except IndexError:
                    return render(request, 'error.html', {'error_message': 'Такого очікувача не існує!'})
                else:
                    if flag is True:
                        if latest_users_list:
                            position_check(request, turn_id)
                    users_check(request, turn_id)
                    return HttpResponseRedirect(reverse('detail', args=(turn.id,)))
        else:
            return render(request, 'error.html', {'error_message': 'Ви не хазяїн черги!'})


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
        expected_hours = -1
        expected_minutes = -1
    else:
        average_service_time = turn.all_service_time // turn.all_waiting
        expected_waiting_time = average_service_time * users_in_the_turn_before_user
        expected_hours, remainder = divmod(expected_waiting_time, 3600)
        expected_minutes, expected_seconds = divmod(remainder, 60)

        if expected_minutes == 0 and expected_seconds != 0:
            expected_minutes = 1

    return expected_hours, expected_minutes
