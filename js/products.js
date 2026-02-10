document.addEventListener('DOMContentLoaded', function () {
	var container = document.getElementById('dynamic-products');
	if (!container) return;

	function formatPrice(p) {
		if (typeof p !== 'number') return '' + p;
		return '₹' + p.toString();
	}

	fetch('http://localhost:5000/api/products')
		.then(function (r) { return r.json(); })
		.then(function (items) {
			if (!Array.isArray(items)) return;
			var html = items.map(function (item) {
				return (
					'<div class="col-6 col-md-4 col-lg-3 mb-4">' +
						'<div class="border rounded h-100 p-3 text-center bg-white">' +
							'<div class="mb-2 fw-semibold">' + (item.name || 'Product') + '</div>' +
							'<div class="text-primary">' + formatPrice(item.price) + '</div>' +
							'<button class="btn btn-sm btn-primary mt-3">Add to cart</button>' +
						'</div>' +
					'</div>'
				);
			}).join('');
			container.innerHTML = html || '<div class="text-center text-muted">No products available.</div>';
		})
		.catch(function () {
			container.innerHTML = '<div class="text-center text-muted">Could not load products.</div>';
		});
});

