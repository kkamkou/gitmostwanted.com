$(function () {
  $('form.repository-filter')
    .find('select, input').on('change', function () {
      $(this).closest('form').submit();
    })
    .end()
    .find('a.button').on('click', function () {
      $(this).closest('form').find('select').val('All').trigger('change');
      return false;
    });

  $('a.attitude').on('click', function () {
    $.get($(this).attr('href'), function () {
      window.location.reload();
    });
    return false;
  });
});
