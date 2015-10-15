$(function() {

    function displayError(msg) {
        $('div.errors ul').append('<li>' + msg + '</li>');
        $('div.errors').show();
    };
    
    $(document).ready( function addSubmitListener(){
        $('#btnRegister').click(function() {

            var errors = 0;

            $('div.errors ul').empty();

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
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });

    });

});
