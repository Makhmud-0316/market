from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from .forms import *
from .models import Category, Product, Cart, CartItem


class MarketView(TemplateView):
    template_name = 'market/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = []
        context['categories'] = []
        return context


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'market/categories_list.html'
    context_object_name = 'categories'
    login_url = 'login'
    paginate_by = 5


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'market/category_detail.html'
    context_object_name = 'category'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(category=self.object)
        paginator = Paginator(products, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['products'] = page_obj.object_list
        return context


def deals(request):
    return render(request, 'market/deals.html')


def services(request):
    return render(request, 'market/services.html')


class LoginUser(LoginView):
    template_name = 'market/login.html'
    form_class = LogInForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class SignUser(CreateView):
    form_class = SignUpForm
    template_name = 'market/sign.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def logout_user(request):
    logout(request)
    return redirect('home')


# CART VIEWS

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'market/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        # Редирект на страницу категории продукта
        return redirect('category_detail', pk=product.category.id)
    else:
        return redirect('categories')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect('view_cart')
