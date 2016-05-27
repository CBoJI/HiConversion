// Script to process invitations by ajax.

(function () {

    $('#js_invitation_form').submit( function (e) {
        e.preventDefault();
        $.post( "/admin/", $(this).serializeArray(), function( data ){
        })
        .done(function(data) {
            if (data.status == 'ok'){
                alert( "Invite sent." );
            } else {
                alert( "Error! \n " + JSON.stringify(data, null, 4) );
            }
        })
        .fail(function() {
            alert( "Network error. Please, try later." );
        });
    });

})();
