'use strict';

let Order =  null;

class COrder {
    order_total_quantity = 0;
    order_total_cost = 0;
    price_template = '<span class="#CLASS#" data-value="#PRICE#">#PRICE_FORMATED#</span> руб'
    row_id = 0

    constructor(){
        this.getSummery();
        this.setInputEvents();
        this.initPlugins();
    }

    getPriceHtml(price, class_name = 'field-price'){
        if (!price){
            return '';
        }

        return this.price_template.
            replace('#CLASS#', class_name).
            replace('#PRICE#', price).
            replace('#PRICE_FORMATED#', CUtils.number_format(price, 2, ',', ' '));
    }
    /*
     Set page form inputs events
    */
    setInputEvents(){
        /* -- Change order item quantity event ---------------------------------------------------------------------- */
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

        /* -- Change order product event ---------------------------------------------------------------------------- */
        if ($('.field-product').length){
            $('.field-product').change(function(){
                Order.row_id = $(this).parents('tr').index();
                Order.getProductPrice(this.value);
                $('.field-product').attr('disabled', 'disabled');
            });
        }
    }

    /*
    Get product price
    */
    getProductPrice(product_id){
        if (!product_id){
            return false;
        }

        $.get(
            `/orders/product/${product_id}/price/`,
            function(data) {
                if (data.product_id == undefined){
                    return false;
                }
                let parent_tr = $(`.formset_row:eq(${Order.row_id})`);
                parent_tr.find('.td-price').html(Order.getPriceHtml(data.price)).
                    find('.td-price span').data('value', data.price);

                $('.field-product').removeAttr('disabled');
                if (!$.trim(parent_tr.find('.td-summ').text())){
                    parent_tr.find('.td-summ').html(Order.price_template).
                        find('span').addClass('field-summ');
                }
                parent_tr.find('.td-quantity input').trigger('change');
            },
            'JSON'
        );
    }

    /*
     Get order summary information
    */
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

    /*
    Update order summery information
    */
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

    /*
    Init page plugins
    */
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
