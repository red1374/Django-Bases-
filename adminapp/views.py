from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from authapp.models import ShopUser
from products.models import ProductCategory, Product

from adminapp.forms import ShopUserAdminEditForm
from adminapp.forms import ProductEditForm, ProductCategoryEditForm


def get_breadcrumb(list_items=(), object={}):
    """
    Create data to render page breadcrumbs
    :param list_items: categories list
    :param object: object with additional data
    :return:
    """
    breadcrumbs = [
        {
            'title': 'главная',
            'link': reverse('admin_staff:main')
        }
    ]

    if not list_items:
        return breadcrumbs

    for module in list_items:
        if module == 'users':
            breadcrumbs.append(
                {
                    'title': 'пользователи',
                    'link': reverse('admin_staff:users')
                }
            )
        elif module == 'products':
            breadcrumbs.append(
                {
                    'title': object.name,
                    'link': reverse('admin_staff:products', args=[object.pk])
                }
            )
        elif module == 'categories':
            breadcrumbs.append(
                {
                    'title': 'категории продуктов',
                    'link': reverse('admin_staff:categories')
                }
            )

    return breadcrumbs


@user_passes_test(lambda u: u.is_superuser)
def main(request):
    title = 'админка'
    context = {
        'title': title
    }
    return render(request, 'adminapp/main.html', context=context)


########################################################################################################################
# -- Users views -------------------------------------------------------------------------------------------------------
########################################################################################################################
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    ordering = ('-is_active', '-is_superuser', '-is_staff', 'username')
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'cписок пользователей'
        context['breadcrumbs'] = get_breadcrumb()
        context['page_url'] = 'adminapp:users_page'
        return context


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'создание пользователя'
        context['breadcrumbs'] = get_breadcrumb(('users',))
        return context


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'редактирование'
        context['post_title'] = self.object.username
        context['breadcrumbs'] = get_breadcrumb(('users', ))
        return context

    def get_success_url(self):
        if self.object.pk:
            return reverse('admin_staff:user_update', args=[self.object.pk])
        else:
            return reverse('admin_staff:users')


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UsersDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'удаление пользователя'
        context['user_title'] = self.object.username
        if self.object.first_name:
            context['user_title'] += ' (' + self.object.first_name
            if self.object.last_name:
                context['user_title'] += ' ' + self.object.last_name
            context['user_title'] += ')'

        context['breadcrumbs'] = get_breadcrumb(('users', ))
        return context


########################################################################################################################
# -- Products Categories views -----------------------------------------------------------------------------------------
########################################################################################################################
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    ordering = ('-is_active', 'name')
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'категории товаров'
        context['breadcrumbs'] = get_breadcrumb()
        context['page_url'] = 'adminapp:categories_page'
        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'создание категории'
        context['breadcrumbs'] = get_breadcrumb(('categories', ))
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # success_url = reverse_lazy('admin_staff:category_update')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'редактирование "' + self.object.name + '"'
        context['breadcrumbs'] = get_breadcrumb(('categories', ))
        return context

    def get_success_url(self):
        if self.object.pk:
            return reverse('admin_staff:category_update', args=[self.object.pk])
        else:
            return reverse('admin_staff:categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']

        if discount:
            self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)

########################################################################################################################
# -- Products views ---------------------------------------------------------------------------------------------------
########################################################################################################################
class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    ordering = ('-is_active', 'name')
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(category__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])

        context['title'] = 'Товары раздела "' + category.name + '"'
        context['category'] = category
        context['breadcrumbs'] = get_breadcrumb(('categories',))
        context['page_url'] = 'adminapp:products_page'
        context['page_pk'] = self.kwargs['pk']
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        self.category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return {'category': self.category}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'cоздание товара'
        context['breadcrumbs'] = get_breadcrumb(('categories', 'products'), self.category)
        return context

    def get_success_url(self):
        return reverse('admin_staff:products', args=[self.category.pk])


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'редактирование "' + self.object.name + '"'
        context['breadcrumbs'] = get_breadcrumb(('categories', 'products'), self.object.category)
        return context

    def get_success_url(self):
        return reverse('admin_staff:product_update', args=[self.kwargs['pk']])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url())

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'удаление товара'

        context['breadcrumbs'] = get_breadcrumb(('categories', 'products'), self.object.category)
        return context

    def get_success_url(self):
        return reverse('admin_staff:products', args=[self.object.category.pk])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        context['breadcrumbs'] = get_breadcrumb(('categories', 'products'), self.object.category)

        return context
