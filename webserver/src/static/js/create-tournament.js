$(function() {

    function displayError(msg) {
        $('div.red ul').append('<li>' + msg + '</li>');
        $('div.red').show();
    };
    
    $(document).ready( function addSubmitListener(){
        $('#btnRegister').click(function() {

            var errors = 0;

            $('div.red ul').empty();
            $('div.green').empty();

            $.ajax({
                url: '/addTournament',
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
