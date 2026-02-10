document.addEventListener('DOMContentLoaded', function () {
	// Mobile dropdown accessibility improvements
	var dropdownToggles = document.querySelectorAll('.navbar .dropdown > a, .navbar .nav-link.dropdown-toggle');
	dropdownToggles.forEach(function (toggle) {
		toggle.addEventListener('click', function (e) {
			var width = window.innerWidth || document.documentElement.clientWidth;
			if (width < 992) {
				e.preventDefault();
				var menu = this.nextElementSibling;
				if (menu && menu.classList.contains('dropdown-menu')) {
					menu.classList.toggle('show');
				}
			}
		});
	});

	// Sticky header toggle on scroll for small screens
	var navBar = document.querySelector('.nav-bar');
	var lastKnownScrollY = 0;
	var ticking = false;
	function onScroll() {
		lastKnownScrollY = window.scrollY || window.pageYOffset;
		if (!ticking) {
			window.requestAnimationFrame(function () {
				if (!navBar) return;
				if (lastKnownScrollY > 60) {
					navBar.classList.add('is-scrolled');
				} else {
					navBar.classList.remove('is-scrolled');
				}
				ticking = false;
			});
			ticking = true;
		}
	}
	window.addEventListener('scroll', onScroll, { passive: true });

	// Expand/collapse All Categories button on small screens for better UX
	var allCatToggler = document.querySelector('[data-bs-target="#allCat"]');
	if (allCatToggler) {
		allCatToggler.addEventListener('click', function () {
			var width = window.innerWidth || document.documentElement.clientWidth;
			if (width < 992) {
				// allow default Bootstrap collapse behavior; nothing custom needed
			}
		});
	}
});

