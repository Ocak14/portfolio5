from django.shortcuts import render
from .models import Contact, Blog, Category,Portfolio,Team
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
import math

class BlogDetailView(HitCountDetailView):
    model = Blog        # your model goes here
    count_hit = True    # set to True if you want it to try and count the hit
    context_object_name = 'blog'
    template_name = 'publication.html'
    slug_field = 'slug'

def blog_view(request):
    blogs = Blog.objects.all()
    blog_count = len(blogs)
    count_obj = 5
    page_count = math.ceil(blog_count / count_obj)
    paginator = Paginator(blogs, count_obj)

    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    categories = Category.objects.all()
    popular_blogs = list(blogs)  # Convert QuerySet to list
    popular_blogs.sort(key=lambda x: x.hit_count.hits, reverse=True)  # Sorting popular blogs by hit count

    context = {
        "categories": categories,
        'popular_blogs': popular_blogs[:2],
        'page_obj': page_obj,
        'page_count': range(1, page_count + 1),
        'page': int(page)
    }
    return render(request, 'blog.html', context)

def home_view(request):
    popular_blogs = Blog.objects.all()
    popular_blogs = list(popular_blogs)  # Convert QuerySet to list
    sorted(popular_blogs,key=lambda x: x.hit_count.hits, reverse=True)  # Sorting popular blogs by hit count


    context = {"popular_blogs": popular_blogs[:2]}
    return render(request, 'home.html', context)

def contact_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
            new_contact = Contact(name=name, email=email, content=content)
            new_contact.save()
            messages.success(request, "Sizning xabaringiz yuborildi!!!")
            return HttpResponseRedirect(reverse('home-page'))
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")

    return render(request, 'contact.html')

def portfolio_view(request):
    portfolio = Portfolio.objects.all()

    context = {
        
        "portfoios":portfolio,
    }
    return render(request,'portfolio.html', context)



def services_view(request):
    return render(request, 'services.html')

def team_view(request):
    team = Team.objects.all()
    context = {
        "team":team,
    }

    return render(request, 'team.html',context)
