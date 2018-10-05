from django.shortcuts import render


def error_404(request, exception, template_name='error/error_404.html'):
    return render(request, template_name, {}, status=404)


def error_500(request, template_name='error/error_500.html'):
    return render(request, template_name, {}, status=500)


def error_400(request, exception, template_name='error/error_400.html'):
    return render(request, template_name, {}, status=400)


def error_403(request, exception, template_name='error/error_403.html'):
    return render(request, template_name, {}, status=403)
