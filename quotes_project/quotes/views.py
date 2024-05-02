from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quote, Author
from django.core.paginator import Paginator
from .forms import AuthorForm, QuoteForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'quotes/index.html', {'quotes': quotes, 'page': page})


def author_detail(request, fullname):
    author = Author.objects.get(fullname=fullname)
    return render(request, 'quotes/author_detail.html', {'author': author})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.author = request.user
            quote.save()
            return redirect('quotes:index')

    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            if Author.objects.filter(fullname=fullname).exists():
                form.add_error('fullname', 'Author with this name already exists.')
            else:
                form.save()
                return redirect('quotes:index')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})
