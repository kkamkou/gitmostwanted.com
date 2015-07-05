$(function () {
  $('form.filterGhEntries')
    .find('select').on('change', function () {
      $(this).closest('form').submit();
    })
    .end()
    .find('a.button').on('click', function () {
      $(this).closest('form').find('select').val('All').trigger('change');
      return false;
    });
});
