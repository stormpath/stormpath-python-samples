$(document).ready(function () {
    $('.close').tooltip();
    $('.admin, .premium, .basic').popover({trigger: 'hover', placement: 'top'});
    $('#accountTypeModalContent').modal();
    $('#accountTypeModalContent').modal('hide');
    $('#showAccountTypes').on('click', function () {
        $('#accountTypeModalContent').modal('show');
    });
});
