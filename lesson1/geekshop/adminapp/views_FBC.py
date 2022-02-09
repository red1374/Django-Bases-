from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render

from authapp.models import ShopUser
from products.models import ProductCategory, Product

from authapp.forms import ShopUserRegisterForm
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


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'cписок пользователей'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list,
        'breadcrumbs': get_breadcrumb()
    }

    return render(request, 'adminapp/users.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'user_form': user_form,
        'breadcrumbs': get_breadcrumb(('users', )),
    }

    return render(request, 'adminapp/user_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    post_title = edit_user.username

    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        user_form = ShopUserRegisterForm(instance=edit_user)

    context = {
        'title': title,
        'post_title': post_title,
        'user_form': user_form,
        'breadcrumbs': get_breadcrumb(('users',)),
    }

    return render(request, 'adminapp/user_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'удаление пользователя'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    user_title = user.username
    if user.first_name:
        user_title += ' (' + user.first_name
        if user.last_name:
            user_title += ' ' + user.last_name
        user_title += ')'

    context = {
        'title': title,
        'user_to_delete': user,
        'user_title': user_title,
        'breadcrumbs': get_breadcrumb(('users',)),
    }

    return render(request, 'adminapp/user_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'категории товаров'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list,
        'breadcrumbs': get_breadcrumb(),
    }

    return render(request, 'adminapp/categories.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'Создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'form': category_form,
        'breadcrumbs': get_breadcrumb(('categories', )),
    }

    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'редактирование "'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    title += edit_category.name + '"'
    context = {
        'title': title,
        'update_form': edit_form,
        'breadcrumbs': get_breadcrumb(('categories', )),
    }

    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category': category,
    }

    return render(request, 'adminapp/category_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'Товары раздела "'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    title += category.name + '"'
    context = {
        'title': title,
        'category': category,
        'objects': products_list,
        'breadcrumbs': get_breadcrumb(('categories',)),
    }

    return render(request, 'adminapp/products.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'Создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'form': product_form,
        'breadcrumbs': get_breadcrumb(('categories', 'products'), category),
    }

    return render(request, 'adminapp/product_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)
    content = {
        'title': product.name,
        'object': product,
        'breadcrumbs': get_breadcrumb(('categories', 'products'), product.category),
    }

    return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'редактирование "'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    title += edit_product.name + '"'
    context = {
        'title': title,
        'form': edit_form,
        'category': edit_product.category,
        'breadcrumbs': get_breadcrumb(('categories', 'products'), edit_product.category),
    }

    return render(request, 'adminapp/product_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'object': product,
    }

    return render(request, 'adminapp/product_delete.html', context=context)
