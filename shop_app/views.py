from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView, UpdateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from shop_app.models import Category, Product, Comments, UserProfile
from orders.models import Order, OrderItem
from coupons.forms import ProfileEditForm
from cart.forms import CartAddProductForm
from shop_app.forms import CommentForm


class ProductList(View):
    """ Главная страница (выводим первые 6 товаров) """

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)[:6]

        context = {
            'products': products,
        }

        return render(request, 'shop_app/product_list.html', context)


class ProductFilterView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            products = Product.objects.filter(
                title__icontains=search_query,
            )
        else:
            products = Product.objects.filter(available=True)

        p = Paginator(products, 1)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {
            'categories': categories,
            'products': products,
            'page_obj': page_obj,
        }

        return render(request, 'shop_app/category_product.html', context)


class CategoryProductView(View):
    """ Выводим все товары, которые относятся к конкретной категории """

    def get(self, request, category_slug=None, *args, **kwargs):
        category = None
        categories = Category.objects.all()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(
                available=True, category=category)

        p = Paginator(products, 1)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {
            'category': category,
            'products': products,
            'categories': categories,
            'page_obj': page_obj,
        }

        return render(request, 'shop_app/category_product.html', context)


class Search(ListView):
    """Поиск фильмов"""

    template_name = 'shop_app/category_product.html'

    def get_queryset(self):
        return Product.objects.filter(
            title__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class ProductDetail(View):
    """ Детальный вывод конкретного товара """

    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        cart_product_form = CartAddProductForm()
        comment_product_form = CommentForm()

        comments = Comments.objects.filter(
            product=product).order_by('-created_at')

        context = {
            'product': product,
            'cart_product_form': cart_product_form,
            'comment_product_form': comment_product_form,
            'comments': comments,
        }

        return render(request, 'shop_app/product_detail.html', context)


class ProfileView(View):
    """ Выводим страницу профиля """

    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user_comments = Comments.objects.filter(author=profile.user.id)[:10]
        order_details = Order.objects.filter(cart_owner=profile.user.id)
        order_products = OrderItem.objects.filter(order__in=order_details)
        user = profile.user

        context = {
            'user': user,
            'profile': profile,
            'user_comments': user_comments,
            'order_details': order_details,
            'order_products': order_products,
        }

        return render(request, 'profile/profile_view.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Редактирование профиля """

    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'profile/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('shop:profile_edit', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddComment(LoginRequiredMixin, View):
    """ Добавление комментария """

    def post(self, request, pk):
        form = CommentForm(request.POST)
        product = Product.objects.get(id=pk)

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            form.save()

        return redirect(product.get_absolute_url())


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Удаление комментария """

    model = Comments
    template_name = 'shop_app/comment_delete.html'

    def get_success_url(self):
        slug = self.kwargs['product_slug']
        return reverse_lazy('shop:product_detail', kwargs={'slug': slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class AddLikeComment(LoginRequiredMixin, View):
    """ Добавление лайка к комментарию """

    def post(self, request, pk, *args, **kwargs):
        comment = Comments.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', 'product_detail')
        return HttpResponseRedirect(next)


class AddDislikeComment(LoginRequiredMixin, View):
    """ Добавление дизлайка к комментарию """

    def post(self, request, pk, *args, **kwargs):
        comment = Comments.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', 'product_detail')
        return HttpResponseRedirect(next)
