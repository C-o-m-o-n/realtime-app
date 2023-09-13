from django.shortcuts import render

def main(request):
    statistics = Statistic.objects.all()
    return render(request, 'base/main.html', {'statistics': statistics})

def dashboard(request, slug):
    return render(request, 'base/dashboard.html', {})

def lobby(request):
    return render(request, 'notification/lobby.html')
