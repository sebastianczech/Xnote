# import json

from bson import json_util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404

from . import mongoDatabase
from .forms import LogForm
from .models import Log


def log(request):
    logs_all = Log.objects.all().order_by('-modified')
    paginator = Paginator(logs_all, 10)

    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    # for document_log in mongoDatabase.log.find():
        # json_object = json_util.dumps(document_log)
        # print("/log: " + json_object)

    return render(request, 'app/log.html', {'logs': logs})


def log_detail(request, id):
    log = get_object_or_404(Log, id=id)
    # utils.console(log.json)
    # log.json = json.dumps(log.json, indent=4, sort_keys=False, separators=(',', ': '))
    return render(request, 'app/log_detail.html', {'log': log})


def log_add(request):
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [Log.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.insert_one(python_list[0])
            # print("/log/add: " + json_object + "; result: " + str(result.inserted_id))

            return redirect('log_detail', id=post.id)
    else:
        form = LogForm()
    return render(request, 'app/log_form.html', {'form': form,
                                                 'title': 'New log',
                                                 'button': 'Add'})


def log_edit(request, id):
    log = get_object_or_404(Log, id=id)
    if request.method == "POST":
        form = LogForm(request.POST, instance=log)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            json_list = serialize('json', [Log.objects.get(id=post.id)])
            python_list = json_util.loads(json_list)
            json_object = json_util.dumps(python_list[0])
            result = mongoDatabase.log.replace_one({"pk": post.id}, python_list[0])
            # print("/log/edit: " + json_object + "; result: " + str(result.matched_count))

            return redirect('log_detail', id=post.id)
    else:
        form = LogForm(instance=log)
    return render(request, 'app/log_form.html', {'form': form,
                                                 'title': 'Edit log',
                                                 'button': 'Save',
                                                 'id': log.id})


def log_remove(request, id):
    log = get_object_or_404(Log, id=id)
    Log.objects.get(id=id).delete()

    json_list = serialize('json', [log])
    python_list = json_util.loads(json_list)
    json_object = json_util.dumps(python_list[0])
    result = mongoDatabase.log.delete_one({"pk": int(id)})
    # print("/log/remove: " + json_object + "; result: " + str(result.deleted_count))

    return redirect('log')