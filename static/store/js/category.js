document.addEventListener('DOMContentLoaded', function() {
  var checkboxes = document.querySelectorAll('.form-check-input');
  var priceRange = document.getElementById('priceRange');
  var rangeValues = document.getElementById('rangeValues');
  var productCards = document.querySelectorAll('.product-card');
  
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateProducts);
  });

  let priceTimeout;

  priceRange.addEventListener('input', function() {
    rangeValues.innerHTML = this.value;
  
    clearTimeout(priceTimeout);
    priceTimeout = setTimeout(updateProducts, 300);
  });

  priceRange.addEventListener('change', () => {
    clearTimeout(priceTimeout);
    updateProducts();
  });

  function updateProducts() {
    var selectedSpecs = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedPrice = parseFloat(priceRange.value)

    productCards.forEach(product => {
      var productSpecs = product.getAttribute('data-specs').split(',');
      var productPrice = product.getAttribute('data-price');

      var specsMatch = selectedSpecs.length === 0 || productSpecs.every(spec => selectedSpecs.includes(spec));
      var priceMatch = isNaN(selectedPrice) || productPrice <= selectedPrice;

      product.style.display = specsMatch && priceMatch ? 'block' : 'none';
    });
  }
});