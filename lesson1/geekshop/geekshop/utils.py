from django.utils.formats import number_format


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_price_formated(number):
    return number_format(number, decimal_pos=0, force_grouping=True)
