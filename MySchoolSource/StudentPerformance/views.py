from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from .forms import *

from aagam_packages.django.view_extensions import generic


# Create your views here.


def paper_entry_create(request):
    form = PaperEntryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponseRedirect("/")
    return render(request, "test/test.html", {'form': form})



def paper_pattern_entry_create_popup(request):
    form = PaperPatternEntryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_author". This is the element id in the form

        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))

    return render(request, "author_form.html", {"form": form})
