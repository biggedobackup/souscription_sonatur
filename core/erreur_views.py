from django.shortcuts import render

def handler_400_view(request, exception):
    return render(request, "erreurs/400.html", status=400)


def handler_403_view(request, exception):
    return render(request, "erreurs/403.html", status=403)


def handler_404_view(request, exception):
    return render(request, "erreurs/404.html", status=404)


def handler_500_view(request):
    return render(request, "erreurs/500.html", status=500)
