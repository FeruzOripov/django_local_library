from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import RenewBookForm


# Create your views here.

def index(request):
	"""
	View function for home page of site.
	"""
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
	num_authors = Author.objects.all().count()
	num_genres = Genre.objects.all().count()
	num_books_cont_word = Book.objects.filter(summary__contains = 's').count()

	#Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	return render(request, 'catalog/index.html', context = {
			'num_books':num_books,
			'num_instances':num_instances,
			'num_instances_available':num_instances_available,
			'num_authors':num_authors,
			'num_genres':num_genres,
			'num_books_cont_word':num_books_cont_word,
			'num_visits':num_visits,
		}
	)

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10

class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author

class AuthorDetailView(generic.DetailView):
	model = Author

class LoanedBooksUserListView(LoginRequiredMixin, generic.ListView):
	"""
	Generic class-based view listing books on loan to current user.
	"""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/loaned_books_list.html'
	permission_required = 'catalog.can_mark_returned'

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact = 'o')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_inst = get_object_or_404(BookInstance, pk = pk)

	if request.method == "POST":
		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()

			return HttpResponseRedirect(reverse('loaned_books'))

	else:
		proceed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
		form = RenewBookForm(initial = {'renewal_date':proceed_renewal_date,})

	return render(request, 'catalog/book_renew_librarian.html', {'form':form, 'bookinst':book_inst})


class AuthorCreate(PermissionRequiredMixin,CreateView):
	model = Author
	fields = '__all__'
	initial = {'date_of_death':'05/01/2018',}
	permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
	permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin,DeleteView):
	model = Author
	success_url = reverse_lazy('author')
	permission_required = 'catalog.can_mark_returned'

class BookCreate(PermissionRequiredMixin, CreateView):
	model = Book
	fields = '__all__'
	permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
	model = Book
	fields = '__all__'
	permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
	model = Book
	success_url = reverse_lazy('books')
	permission_required = 'catalog.can_mark_returned'