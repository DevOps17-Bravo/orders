$(function () {

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        var customer_id = $(this).parent().find("#create_customer_id").val();
        var order_total = $(this).parent().find("#create_order_total").val();
        var order_time = $(this).parent().find("#create_order_time").val();
        var order_status = $(this).parent().find("#create_order_status").val();

        var data = {
            "order_id": 0,
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
            var result_order_id = res.order_id;
            var result_customer_id = res.customer_id;
            var result_order_total = res.order_total;
            var result_order_time = res.order_time;
            var result_order_status = res.order_status;

            $("#create_customer_id").empty();
            $("#create_order_total").empty();
            $("#create_order_time").empty();
            $("#create_order_status").empty();

            $("#create_result_order_id").append(result_order_id);
            $("#create_result_customer_id").append(result_customer_id);
            $("#create_result_order_total").append(result_order_total);
            $("#create_result_order_time").append(result_order_time);
            $("#create_result_order_status").append(result_order_status);

        });
        ajax.fail(function(res){

            $("#create_result_order_id").empty();
            $("#create_result_customer_id").empty();
            $("#create_result_order_total").empty();
            $("#create_result_order_time").empty();
            $("#create_result_order_status").append("Server Error!");
        });

    });


    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $(this).parent().find("#update_order_id").val();
        var customer_id = $(this).parent().find("#update_customer_id").val();
        var order_total = $(this).parent().find("#update_order_total").val();
        var order_time = $(this).parent().find("#update_order_time").val();
        var order_status = $(this).parent().find("#update_order_status").val();

        var data = {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_total": order_total,
            "order_time": order_time,
            "order_status": order_status
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            var result_order_id = res.order_id;
            var result_customer_id = res.customer_id;
            var result_order_total = res.order_total;
            var result_order_time = res.order_time;
            var result_order_status = res.order_status;

            $("#update_order_id").empty();
            $("#update_customer_id").empty();
            $("#update_order_total").empty();
            $("#update_order_time").empty();
            $("#update_order_status").empty();


            $("#update_result_order_id").append(result_order_id);
            $("#update_result_customer_id").append(result_customer_id);
            $("#update_result_order_total").append(result_order_total);
            $("#update_result_order_time").append(result_order_time);
            $("#update_result_order_status").append(result_order_status);

        });
        ajax.fail(function(res){

            $("#update_result_order_id").empty();
            $("#update_result_customer_id").empty();
            $("#update_result_order_total").empty();
            $("#update_result_order_time").empty();
            $("#update_result_order_status").append("Server Error!");
        });
    });

    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#retrieve_order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })
        ajax.done(function(res){
            var result_order_id = res.order_id;
            var result_customer_id = res.customer_id;
            var result_order_total = res.order_total;
            var result_order_time = res.order_time;
            var result_order_status = res.order_status;

            $("#retrieve_order_id").empty();
            $("#retrieve_customer_id").empty();
            $("#retrieve_order_total").empty();
            $("#retrieve_order_time").empty();
            $("#retrieve_order_status").empty();

            $("#retrieve_result_order_id").append(result_order_id);
            $("#retrieve_result_customer_id").append(result_customer_id);
            $("#retrieve_result_order_total").append(result_order_total);
            $("#retrieve_result_order_time").append(result_order_time);
            $("#retrieve_result_order_status").append(result_order_status);

        });
        ajax.fail(function(res){

            $("#retrieve_result_order_id").empty();
            $("#retrieve_result_customer_id").empty();
            $("#retrieve_result_order_total").empty();
            $("#retrieve_result_order_time").empty();
            $("#retrieve_result_order_status").append("Order ID does not exist!");
        });
    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        var order_id = $("#delete_order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){

            $("#delete_order_id").empty();
            $("#delete_result").append("Deleted!");

        });
        ajax.fail(function(res){

            $("#delete_result").append("server error!");
        });
    });


})
