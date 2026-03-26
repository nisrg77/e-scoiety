/**
 * eSociety Management System — Global JavaScript
 * -----------------------------------------------
 * Loaded on every page via base.html.
 * Page-specific logic goes in {% block extra_js %} of each template.
 */

'use strict';

/* =========================================================
   1.  AUTO-DISMISS FLASH MESSAGES
   ========================================================= */
(function () {
    const DISMISS_DELAY = 4500; // ms

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (el) {
            setTimeout(function () {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                if (bsAlert) bsAlert.close();
            }, DISMISS_DELAY);
        });
    });
})();

/* =========================================================
   2.  ACTIVE NAV HIGHLIGHT
       Adds "active" to the sidebar link whose href matches
       the current URL so you never have to hard-code it.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const current = window.location.pathname;
        document.querySelectorAll('.sidebar-nav .nav-link').forEach(function (link) {
            if (link.getAttribute('href') === current) {
                link.classList.add('active');
            }
        });
    });
})();

/* =========================================================
   3.  RADIO OPTION TILES
       Highlights the parent .option-tile when its hidden
       radio input is selected.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.option-tile input[type="radio"]').forEach(function (radio) {
            // Apply initial state (e.g. after validation error repopulates form)
            if (radio.checked) radio.closest('.option-tile').classList.add('selected');

            radio.addEventListener('change', function () {
                // Deselect siblings in the same group
                const name = radio.getAttribute('name');
                document.querySelectorAll(`.option-tile input[name="${name}"]`).forEach(function (r) {
                    r.closest('.option-tile').classList.remove('selected');
                });
                if (this.checked) this.closest('.option-tile').classList.add('selected');
            });

            // Allow clicking the tile div itself (not just the hidden input)
            radio.closest('.option-tile').addEventListener('click', function () {
                radio.checked = true;
                radio.dispatchEvent(new Event('change', { bubbles: true }));
            });
        });
    });
})();

/* =========================================================
   4.  VEHICLE TYPE TOGGLE
       On the add_vehicle page: show/hide the "Parking Slot"
       field only when vehicle type is "Car".
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const vehicleTypeSelect = document.getElementById('id_vehicle_type');
        const parkingSlotRow    = document.getElementById('parking-slot-row');

        if (!vehicleTypeSelect || !parkingSlotRow) return;

        function toggleParkingSlot () {
            parkingSlotRow.style.display =
                vehicleTypeSelect.value === 'car' ? '' : 'none';
        }

        vehicleTypeSelect.addEventListener('change', toggleParkingSlot);
        toggleParkingSlot(); // run on page load
    });
})();

/* =========================================================
   5.  CONFIRM BEFORE DANGEROUS ACTIONS
       Add data-confirm="Are you sure?" to any button/link
       to get a native confirm dialog before it fires.
   ========================================================= */
(function () {
    document.addEventListener('click', function (e) {
        const el = e.target.closest('[data-confirm]');
        if (!el) return;
        const msg = el.dataset.confirm || 'Are you sure?';
        if (!window.confirm(msg)) e.preventDefault();
    });
})();

/* =========================================================
   6.  TABLE ROW CLICK → NAVIGATE
       Add data-href="/some/url/" to <tr> to make the whole
       row clickable.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('tr[data-href]').forEach(function (row) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function () {
                window.location.href = this.dataset.href;
            });
        });
    });
})();

/* =========================================================
   7.  LIVE CHARACTER COUNTER
       Add data-maxlength="200" to a textarea/input and a
       <span data-counter-for="inputId"> next to it.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-maxlength]').forEach(function (el) {
            const max     = parseInt(el.dataset.maxlength, 10);
            const counter = document.querySelector(`[data-counter-for="${el.id}"]`);
            if (!counter) return;

            function update () {
                const remaining = max - el.value.length;
                counter.textContent = `${remaining} / ${max}`;
                counter.style.color = remaining < 20 ? '#EF4444' : '#6B7280';
            }

            el.addEventListener('input', update);
            update();
        });
    });
})();

/* =========================================================
   8.  DATE INPUT — Prevent past dates on booking forms
       Add data-min-today to any date input.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('input[type="date"][data-min-today]').forEach(function (el) {
            const today = new Date().toISOString().split('T')[0];
            el.setAttribute('min', today);
        });
    });
})();

/* =========================================================
   9.  SEARCH FILTER — Client-side table row filter
       Add data-filter-table="tableId" to a text input and
       data-filter-col="colIndex" to specify which column to search.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-filter-table]').forEach(function (input) {
            const tableId  = input.dataset.filterTable;
            const colIndex = parseInt(input.dataset.filterCol ?? '0', 10);
            const table    = document.getElementById(tableId);
            if (!table) return;

            input.addEventListener('input', function () {
                const query = this.value.trim().toLowerCase();
                table.querySelectorAll('tbody tr').forEach(function (row) {
                    const cell = row.cells[colIndex];
                    const text = cell ? cell.textContent.toLowerCase() : '';
                    row.style.display = text.includes(query) ? '' : 'none';
                });
            });
        });
    });
})();

/* =========================================================
   10.  STATS COUNTER ANIMATION
        Any element with class .stat-number will count up
        from 0 to its text content on page load.
   ========================================================= */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.stat-number').forEach(function (el) {
            const target = parseInt(el.textContent.replace(/[^0-9]/g, ''), 10);
            if (isNaN(target) || target === 0) return;

            let start = 0;
            const duration = 900; // ms
            const step = (timestamp, startTime) => {
                const elapsed  = timestamp - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease-out quad
                el.textContent = Math.floor(progress * target);
                if (progress < 1) requestAnimationFrame(ts => step(ts, startTime));
                else el.textContent = target;
            };
            requestAnimationFrame(ts => step(ts, ts));
        });
    });
})();

/* =========================================================
   11.  GLASS-CARD ENTRANCE ANIMATION on scroll
        Applies .visible when a .glass-card enters viewport.
   ========================================================= */
(function () {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity  = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.glass-card, .stat-card').forEach(function (card) {
            // Only animate cards that are off-screen at load time
            const rect = card.getBoundingClientRect();
            if (rect.top > window.innerHeight) {
                card.style.opacity   = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                observer.observe(card);
            }
        });
    });
})();

/* =========================================================
   12.  TOASTER UTILITY  (call window.esSocToast("msg", "success"))
        Shows a Bootstrap toast without needing explicit HTML.
   ========================================================= */
(function () {
    window.esSocToast = function (message, type) {
        type = type || 'info';
        const colors = {
            success : '#10B981',
            danger  : '#EF4444',
            warning : '#F59E0B',
            info    : '#4F46E5'
        };

        const toastEl = document.createElement('div');
        toastEl.style.cssText = `
            position:fixed; bottom:20px; right:20px; z-index:9999;
            background:${colors[type] || colors.info}; color:#fff;
            padding:14px 20px; border-radius:12px; font-size:14px;
            font-weight:500; font-family:'Inter',sans-serif;
            box-shadow:0 8px 24px rgba(0,0,0,0.15);
            display:flex; align-items:center; gap:10px;
            transform:translateY(40px); opacity:0;
            transition:all 0.3s cubic-bezier(0.4,0,0.2,1);
        `;
        toastEl.textContent = message;
        document.body.appendChild(toastEl);

        // Slide in
        requestAnimationFrame(() => {
            toastEl.style.transform = 'translateY(0)';
            toastEl.style.opacity   = '1';
        });

        // Auto-remove
        setTimeout(() => {
            toastEl.style.transform = 'translateY(40px)';
            toastEl.style.opacity   = '0';
            setTimeout(() => toastEl.remove(), 350);
        }, 3500);
    };
})();
