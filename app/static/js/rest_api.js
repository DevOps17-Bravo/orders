$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.order_id);
        $("#customer_id").val(res.customer_id);
        $("#order_total").val(res.order_total);
        $("#order_time").val(res.order_time);
        $("#order_status").val(res.order_status);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val();
        $("#customer_id").val();
        $("#order_total").val();
        $("#order_time").val();
        $("#order_status").val();
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        var order_id = $("#order_id").val();
        var customer_id = $("#customer_id").val();
        var order_total = $("#order_total").val();
        var order_time = $("#order_time").val();
        var order_status = $("#order_status").val();

        var data = {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_total": order_total,
            "order_time": order_time,
            "order_status": order_status
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var customer_id = $("#customer_id").val();
        var order_total = $("#order_total").val();
        var order_time = $("#order_time").val();
        var order_status = $("#order_status").val();

        var data = {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_total": order_total,
            "order_time": order_time,
            "order_status": order_status
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + pet_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Order with ID [" + res.order_id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for an Order
    // ****************************************

    $("#search-btn").click(function () {

        var order_id = $("#order_id").val();
        var customer_id = $("#customer_id").val();
        var order_total = $("#order_total").val();
        var order_time = $("#order_time").val();
        var order_status = $("#order_status").val();

        var queryString = ""

        if (customer_id) {
            queryString += 'customer_id=' + customer_id
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/orders?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">Order_ID</th>'
            header += '<th style="width:40%">Customer_ID</th>'
            header += '<th style="width:40%">Order_Total</th>'
            header += '<th style="width:40%">Order_Time</th>'
            header += '<th style="width:10%">Order_Status</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                order = res[i];
                var row = "<tr><td>"+order.order_id
                    +"</td><td>"+order.customer_id
                    +"</td><td>"+order.order_total
                    +"</td><td>"+orer.order_time
                    +"</td><td>"+orer.order_status
                    +"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
