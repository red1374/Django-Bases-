'use strict';

let Order =  null;

class COrder {
    order_total_quantity = 0;
    order_total_cost = 0;

    constructor(){
        this.getSummery();
        this.setInputEvents();
        this.initPlugins();
    }

    setInputEvents(){
        if ($('.field-quantity').length){
            $('.field-quantity').change(function(){
                let parent_tr = $(this).parents('tr'),
                    price = parent_tr.find('.field-price');

                parent_tr.find('.field-summ').text(CUtils.number_format(
                    CUtils.getFloatValue(price.data('value')) * $(this).val(),
                    2, ',', ' '
                ));

                Order.updateSummery();
            });
        }
    }

    getSummery(){
        if (!$('.order_form .formset_row').length){
            return false;
        }
        let qty = 0, total = 0;

        $('.order_form .formset_row:visible').each(function(){
            if (parseInt($(this).find('.field-quantity').val())){
                qty += parseInt($(this).find('.field-quantity').val());

                if (CUtils.getFloatValue($(this).find('.field-price').data('value'))){
                    total += CUtils.getFloatValue($(this).find('.field-price').data('value')) * parseInt($(this).find('.field-quantity').val());
                }
            }
        });

        this.order_total_quantity = qty;
        this.order_total_cost = total;
    }

    updateSummery(){
        this.getSummery();

        if (this.order_total_quantity){
            $('#order_total_quantity').data('value', this.order_total_quantity).
                text(this.order_total_quantity);
        }
        if (this.order_total_cost){
            $('#order_total_cost').data('value', this.order_total_cost).
                text(CUtils.number_format(this.order_total_cost, 2, '.', ' ')
            );
        }
    }

    initPlugins(){
        if (!$('.formset_row').length){
            return false;
        }

        $('.formset_row').formset({
            addText: 'добавить продукт',
            deleteText: 'удалить',
            prefix: 'orderitems',
            removed: function(row){
                Order.updateSummery();
            }
        });

    }
}

$(document).ready(function(){
    Order = new COrder();
});
