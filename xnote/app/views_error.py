from django.shortcuts import render


def bad_request(request, exception):
    return render(request, 'app/error.html', {'error_message': 'Bad request'})


def permission_denied(request, exception):
    return render(request, 'app/error.html', {'error_message': 'Permission denied'})


def page_not_found(request, exception):
    return render(request, 'app/error.html', {'error_message': 'Page not found'})


def server_error(request):
    return render(request, 'app/error.html', {'error_message': 'Server error'})