$(function () {
  'use strict';

  var $formFilter = $('form.repository-filter'),
    $formFilterBtn = $('a.repository-filter');

  $formFilter
    .find('select, input').change(function () {
      $formFilter.hide(0, function () {
        $formFilter.submit();
      })
    })
    .end()
    .find('label').click(function () {
      var $prev = $(this).prev();
      if ($prev.prop('checked')) {
        $prev.prop('checked', false).trigger('change');
        return false;
      }
    })
    .end()
    .find('a.button').click(function () {
      $formFilter
        .find('select').val('All').end()
        .find('input:checkbox, input:radio').prop('checked', false).trigger('change');
      return false;
    });

  $formFilterBtn.click(function () {
    var $elem = $(this);
    $formFilter.find('div.' + $elem.data('section')).toggle(0, function () {
      if ($(this).is(':visible')) {
        $elem.removeClass('secondary').addClass('info');
        return;
      }
      $elem.removeClass('info').addClass('secondary');
    });
    $formFilter.find('input[autofocus]:visible').focus();
    return false;
  });

  $('a.attitude').click(function () {
    if (!$(this).hasClass('secondary')) {
      return false;
    }
    $.get($(this).attr('href'), function () {
      window.location.reload();
    });
    return false;
  });
});
