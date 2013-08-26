$(document).ready(function () {
    $('.close').tooltip();
    $('.admin, .premium, .basic').popover({trigger: 'hover', placement: 'top'});
    $('#accountTypeModalContent').modal();
    $('#accountTypeModalContent').modal('hide');
    $('#showAccountTypes').on('click', function () {
        $('#accountTypeModalContent').modal('show');
    });
    updateChirps();
    setInterval(updateChirps, 60000);
});

function updateChirps() {
    $(".chirps").fadeOut(function() {
        $(".chirps").empty();
        $.ajax({
            url: chirps_url,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                $(".chirps").append(response[0].chirps);
            }
        });
    });
    $(".chirps").fadeIn();
}
