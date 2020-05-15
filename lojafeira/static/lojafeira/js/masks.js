$(document).ready(function() {
    $('.date-mask').mask('00/00/0000');
    $('.date-mask-placeholder').mask('00/00/0000', {placeholder: "__/__/____"});
    $('.phone-mask').mask('(00) 00000-0000');
    $('.cpf-mask').mask('000.000.000-00');
    $('.datepicker').datepicker({
        dateFormat: "dd/mm/yy",
    });
});
