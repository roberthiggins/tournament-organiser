$(function() {
    
    $(document).ready( function addSubmitListener(){
        $('#btnRegister').click(function() {
            $.ajax({
                url: '/addPlayer',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });

    });

});
