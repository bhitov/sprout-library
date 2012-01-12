from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import list_detail

import library.google_books as google_books

from urllib2 import urlopen

from library.models import Book, create_book
from library.forms import BookForm, UserForm, BookSearch

def login_required(function):
    """
    Login required decorator that uses the messages middleware.
    """
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            messages.error(request, "You must be logged in to do that")
            return redirect_to_login(request.path)
        else:
            return function(request, *args, **kw)
    return wrapper

def admin_required(function):
    """
    Admin required decorator that uses the messages middleware
    """
    def wrapper(request, *args, **kw):
        if not (request.user.is_authenticated() and request.user.is_superuser):
            messages.error(request, "Only admins may perform that action")
            return redirect('/books/')
        else:
            return function(request, *args, **kw)
    return wrapper


#note: this view is orphaned
def detail(request, book_id):
    """
    Displays info for a specific book.
    """
    entry = get_object_or_404(Book, pk=book_id)
    return render(request,
                  template='index.html',
                  dictionary={'books' : [entry]})

#TODO: convert from deprecated function based generic to class based generic
def book_list(request):
    """
    Displays a list of all books in the library
    """
    return list_detail.object_list(
                    request,
                    queryset=Book.objects.all(),
                    template_object_name='book')



def generic_conditional(request, condition, true_message, false_message, to):
    """
    Generic status testing for synchronous or asynchronous requests. Responds
    with true_message if the conditional is met, and false_message otherwise.
    if the request was synchronous, the user is redirected to 'to'.
    """
    if condition:
        message = true_message
        message_tag = 'success'
    else:
        message = false_message
        message_tag = 'error'
    if request.is_ajax():
        response = {}
        response['status'] = "S"
        response['message'] = message
        response['message_tag'] = message_tag
        json = simplejson.dumps(response)
        return HttpResponse(json, mimetype='application/json')
    else:
        messages.success(request, message)
        return HttpResponseRedirect(to)
    
@admin_required
def createa(request):
    """
    Asynchronous book creation
    """
    post = request.POST.copy()
    jsondata = {'result' : 'E'}
    try:
        create_book(post)
        jsondata['result'] = 'S'
    except:
        print 'form field error'
    json = simplejson.dumps(jsondata)
    return HttpResponse(json, mimetype='application/json')

@admin_required
def create(request):
    """
    Synchronous book creation
    """
    if request.method == 'POST':
        print request.POST
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect('/books/')
    else:
        form = BookForm()
    return render(request,
                  'addbook.html',
                  {'form': form})
        
@login_required
def scanx(request):
    """
    Loans a book to the current user based on the scanned barcode
    """
    if request.method == 'POST':
        barcode = request.POST['barcode']
        book = get_object_or_404(Book, barcode=barcode)
        return loanx(request, book.id, '/books/scan/')
    else:
        form = BookSearch()
        return render(request,
                      'scan.html',
                      {'form': form, 'title' : 'Scan'})

@admin_required
def delete(request, book_id):
    """
    Removes a book from the library
    """
    book = get_object_or_404(Book, pk=book_id)
    title = book.title
    book.delete()
    return HttpResponseRedirect('/books/')
    
@login_required
def loanx(request, book_id, to='/books/'):
    """
    Loans a book to the current user based on the 'borrow' link that
    the user clicked
    """
    book = get_object_or_404(Book, pk=book_id)
    return generic_conditional(request, book.loan_book(request.user),
                               "%s has been added to your books" % book.title,
                               "That book is already loaned out",
                               to)

@login_required
def return_book(request, book_id):
    """
    Returns a book to the library
    """
    book = get_object_or_404(Book, pk=book_id)
    return generic_conditional(request, book.return_book(request.user),
                               "%s has been returned" % book.title,
                               "You don't have that book",
                               '/books/user_books/')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/books/')
    else:
        form = UserForm()
    return render(request,
                  'registration/registration_form.html',
                  {'form': form})

@login_required
def user_books(request):
    """
    Lists books the user is currently borrowing
    """
    return list_detail.object_list(
                    request,
                    queryset=request.user.book_set.all(),
                    template_name='library/user_books.html',
                    template_object_name='book')

@admin_required
def search_googlex(request):
    """
    Searches google books for a book with the given barcode (isbn)
    """
    if request.method == 'POST':
        form = BookSearch(request.POST)
        barcode = form.data['barcode']
        response = google_books.search(barcode)
        print "I passed the loop"
        if request.is_ajax():
            print "I think I am ajax"
            json = simplejson.dumps(response)
            return HttpResponse(json, mimetype='application/json')
        return render(request,
                      'search.html',
                      {'book_list': response['book_list'], 'form': form, 
                       'title' :'Search Google'})
    else:
        book = Book(author='a', title='t')
        book.id = 'dummy'
        form = BookSearch()
        return render(request,
                      'search.html',
                      {'form': form, 'title' : 'Search Google',
                       'book_list' : [book]},)