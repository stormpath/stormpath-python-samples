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
                    html = "<div class='well well-small'> \
                            <code><a href='#''>" + chirp.name + "</a>: " +
                                chirp.message + "</code>";

                    if (chirp.admin) {
                        html = html + "<button class='close'" +
                        "title='Delete the chirp permanently'>" +
                        "<a href='" + chirp.id + "' >&times;</a></button>";
                    }

                    html = html + "</div>";
                    $(".chirps").append(html);
                });
            } else {
                html = "<div class='alert'>There are no chirps!</div>";
                $(".chirps").append(html);
            }
        }
    });
}
