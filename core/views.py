from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Habit, CheckIn, Partnership
from .forms import HabitForm, CheckInForm, PartnershipForm
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
       
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('habit_list')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('habit_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'core/habit_list.html', {'habits': habits})


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)   # build the object, don't save to DB yet
            habit.user = request.user          # manually set the missing field
            habit.save()                       # NOW save to DB
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'core/habit_form.html', {'form': form})


@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'core/habit_form.html', {'form': form})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit_list')
    return render(request, 'core/habit_confirm_delete.html', {'habit': habit})

@login_required
def checkin_list(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    return render(request, 'core/habit_detail.html', {'habit': habit})

@login_required
def checkin_create(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.habit = habit
            checkin.save()

            streak, created = Streak.objects.get_or_create(habit=habit)

            if streak.last_checkin_date is None:
                streak.current_streak = 1
            elif (checkin.date - streak.last_checkin_date).days == 1:
                streak.current_streak += 1
            else:
                streak.current_streak = 1

            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak

            streak.last_checkin_date = checkin.date
            streak.save()

            return redirect('habit_list')
    else:
        form = CheckInForm()
    return render(request, 'core/checkin_form.html', {'form': form, 'habit': habit})

@login_required
def checkin_update(request, habit_id, checkin_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    checkin = get_object_or_404(CheckIn, pk=checkin_id, habit=habit)
    if request.method == 'POST':
        form = CheckInForm(request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = CheckInForm(instance=checkin)
    return render(request, 'core/checkin_form.html', {'form': form, 'habit': habit})


@login_required
def checkin_delete(request, habit_id, checkin_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    checkin = get_object_or_404(CheckIn, pk=checkin_id, habit=habit)
    if request.method == 'POST':
        checkin.delete()
        return redirect('habit_list')
    return render(request, 'core/checkin_confirm_delete.html', {'checkin': checkin, 'habit': habit})

