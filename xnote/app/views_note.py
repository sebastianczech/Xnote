from django.shortcuts import render


def note(request):
    return render(request, 'app/note.html', { })