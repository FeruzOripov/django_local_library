from . import views
from django.urls import path

urlpatterns = [
	path('', views.index, name = 'index'),
	path('books/', views.BookListView.as_view(), name = 'books'),
	path('books/<int:pk>', views.BookDetailView.as_view(), name = 'book-detail'),
	path('author/', views.AuthorListView.as_view(), name = 'author'),
	path('author/<int:pk>', views.AuthorDetailView.as_view(), name = 'author-detail'),
	path('mybooks/', views.LoanedBooksUserListView.as_view(), name = 'my_borrowed'),
	path('loaned/', views.LoanedBooksListView.as_view(), name = 'loaned_books'),
	path('book/<slug:pk>/renew/', views.renew_book_librarian, name = 'renew_book_librarian'),
	path('author/create/', views.AuthorCreate.as_view(), name = 'author_create'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name = 'author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'author_delete'),
	path('book/create/', views.BookCreate.as_view(), name = 'book_create'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name = 'book_update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book_delete'),
]