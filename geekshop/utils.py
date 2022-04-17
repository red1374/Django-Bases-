import json

from django.utils.formats import number_format


def get_file_data(file_name=''):
    if not file_name:
        return False

    with open(file_name) as data_file:
        data = json.load(data_file)

    return data


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_price_format(number):
    return number_format(number, decimal_pos=0, force_grouping=True)
