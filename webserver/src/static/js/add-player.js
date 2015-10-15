$(function() {

    function displayError(msg) {
        $('div.red ul').append('<li>' + msg + '</li>');
        $('div.red').show();
    };
    
    $(document).ready( function addSubmitListener(){
        $('#btnRegister').click(function() {

            var errors = 0;

            $('div.red ul').empty();
            $('div.green ul').empty();

            if ( $.trim($('input#inputPassword').val()) == '' ) {
                displayError("Please enter a password");
                errors++;
            }

            if ( $('input#inputPassword').val() !== $('input#inputConfirmPassword').val() ) {
                displayError("Your passwords don't match");
                errors++;
            }

            if (errors > 0 ) {
                return;
            }

            $.ajax({
                url: '/addPlayer',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    $('div.green').html(response);
                    $('div.green').show();
                },
                error: function(error) {
                    displayError(error['responseText']);
                }
            });
        });

    });

});
