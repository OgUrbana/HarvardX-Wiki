from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
import markdown2
import random
from . import util
from django.core.files.storage import default_storage

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'new-title', 'placeholder':'Title'}), label="")
    new_entry = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'new-entry'}), label="")

class editForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title', 'id':'edit-title'}), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id':'edit-entry'}), label="")

class searchForm(forms.Form):
    searchName = forms.CharField(widget = forms.TextInput(attrs={'class':'search', 'type':'text', 'name':'q', 'placeholder':'Search Encyclopedia'}), label="")

def index(request):
    searchingForm = searchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": searchingForm
    })

def entry(request, title):
    entry = util.get_entry(title)
    searchingForm = searchForm()
    if entry is None:
        return render(request, "encyclopedia/error404.html", {
            "title": title,
            "searchForm": searchingForm
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry),
            "searchForm": searchingForm
        })

def edit(request, title):
    searchingForm = searchForm()
    if request.method == "POST":
        content = util.get_entry(title)
        getForm = editForm(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            "editForm": getForm,
            "title": title,
            "entry": content,
            "searchForm": searchingForm
        })

def submitEdit(request, title):
    searchingForm = searchForm()
    if request.method == "POST":
        editedEntry = editForm(request.POST)
        if editedEntry.is_valid():
            edited_title = editedEntry.cleaned_data["title"]
            content = editedEntry.cleaned_data["content"]
            if edited_title != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(edited_title, content)
            entry = util.get_entry(edited_title)
        return render(request, "encyclopedia/entry.html", {
            "title": edited_title,
            "entry": markdown2.markdown(entry),
            "searchForm": searchingForm
        })
        
def create(request):
    searchingForm = searchForm()
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            new_entry = form.cleaned_data["new_entry"]
            listEntries = util.list_entries()

            for entry in listEntries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": NewEntryForm(),
                        "error": "That wiki is already made!",
                        "searchForm": searchingForm
                    })

            entryTitle = f"# {title}"
            entryInput = f"\n {new_entry}"
            page = entryTitle + entryInput
            util.save_entry(title, page)
            newEntry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(newEntry),
                "searchForm": searchingForm
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm(),
        "searchForm": searchingForm
    })

def randomPage(request): 
    searchingForm = searchForm()
    listEntries = util.list_entries()
    randomTitle = random.choice(listEntries)
    content = util.get_entry(randomTitle)
    # print(listEntries)
    # print(randomTitle)  
    return render(request, "encyclopedia/entry.html", {
        "title": randomTitle,
        "entry": markdown2.markdown(content),
        "searchForm": searchingForm
    })

def search(request):
    searchingForm = searchForm()
    listEntries = util.list_entries()
    similarEntries = []
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            searchInput = form.cleaned_data["searchName"]
            for entry in listEntries:
                if searchInput.lower() == entry.lower():
                    title = entry
                    content = util.get_entry(title)
                    return render(request, "encyclopedia/entry.html", {
                        "title": title,
                        "entry": markdown2.markdown(content),
                        "searchForm": searchForm
                    })
                if searchInput.lower() in entry.lower():
                    similarEntries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entry": similarEntries,
                "searchForm": searchingForm
            })
