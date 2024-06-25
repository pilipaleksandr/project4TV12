from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_add.html', {'form': form})

def book_edit(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form})

def book_delete(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', {'book': book})

def book_search(request):
    query = request.GET.get('q')
    results = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    return render(request, 'books/book_search.html', {'results': results})

def book_statistics(request):
    books = Book.objects.all()
    df = pd.DataFrame(list(books.values('genre')))
    genre_counts = df['genre'].value_counts()

    plt.figure(figsize=(10, 5))
    genre_counts.plot(kind='bar', color='skyblue')
    plt.title('Number of Books by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Books')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'books/book_statistics.html', {'data': uri})
