<!DOCTYPE html>

<html class="scroll-smooth" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>eSociety | The Luminous Ledger for Modern Living</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=Inter:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    /* === eSociety Project Design Tokens (synced with base.html) === */
                    "primary":                  "#403ecc",
                    "primary-container":        "#5a5ae6",
                    "on-primary":               "#ffffff",
                    "on-primary-container":     "#f1eeff",
                    "primary-fixed":            "#e1dfff",
                    "primary-fixed-dim":        "#c1c1ff",
                    "inverse-primary":          "#c1c1ff",

                    "secondary":                "#3a5ca6",
                    "secondary-container":      "#8fafff",
                    "on-secondary":             "#ffffff",
                    "on-secondary-container":   "#194089",
                    "secondary-fixed":          "#d9e2ff",
                    "secondary-fixed-dim":      "#b0c6ff",

                    "tertiary":                 "#764c00",
                    "tertiary-container":       "#966200",
                    "on-tertiary":              "#ffffff",
                    "on-tertiary-container":    "#ffedda",
                    "tertiary-fixed":           "#ffddb4",
                    "tertiary-fixed-dim":       "#ffb955",

                    "surface":                  "#f8f9fd",
                    "surface-bright":           "#f8f9fd",
                    "surface-container-lowest": "#ffffff",
                    "surface-container-low":    "#f2f3f7",
                    "surface-container":        "#edeef2",
                    "surface-container-high":   "#e7e8ec",
                    "surface-container-highest":"#e1e2e6",
                    "surface-dim":              "#d9dade",
                    "surface-variant":          "#e1e2e6",
                    "surface-tint":             "#4b4ad7",
                    "inverse-surface":          "#2e3134",
                    "inverse-on-surface":       "#eff1f5",

                    "on-surface":               "#191c1f",
                    "on-surface-variant":       "#464554",
                    "on-background":            "#191c1f",
                    "background":               "#f8f9fd",

                    "outline":                  "#777586",
                    "outline-variant":          "#c7c4d7",

                    "error":                    "#ba1a1a",
                    "error-container":          "#ffdad6",
                    "on-error":                 "#ffffff",
                    "on-error-container":       "#93000a"
            },
            "borderRadius": {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            },
            "spacing": {
                    "margin-mobile": "20px",
                    "unit": "8px",
                    "stack-gap": "16px",
                    "container-max": "1280px",
                    "section-gap": "120px",
                    "gutter": "24px"
            },
            "fontFamily": {
                    "h3": ["Plus Jakarta Sans"],
                    "button": ["Plus Jakarta Sans"],
                    "body-md": ["Plus Jakarta Sans"],
                    "h2": ["Plus Jakarta Sans"],
                    "h1": ["Plus Jakarta Sans"],
                    "label-bold": ["Plus Jakarta Sans"],
                    "body-lg": ["Plus Jakarta Sans"]
            },
            "fontSize": {
                    "h3": ["32px", {"lineHeight": "1.3", "fontWeight": "700"}],
                    "button": ["16px", {"lineHeight": "1", "fontWeight": "600"}],
                    "body-md": ["16px", {"lineHeight": "1.6", "fontWeight": "400"}],
                    "h2": ["48px", {"lineHeight": "1.2", "letterSpacing": "-0.01em", "fontWeight": "700"}],
                    "h1": ["64px", {"lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "800"}],
                    "label-bold": ["14px", {"lineHeight": "1.2", "letterSpacing": "0.05em", "fontWeight": "600"}],
                    "body-lg": ["18px", {"lineHeight": "1.6", "fontWeight": "400"}]
            }
          },
        },
      }
    </script>
<style>
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0px 10px 30px rgba(90, 90, 230, 0.05);
        }
        .hero-gradient {
            background: radial-gradient(circle at top right, rgba(90, 90, 230, 0.1), transparent 40%),
                        radial-gradient(circle at bottom left, rgba(64, 62, 204, 0.05), transparent 40%);
        }
        .button-glow:hover {
            box-shadow: 0 0 20px rgba(90, 90, 230, 0.4);
        }
        .squircle {
            border-radius: 24px;
        }
    </style>
</head>
<body class="bg-background text-on-background font-body-md overflow-x-hidden hero-gradient">
<!-- TopNavBar -->
<header class="sticky top-0 w-full z-50 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl no-border shadow-[0_12px_40px_rgba(25,28,31,0.04)]">
<nav class="flex justify-between items-center px-8 py-4 max-w-7xl mx-auto">
<div class="text-2xl font-bold tracking-tighter text-[#191C1F] dark:text-white font-h2">
                eSociety
            </div>
<div class="hidden md:flex items-center gap-8 font-['Plus_Jakarta_Sans'] font-semibold text-sm tracking-tight">
<a class="text-[#5A5AE6] dark:text-[#8FAFFF] font-bold transition-all duration-300" href="#">Features</a>
<a class="text-[#191C1F] dark:text-slate-400 hover:text-[#5A5AE6] transition-all duration-300" href="#">Pricing</a>
<a class="text-[#191C1F] dark:text-slate-400 hover:text-[#5A5AE6] transition-all duration-300" href="#">About</a>
</div>
<div class="flex items-center gap-4 font-button">
<button class="px-6 py-2 text-[#191C1F] dark:text-slate-400 hover:text-[#5A5AE6] transition-all duration-300 active:scale-95">Login</button>
<button class="px-6 py-3 bg-primary-container text-on-primary-container rounded-full button-glow transition-all duration-300 active:scale-95 shadow-lg">Get Started</button>
</div>
</nav>
</header>
<main>
<!-- Hero Section -->
<section class="max-w-7xl mx-auto px-8 pt-20 pb-32 grid md:grid-cols-2 gap-16 items-center">
<div class="flex flex-col gap-8">
<div class="inline-flex items-center gap-2 px-4 py-1 bg-primary/10 text-primary rounded-full w-fit">
<span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
<span class="text-label-bold font-label-bold uppercase">v2.0 is now live</span>
</div>
<h1 class="text-h1 font-h1 text-on-background">
                    Elevate Your <br/>
<span class="text-primary-container">Community Living</span>
</h1>
<p class="text-body-lg font-body-lg text-on-surface-variant max-w-lg">
                    Experience seamless communication, robust security, and absolute financial transparency. The ultimate OS for modern residential societies.
                </p>
<div class="flex flex-wrap gap-4 mt-4">
<button class="px-8 py-4 bg-primary text-white rounded-xl font-button button-glow transition-all flex items-center gap-2">
                        Get Started <span class="material-symbols-outlined">arrow_forward</span>
</button>
<button class="px-8 py-4 glass-card rounded-xl font-button text-primary hover:bg-white transition-all">
                        View Demo
                    </button>
</div>
</div>
<div class="relative">
<div class="absolute -inset-4 bg-primary/20 blur-3xl rounded-full opacity-30"></div>
<img alt="eSociety Dashboard Preview" class="relative w-full h-auto squircle shadow-2xl glass-card object-cover" data-alt="Modern sleek dashboard interface with colorful charts, clean typography, and translucent panels showcasing residential analytics and community growth" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAA64VGKa449sEcJmymsstPvtZUsCwuSrGMroz67Rc-3sk14Nhy1-ecJXC10ZwcUnUAt0Kr57kY-ujMGgeJExjEB-Y0X4uQGhpf7XMWKlHUWqx_Mn0KyUKdZMTEMhpEYChB6bhik3iJp80nTKYsPDw1QAxNXB5DYjxXAR54B0nC9eVPPP60zu5FOfXvG6uVbaww2oM06bS3dy6LtMtGs_7TTf_bXmAN72xw6qgKVmASSsHfpOEJPdCxfYeKGVDb7YqjAhFqA0V8bdlO"/>
</div>
</section>
<!-- Social Proof -->
<section class="bg-surface-container-low py-16">
<div class="max-w-7xl mx-auto px-8">
<p class="text-center text-label-bold font-label-bold text-outline mb-12 uppercase">Trusted by 500+ Premium Societies</p>
<div class="flex flex-wrap justify-center items-center gap-16 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
<span class="text-2xl font-bold font-h2">MARATHON</span>
<span class="text-2xl font-bold font-h2">LODHA</span>
<span class="text-2xl font-bold font-h2">OBEROI</span>
<span class="text-2xl font-bold font-h2">GODREJ</span>
<span class="text-2xl font-bold font-h2">TATA</span>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 text-center">
<div>
<div class="text-h2 font-h2 text-primary">500+</div>
<div class="text-body-md font-body-md text-on-surface-variant">Societies</div>
</div>
<div>
<div class="text-h2 font-h2 text-primary">100k+</div>
<div class="text-body-md font-body-md text-on-surface-variant">Residents</div>
</div>
<div>
<div class="text-h2 font-h2 text-primary">4.9/5</div>
<div class="text-body-md font-body-md text-on-surface-variant">App Rating</div>
</div>
<div>
<div class="text-h2 font-h2 text-primary">24/7</div>
<div class="text-body-md font-body-md text-on-surface-variant">Support</div>
</div>
</div>
</div>
</section>
<!-- Key Features Grid -->
<section class="max-w-7xl mx-auto px-8 py-section-gap">
<div class="text-center max-w-2xl mx-auto mb-20">
<h2 class="text-h2 font-h2 mb-4">Everything you need to manage your society</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Powerful features designed to automate workflows and enhance resident satisfaction.</p>
</div>
<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
<!-- Card 1 -->
<div class="glass-card p-8 squircle group hover:scale-[1.02] transition-all">
<div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-3xl">account_balance_wallet</span>
</div>
<h3 class="text-h3 font-h3 text-xl mb-3">Financial Transparency</h3>
<p class="text-on-surface-variant text-body-md">Real-time accounting, automated maintenance billing, and transparent ledger access for all.</p>
</div>
<!-- Card 2 -->
<div class="glass-card p-8 squircle group hover:scale-[1.02] transition-all">
<div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-3xl">shield</span>
</div>
<h3 class="text-h3 font-h3 text-xl mb-3">Smart Security</h3>
<p class="text-on-surface-variant text-body-md">Visitor management, staff attendance, and emergency SOS alerts at your fingertips.</p>
</div>
<!-- Card 3 -->
<div class="glass-card p-8 squircle group hover:scale-[1.02] transition-all">
<div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-3xl">event_available</span>
</div>
<h3 class="text-h3 font-h3 text-xl mb-3">Facility Booking</h3>
<p class="text-on-surface-variant text-body-md">Seamlessly book clubhouses, gyms, and sports courts with integrated conflict resolution.</p>
</div>
<!-- Card 4 -->
<div class="glass-card p-8 squircle group hover:scale-[1.02] transition-all">
<div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined text-3xl">chat_bubble</span>
</div>
<h3 class="text-h3 font-h3 text-xl mb-3">Resident Chat</h3>
<p class="text-on-surface-variant text-body-md">Official notice boards and community discussion groups for better local networking.</p>
</div>
</div>
</section>
<!-- Platform Overview (Bento Style) -->
<section class="bg-surface-container py-section-gap">
<div class="max-w-7xl mx-auto px-8">
<div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
<div class="max-w-xl">
<h2 class="text-h2 font-h2 mb-4">Unified experience for everyone</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Three specialized interfaces connected to one powerful core system.</p>
</div>
<div class="flex gap-2 p-1 bg-white rounded-full">
<button class="px-6 py-2 bg-primary text-white rounded-full font-button text-sm">Admin</button>
<button class="px-6 py-2 text-on-surface-variant rounded-full font-button text-sm">Resident</button>
<button class="px-6 py-2 text-on-surface-variant rounded-full font-button text-sm">Security</button>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-12 gap-8">
<div class="md:col-span-8 glass-card p-10 squircle overflow-hidden flex flex-col justify-between">
<div>
<h4 class="text-h3 font-h3 mb-4">Admin Command Center</h4>
<p class="text-body-md text-on-surface-variant mb-8 max-w-md">Complete control over society finances, vendor management, and official communications from a single high-performance dashboard.</p>
</div>
<img alt="Admin Dashboard" class="rounded-xl shadow-xl border border-white/40" data-alt="Close up of a financial dashboard on a laptop with vibrant blue and purple graphs, clean user interface design on a white desk" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCwf-biCP19ii_4pq9JjkjgUEX0ejXplcS9EePO6OMHEDS2-Yr_B6gvnAIETmrR3v-jyl7SFRa-RfMTa2Rk5WNuHRkV2gXYmZ74JsIp5HwIvRR1AdFOpxBks9Z8lPg7ACn6HPUHXyfjcbwnGCV_17JJuxao38FkNb2AmdArHPfVkwVSm_o1HxmIsP5E6JVxUdSwg6WvfobEKcd_6bgpHEDT6tHp79NVcis1KFlRVMf2bSh45OPQHrs8Zo957DiFXO5eIsxjC2hCwyKN"/>
</div>
<div class="md:col-span-4 flex flex-col gap-8">
<div class="glass-card p-8 squircle h-full">
<h4 class="text-xl font-bold font-h3 mb-2">Resident App</h4>
<p class="text-sm text-on-surface-variant mb-6">Pay maintenance, invite guests, and raise complaints on the go.</p>
<img alt="Resident App" class="rounded-lg shadow-md mx-auto h-48 object-cover w-full" data-alt="A smartphone held by a person showing a modern mobile app with property management features and clean colorful icons" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDj1fzuV0Q6ffeLWZ9key_eB0aDiasmwtrsoM8VPZQAQ1upKZk2JFoarRzuQoDifOUvQHw82iewEp5h7V5lO0mLYRZ6UzYtRrrKgKKWfYwTQvoB1BT5JwOm3U_RnCho7iafmaILYlAIGXA0MF3T-I4mbcqWZ-7Ua3QlJiiVU4R6uk72tWbwqoS4WsR9dElLzlsgVb_WiHeYBXEryJ2VY8ospKLWLGbEenDOd4C-LEgGfcp0QUlhIvP9XJ9olAnGCzOzOrOQ6LClfN1B"/>
</div>
<div class="glass-card p-8 squircle h-full">
<h4 class="text-xl font-bold font-h3 mb-2">Security Hub</h4>
<p class="text-sm text-on-surface-variant mb-6">Simple, tablet-first interface for gatekeepers and staff.</p>
<div class="bg-primary/5 p-4 rounded-xl flex items-center justify-center">
<span class="material-symbols-outlined text-6xl text-primary/30">tablet_mac</span>
</div>
</div>
</div>
</div>
</div>
</section>
<!-- Pricing Section -->
<section class="max-w-7xl mx-auto px-8 py-section-gap">
<div class="text-center max-w-2xl mx-auto mb-20">
<h2 class="text-h2 font-h2 mb-4">Simple, transparent pricing</h2>
<p class="text-body-lg font-body-lg text-on-surface-variant">Choose the plan that best fits your community size and requirements.</p>
</div>
<div class="grid md:grid-cols-3 gap-8">
<!-- Tier 1 -->
<div class="glass-card p-10 squircle border-transparent hover:border-primary/20 transition-all">
<div class="text-label-bold font-label-bold text-primary uppercase mb-4">Basic</div>
<div class="flex items-baseline gap-1 mb-6">
<span class="text-4xl font-bold font-h2 text-on-background">$49</span>
<span class="text-on-surface-variant">/month</span>
</div>
<p class="text-on-surface-variant mb-8 text-sm">Ideal for small buildings and apartments with up to 20 units.</p>
<ul class="space-y-4 mb-10 text-body-md">
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Maintenance Billing</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Basic Security Desk</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Notice Board</li>
<li class="flex items-center gap-3 text-on-surface-variant/40"><span class="material-symbols-outlined text-xl">cancel</span> Facility Booking</li>
</ul>
<button class="w-full py-4 border-2 border-primary/20 text-primary rounded-xl font-button hover:bg-primary hover:text-white transition-all">Get Started</button>
</div>
<!-- Tier 2 (Featured) -->
<div class="glass-card p-10 squircle bg-white relative border-primary shadow-2xl scale-105 z-10">
<div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white text-[10px] font-bold px-4 py-1 rounded-full uppercase tracking-widest">Most Popular</div>
<div class="text-label-bold font-label-bold text-primary uppercase mb-4">Pro</div>
<div class="flex items-baseline gap-1 mb-6">
<span class="text-4xl font-bold font-h2 text-on-background">$129</span>
<span class="text-on-surface-variant">/month</span>
</div>
<p class="text-on-surface-variant mb-8 text-sm">Perfect for active communities with up to 150 units.</p>
<ul class="space-y-4 mb-10 text-body-md">
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> All Basic Features</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Full Facility Booking</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Visitor Management Pro</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Staff Attendance App</li>
</ul>
<button class="w-full py-4 bg-primary text-white rounded-xl font-button button-glow shadow-lg shadow-primary/30 transition-all">Get Started</button>
</div>
<!-- Tier 3 -->
<div class="glass-card p-10 squircle border-transparent hover:border-primary/20 transition-all">
<div class="text-label-bold font-label-bold text-primary uppercase mb-4">Enterprise</div>
<div class="flex items-baseline gap-1 mb-6">
<span class="text-4xl font-bold font-h2 text-on-background">Custom</span>
</div>
<p class="text-on-surface-variant mb-8 text-sm">Bespoke solutions for large gated communities &amp; townships.</p>
<ul class="space-y-4 mb-10 text-body-md">
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Unlimited Units</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Dedicated Manager</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Multi-Society Sync</li>
<li class="flex items-center gap-3"><span class="material-symbols-outlined text-primary text-xl">check_circle</span> Custom API Integrations</li>
</ul>
<button class="w-full py-4 border-2 border-primary/20 text-primary rounded-xl font-button hover:bg-primary hover:text-white transition-all">Contact Sales</button>
</div>
</div>
</section>
<!-- Final CTA -->
<section class="max-w-7xl mx-auto px-8 mb-20">
<div class="bg-primary-container p-16 squircle text-center relative overflow-hidden">
<div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32 blur-3xl"></div>
<div class="absolute bottom-0 left-0 w-64 h-64 bg-black/10 rounded-full -ml-32 -mb-32 blur-3xl"></div>
<h2 class="text-h2 font-h2 text-white mb-6 relative z-10">Ready to transform your society?</h2>
<p class="text-on-primary-container text-body-lg mb-10 max-w-xl mx-auto relative z-10 opacity-90">Join hundreds of communities that have already upgraded to a smarter, more secure way of living.</p>
<div class="flex flex-col sm:flex-row justify-center gap-4 relative z-10">
<button class="px-10 py-5 bg-white text-primary font-button rounded-xl hover:shadow-2xl transition-all">Get Started Now</button>
<button class="px-10 py-5 bg-primary text-white border border-white/20 font-button rounded-xl hover:bg-primary/80 transition-all">Schedule a Demo</button>
</div>
</div>
</section>
</main>
<!-- Footer -->
<footer class="w-full rounded-t-[2rem] mt-20 bg-[#F2F3F7] dark:bg-slate-950 font-['Inter'] text-sm text-slate-600 dark:text-slate-400 tonal-shift">
<div class="grid grid-cols-2 md:grid-cols-4 gap-12 px-8 py-16 max-w-7xl mx-auto">
<div class="col-span-2 md:col-span-1">
<div class="text-xl font-bold text-[#191C1F] dark:text-white mb-6">eSociety</div>
<p class="mb-6 max-w-xs">The Luminous Ledger. Redefining how communities connect, secure, and grow in the modern age.</p>
</div>
<div class="flex flex-col gap-4">
<h5 class="text-[#191C1F] dark:text-white font-bold uppercase text-[10px] tracking-widest mb-2">Product</h5>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Features</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Pricing</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Security</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Documentation</a>
</div>
<div class="flex flex-col gap-4">
<h5 class="text-[#191C1F] dark:text-white font-bold uppercase text-[10px] tracking-widest mb-2">Company</h5>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">About Us</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Careers</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Contact</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Support</a>
</div>
<div class="flex flex-col gap-4">
<h5 class="text-[#191C1F] dark:text-white font-bold uppercase text-[10px] tracking-widest mb-2">Legal</h5>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Terms</a>
<a class="hover:text-[#5A5AE6] dark:hover:text-white transition-colors" href="#">Privacy</a>
</div>
</div>
<div class="max-w-7xl mx-auto px-8 py-8 border-t border-slate-200 dark:border-slate-800 text-center">
            © 2024 eSociety. The Luminous Ledger. All rights reserved.
        </div>
</footer>
</body></html>