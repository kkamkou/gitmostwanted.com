$(function () {
  'use strict';

  var $form = $('form.repository-filter');

  $form
    .find('select, input').on('change', function () {
      $form.slideUp('fast', function () {
        $form.submit();
      })
    })
    .end()
    .find('label').on('click', function () {
      var $prev = $(this).prev();
      if ($prev.prop('checked')) {
        $prev.prop('checked', false).trigger('change');
        return false;
      }
    })
    .end()
    .find('a.button').on('click', function () {
      $form
        .find('select').val('All').end()
        .find('input:checkbox, input:radio').prop('checked', false).trigger('change');
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
