(function () {
  'use strict';

  function executeScripts(container) {
    var scripts = container.querySelectorAll('script');
    scripts.forEach(function (oldScript) {
      var newScript = document.createElement('script');
      Array.from(oldScript.attributes).forEach(function (attr) {
        newScript.setAttribute(attr.name, attr.value);
      });
      newScript.textContent = oldScript.textContent;
      oldScript.parentNode.replaceChild(newScript, oldScript);
    });
  }

  function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (!modal) {
      return;
    }
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal(modal) {
    if (!modal) {
      return;
    }
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    if (!document.querySelector('.modal-backdrop.open')) {
      document.body.style.overflow = '';
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-theme') || 'dark';
        var next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        try {
          localStorage.setItem('gmw-theme', next);
        } catch (e) {}
        if (typeof window.__gmwRenderActiveChart === 'function') {
          window.__gmwRenderActiveChart();
        }
      });
    }

    window.addEventListener('resize', function () {
      if (typeof window.__gmwRenderActiveChart === 'function') {
        var openDetailsModal = document.querySelector('#repoDetailsModal.open');
        if (openDetailsModal) {
          window.__gmwRenderActiveChart();
        }
      }
    });

    var userDropdown = document.querySelector('.user-dropdown');
    if (userDropdown) {
      var trigger = userDropdown.querySelector('.user-menu-trigger');
      trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        var isOpen = userDropdown.classList.toggle('open');
        trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
      document.addEventListener('click', function () {
        userDropdown.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
      });
    }

    var formFilter = document.querySelector('form.repository-filter');
    if (formFilter) {
      formFilter.querySelectorAll('select, input[type="checkbox"]').forEach(function (input) {
        input.addEventListener('change', function () {
          formFilter.submit();
        });
      });

      var radios = formFilter.querySelectorAll('input[type="radio"]');
      radios.forEach(function (radio) {
        radio.__wasChecked = radio.checked;
        radio.addEventListener('click', function () {
          if (radio.__wasChecked) {
            radio.checked = false;
            radio.__wasChecked = false;
          } else {
            radios.forEach(function (other) {
              other.__wasChecked = (other === radio);
            });
          }
          formFilter.submit();
        });
      });

      var clearSearchBtn = formFilter.querySelector('[data-clear-search]');
      if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function () {
          var termInput = formFilter.querySelector('input[name="term"]');
          if (termInput) {
            termInput.value = '';
            formFilter.submit();
          }
        });
      }

      var resetBtn = formFilter.querySelector('[data-reset-filters]');
      if (resetBtn) {
        resetBtn.addEventListener('click', function () {
          var langSelect = formFilter.querySelector('select[name="lang"]');
          if (langSelect) {
            langSelect.value = 'All';
          }
          formFilter.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(function (el) {
            el.checked = false;
          });
          formFilter.submit();
        });
      }

      var filterToggleBtns = document.querySelectorAll('.filter-toggle-btn[data-section]');
      filterToggleBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          var section = formFilter.querySelector('.' + btn.getAttribute('data-section'));
          if (section) {
            var hidden = section.classList.toggle('hide');
            btn.classList.toggle('active', !hidden);
            btn.setAttribute('aria-expanded', !hidden ? 'true' : 'false');
          }
        });
      });
    }

    document.querySelectorAll('a.attitude').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        if (!link.classList.contains('secondary')) {
          return;
        }
        fetch(link.getAttribute('href'), { credentials: 'same-origin' })
          .then(function (res) {
            if (!res.ok) {
              return;
            }
            var parent = link.parentElement;
            parent.querySelectorAll('a.attitude').forEach(function (sib) {
              sib.classList.remove('active-like', 'active-neutral', 'active-dislike');
              sib.classList.add('secondary');
            });
            link.classList.remove('secondary');
            link.classList.add(link.getAttribute('data-active-class'));
          });
      });
    });

    document.querySelectorAll('[data-modal-open]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        openModal(btn.getAttribute('data-modal-open'));
      });
    });

    document.querySelectorAll('[data-ajax-modal]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var modalId = link.getAttribute('data-ajax-modal');
        var modal = document.getElementById(modalId);
        var content = document.getElementById(modalId + 'Content') || modal;
        if (!modal || !content) {
          return;
        }
        content.innerHTML =
          '<div class="modal-header">' +
          '<h3 class="modal-title">Repository Analytics</h3>' +
          '<button type="button" class="modal-close" data-modal-close aria-label="Close">&times;</button>' +
          '</div>' +
          '<div class="modal-body modal-loading">' +
          '<span class="loading-spinner" aria-hidden="true"></span>' +
          '<span>Loading repository details&hellip;</span>' +
          '</div>';
        openModal(modalId);
        fetch(link.getAttribute('href'), { credentials: 'same-origin' })
          .then(function (res) {
            if (!res.ok) {
              throw new Error('Failed to load');
            }
            return res.text();
          })
          .then(function (html) {
            content.innerHTML = html;
            executeScripts(content);
          })
          .catch(function () {
            content.innerHTML =
              '<div class="modal-header">' +
              '<h3 class="modal-title">Repository Analytics</h3>' +
              '<button type="button" class="modal-close" data-modal-close aria-label="Close">&times;</button>' +
              '</div>' +
              '<div class="modal-body">' +
              '<div class="empty-state">' +
              '<p>Could not load repository details.</p>' +
              '<span class="empty-state-sub">Please check your connection and try again.</span>' +
              '</div>' +
              '</div>';
          });
      });
    });

    document.addEventListener('click', function (e) {
      var closeBtn = e.target.closest('[data-modal-close]');
      if (closeBtn) {
        closeModal(closeBtn.closest('.modal-backdrop'));
        return;
      }
      if (e.target.classList && e.target.classList.contains('modal-backdrop')) {
        closeModal(e.target);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-backdrop.open').forEach(closeModal);
        if (userDropdown) {
          userDropdown.classList.remove('open');
        }
        if (document.activeElement && document.activeElement.classList.contains('search-input')) {
          document.activeElement.blur();
        }
        return;
      }

      if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes((document.activeElement || {}).tagName)) {
        var searchInput = document.querySelector('.search-input');
        if (searchInput) {
          e.preventDefault();
          searchInput.focus();
          searchInput.select();
        }
      }
    });
  });
})();
