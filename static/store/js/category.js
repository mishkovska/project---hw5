document.addEventListener('DOMContentLoaded', function() {
    var priceRange = document.getElementById('priceRange');
    var rangeValues = document.getElementById('rangeValues');
  
    priceRange.oninput = function() {
      rangeValues.innerHTML = this.value;
    }
});