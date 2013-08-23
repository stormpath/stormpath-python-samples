$(document).ready(function () {
    $('.close').tooltip();
    $('.admin, .premium, .basic').popover({trigger: 'hover', placement: 'top'});
    $('#accountTypeModalContent').modal();
    $('#accountTypeModalContent').modal('hide');
    $('#showAccountTypes').on('click', function () {
        $('#accountTypeModalContent').modal('show');
    });
    updateChirps();
});

function updateChirps() {
    $.ajax({
        url: chirps_url,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response.length !== 0) {
                response.forEach(function (chirp) {
                    $(".chirps").append(chirp.message);
                });
            } else {
                html = "<div class='alert'>There are no chirps!</div>";
                $(".chirps").append(html);
            }
        }
    });
}
