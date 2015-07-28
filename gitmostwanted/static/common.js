$(function () {
  $('form.repository-filter')
    .find('select, input').on('change', function () {
      $(this).closest('form').submit();
    })
    .end()
    .find('a.button').on('click', function () {
      $(this).closest('form')
        .find('select').val('All').end()
        .find('input:checkbox, input:radio').prop('checked', false).end()
        .submit();
      return false;
    })
    .end()
    .prev().on('click', function () {
      var $elem = $(this);
      $(this).next().slideToggle('fast', function () {
        if ($(this).is(':visible')) {
          $elem.removeClass('secondary').addClass('info');
          return;
        }
        $elem.removeClass('info').addClass('secondary');
      });
      return false;
    });

  $('a.attitude').on('click', function () {
    $.get($(this).attr('href'), function () {
      window.location.reload();
    });
    return false;
  });
});
