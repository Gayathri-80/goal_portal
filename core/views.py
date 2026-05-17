from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Goal, Step


# LOGIN
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("/login/")


# DASHBOARD (HACKATHON UPGRADE)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    goals = Goal.objects.filter(user=request.user)

    total_goals = goals.count()
    completed_goals = 0

    streak = 0
    badges = []

    for goal in goals:
        total_steps = goal.steps.count()
        done_steps = goal.steps.filter(completed=True).count()

        progress = int((done_steps / total_steps) * 100) if total_steps else 0
        goal.progress = progress

        if progress == 100:
            goal.status = "Completed 🎉"
            completed_goals += 1
            badges.append("🏆 Goal Master")
        elif progress > 50:
            goal.status = "Almost There 🔥"
        elif progress > 0:
            goal.status = "In Progress 🚀"
        else:
            goal.status = "Not Started ⚪"

        if progress > 0:
            streak += 1

    overall_progress = int((completed_goals / total_goals) * 100) if total_goals else 0

    if completed_goals >= 1:
        badges.append("🥇 First Achievement")
    if overall_progress >= 50:
        badges.append("⚡ Halfway Hero")

    return render(request, "dashboard.html", {
        "goals": goals,
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "overall_progress": overall_progress,
        "streak": streak,
        "badges": badges
    })


# CREATE GOAL (FIXED + STEPS SUPPORT)
def create_goal(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == "POST":
        title = request.POST.get("title")
        steps = request.POST.getlist("steps")

        goal = Goal.objects.create(user=request.user, title=title)

        for s in steps:
            if s and s.strip():
                Step.objects.create(goal=goal, title=s)

        return redirect("/dashboard/")

    return render(request, "create.html")


# TOGGLE STEP
def toggle_step(request, id):
    step = get_object_or_404(Step, id=id)
    step.completed = not step.completed
    step.save()
    return redirect("/dashboard/")