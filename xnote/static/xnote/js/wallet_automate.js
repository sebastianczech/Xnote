$(document).ready(function(){
    console.log("wallet automate loaded");

    $("#id_exchange_rate, #id_value, #id_operation").change(function() {
        var operation = $("#id_operation").val();
        var exchange_rate = $("#id_exchange_rate").val();
        var value = $("#id_value").val();

        console.log(operation + " with exchange rate " + exchange_rate);
        if (operation == "purchase") {
            $("#id_calculated_value").val(Math.round((value / exchange_rate) * 100) / 100);
        } else if (operation == "sale") {
            $("#id_calculated_value").val(Math.round((value * exchange_rate) * 100) / 100);
        }

        Materialize.updateTextFields();
    });
});