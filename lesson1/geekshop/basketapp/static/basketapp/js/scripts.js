'use strict';

let Basket = null;

class CBasket {
    constructor(){
        this.setInputsEvent();
    }

    changeQuantity(id, value){
        if (!id || !value){
            return false;
        }

        $.get(
            `/basket/edit/${id}/${value}/`,
            function(data) {
                if (data.basket_item == undefined){
                    return false;
                }
                if (!data.basket_item.cost){
                    $(`.basket_record[data-id=${data.basket_item.id}]`).slideUp('fast', function(){
                        $(this).remove();
                    });
                }else{
                    $(`.basket_record[data-id=${data.basket_item.id}] .product_cost .value`).
                        text(data.basket_item.cost);
                    $(`.basket_record[data-id=${data.basket_item.id}] input`).val(data.basket_item.qty);
                }
                if (data.itog != undefined && data.itog.qty > 0){
                    $('.basket_summary strong:eq(0)').text(data.itog.qty);
                    $('.basket_summary strong:eq(1)').text(data.itog.sum);
                }else{
                    window.location.reload();
                }
            },
            'JSON'
        );
    }

    setInputsEvent(){
        if (!$('.basket_list input[type="number"]').length){
            return false;
        }

        $('.basket_list').on('click', 'input[type="number"]', () => {
            let input   = event.target,
                row     = $(input).parents('.basket_record');

            event.preventDefault();

            this.changeQuantity(row.data('id'), input.value);
        });
    }
}

$(document).ready(() => {
    Basket = new CBasket();
});
