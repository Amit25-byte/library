from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.decorators import login_required  # for function based views
from django.contrib.auth.mixins import LoginRequiredMixin # for classed based views
from django.contrib.auth.forms import UserCreationForm #it's technically a form.
from django.urls import reverse_lazy
# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_avail = BookInstance.objects.filter(status__exact='a').count()  

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_avail':num_instances_avail
    }

    return render(request,'catalog/index.html',context=context)


class BookCreate(LoginRequiredMixin,CreateView): #book_form.html(inside the module)
    model = Book 
    fields = '__all__'

class BookDetail(DetailView):
    model = Book

# function based views.
@login_required
def my_view(request):
    return render(request,'catalog/my_view.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'

class CheckedOutBookByUserView (LoginRequiredMixin,ListView):
    # list  all BookInstances but it will filter based off currently logged in user session.

    model = BookInstance
    template_name = 'catalog/profile.html'
    paginate_by = 5 # 5 books instances per page.

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)  # .all()