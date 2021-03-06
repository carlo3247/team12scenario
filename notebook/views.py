from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect

from .forms import SearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter

from .models import Note, Notebook


class NotebookView(generic.ListView):
    template_name = 'notebook/overview.html'

    context_object_name = 'note_books'

    def get_queryset(self):
        return Notebook.objects.all()


class NoteView(generic.ListView):

    template_name = 'notebook/note.html'

    context_object_name = 'notes'

    def get_queryset(self):
        notebook = get_object_or_404(Notebook, pk=self.kwargs['pk'])
        return Note.objects.filter(notebook__exact=notebook)


class NoteFilter(BaseFilter):
    search_fields = {
        'search_title' : ['title'],
        'search_text' : ['text'],
    }

class NoteSearchList(SearchListView):
    model = Note
    paginate_by = 30
    template_name = "notebook/search.html"
    form_class = SearchForm
    filter_class = NoteFilter


class DetailedNote(generic.DetailView):
    model = Note

    template_name = 'notebook/details.html'

    def get_object(self):
        note_id = self.kwargs['id']
        note = get_object_or_404(Note, id=note_id)
        return note


class AddNote(generic.edit.CreateView):

    model = Note
    fields = ['title', 'text']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.notebook = get_object_or_404(Notebook, pk=self.kwargs['pk'])
        instance.author = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('notebook:all-notes', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse_lazy('notebook:home')

class EditNote(generic.edit.UpdateView):

    model = Note
    fields = ['title', 'text']

    def get_object(self):
        note_id = self.kwargs['id']
        note = get_object_or_404(Note, id=note_id)
        return note

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('notebook:all-notes', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse_lazy('notebook:home')


class DeleteNote(generic.edit.DeleteView):

    model = Note

    def get_object(self):
        note_id = self.kwargs['id']
        note = get_object_or_404(Note, id=note_id)
        return note

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('notebook:all-notes', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse_lazy('notebook:home')


class AddNotebook(generic.edit.CreateView):

    model = Notebook
    fields = ['name']

class DeleteNotebook(generic.edit.DeleteView):

    model = Notebook
    success_url = reverse_lazy('notebook:home')
