from django.shortcuts import render


def dashboard(request, project_id):
    return render(request, 'mainapp/dashboard.html')


def issues(request, project_id):
    return render(request, 'mainapp/issues.html')


def statistics(request, project_id):
    return render(request, 'mainapp/statistics.html')


def files(request, project_id):
    return render(request, 'mainapp/files.html')


def wiki(request, project_id):
    return render(request, 'mainapp/wiki.html')


def settings(request, project_id):
    return render(request, 'mainapp/settings.html')