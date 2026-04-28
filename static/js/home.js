/* ============================================================
   eSociety — Home Page JavaScript
   Companion to: templates/core/home.html
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ── Platform Tab Switcher ────────────────────────────────
    const tabButtons = document.querySelectorAll('[data-tab-btn]');
    const tabPanels  = document.querySelectorAll('[data-tab-panel]');

    function activateTab(targetId) {
        // Update button styles
        tabButtons.forEach(btn => {
            const isActive = btn.dataset.tabBtn === targetId;
            btn.classList.toggle('bg-primary',  isActive);
            btn.classList.toggle('text-white',   isActive);
            btn.classList.toggle('text-on-surface-variant', !isActive);
        });

        // Show / hide panels with a fade
        tabPanels.forEach(panel => {
            if (panel.dataset.tabPanel === targetId) {
                panel.classList.remove('hidden');
                panel.classList.add('animate-fade-in');
            } else {
                panel.classList.add('hidden');
                panel.classList.remove('animate-fade-in');
            }
        });
    }

    // Attach click listeners
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => activateTab(btn.dataset.tabBtn));
    });

    // Activate the first tab by default
    if (tabButtons.length > 0) {
        activateTab(tabButtons[0].dataset.tabBtn);
    }

    // ── Navbar Scroll Shadow ─────────────────────────────────
    const header = document.getElementById('home-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                header.classList.add('shadow-md');
            } else {
                header.classList.remove('shadow-md');
            }
        }, { passive: true });
    }

});
