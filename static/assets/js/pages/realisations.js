document.addEventListener('DOMContentLoaded', function() {
    const clientCard = document.getElementById('client-card');
    const popupClose = document.getElementById('popup-close');

    function toggleBodyScroll(shouldDisable) {
      if (shouldDisable) {
        document.body.classList.add('no-scroll');
      } else {
        document.body.classList.remove('no-scroll');
      }
    }

    if (clientCard) {
      clientCard.addEventListener('click', function() {
        toggleBodyScroll(true);
      });
    }

    if (popupClose) {
      popupClose.addEventListener('click', function() {
        toggleBodyScroll(false);
      });
    }

    const cmsItems = document.querySelectorAll('.client-item');
    const popupCmsList = document.getElementById('popup-cms-list');
    if (popupCmsList) {
      popupCmsList.style.display = 'block';
    }

    function loadItemIntoPopup(itemName) {
      const popupCmsItems = document.querySelectorAll('.popup-item');
      popupCmsItems.forEach(item => {
        if (item.getAttribute('data-item-name') === itemName) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    }

    cmsItems.forEach(item => {
      item.addEventListener('click', function() {
        const itemName = this.getAttribute('data-item-name');
        loadItemIntoPopup(itemName);
      });
    });

    const clearAllDiv = document.getElementById('clear-all');
    const filterList = document.getElementById('filter-list');

    if (clearAllDiv && filterList) {
      filterList.insertBefore(clearAllDiv, filterList.firstChild);
    }

    document.addEventListener('click', function(event) {
      const clearAll = document.getElementById('clear-all');

      function findAncestorWithAttribute(element, attributeName) {
        while (element && !element.hasAttribute(attributeName)) {
          element = element.parentElement;
        }
        return element;
      }

      const tagCheckbox = findAncestorWithAttribute(event.target, 'data-tag-checkbox');
      if (tagCheckbox) {
        clearAll.classList.remove('is-active');
      } else if (event.target.id === 'clear-all' || event.target.closest('#clear-all')) {
        clearAll.classList.add('is-active');
      }
    });
  });
