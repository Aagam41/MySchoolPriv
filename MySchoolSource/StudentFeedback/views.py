from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from StudentPerformance import models



def add_user(request):
    return render(request, 'add_user.html')


def user_detail(request):
    return render(request, 'user_detail.html')

def edit_user(request):
    return render(request, 'edit_user.html')

def class_detail(request):
    data = models.StandardSection.objects.all()
    return render(request, 'class_detail.html', {"da": data})

'''def edit_class(request, standard):
    if request.method == 'POST':
        pi = sp.StandardSection.objects.get(pk=standard)
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = sp.StandardSection(section=sec, standard=std, instance=pi)
        data.save()
    else:
        pi = sp.StandardSection.objects.get(pk=standard)
        data = sp.StandardSection(instance=pi)
        return render(request, 'edit_class.html', {'da': data})'''



def add_class(request):
    if request.method == 'POST':
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = models.StandardSection(section=sec, standard_id=std)
        data.save()
        #return HttpResponseRedirect('/class_detail')
        return render(request, 'add_class.html')
    else:
        return render(request, 'add_class.html')


def delete_class(request, standard_section_id):
    if request.method == "POST":
        pi = models.StandardSection.objects.get(standard_section_id=standard_section_id)
        pi.delete()
        return HttpResponseRedirect('/class_detail.html')
        #return render(request, 'class_detail.html')

