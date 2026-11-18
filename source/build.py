#!/usr/bin/env python3
"""WOLK Coffee & Cakes — static site generator.

Run:  python3 build.py
Out:  dist/     the site to deploy (wolkcoffee.co.uk)
      preview/  flat copy with relative links, for previewing only

All copy, prices and facts live in this file. Prices come from
WOLK_HQ/menu-master.xlsx (Square export 15.09.2026). When a price changes
there, change it here and run the script again.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DOMAIN = "https://wolkcoffee.co.uk"
EMAIL = "info@wolkcoffee.com"
MAPS = "https://maps.app.goo.gl/ysuKY3BTDd2YXBEr5"
INSTAGRAM = "https://www.instagram.com/wolkcoffee.uk/"
CAKES_SITE = "https://www.wolkcakes.co.uk/"


def cakes_url(spot):
    """Order link to wolkcakes.co.uk, tagged so Shopify shows which button sent the visit."""
    return (f"{CAKES_SITE}?utm_source=wolkcoffee&amp;utm_medium=referral"
            f"&amp;utm_campaign=site&amp;utm_content={spot}")


def order_btn(spot, label="Order a whole cake", ghost=False):
    cls = "btn ghost" if ghost else "btn"
    return (f'<a class="{cls}" href="{cakes_url(spot)}" target="_blank" '
            f'rel="noopener">{label}<span aria-hidden="true"> ↗</span></a>')
LASTMOD = "2026-10-05"

FONTS = ("https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500"
         "&family=DM+Serif+Display&family=DM+Serif+Text:ital@0;1&display=swap")

e = html.escape


def gbp(p):
    return f"£{p:.2f}"


# ───────────────────────── MENU DATA ─────────────────────────
# (name, price, description)

ESPRESSO_BAR = [
    ("Espresso", 3.20, None), ("Lungo", 3.20, None), ("Macchiato", 3.70, None),
    ("Cortado", 3.70, None), ("Americano", 3.60, None), ("Flat White", 3.90, None),
    ("Cappuccino", 4.10, None), ("Latte", 4.10, None), ("Mocha", 4.20, None),
    ("Red Eye", 4.20, None),
]
FILTER = [
    ("Batch Brew", 3.80, None),
    ("Pour Over", "from £6.00", "single origin, brewed to order. The list changes."),
    ("Coffee Flight", 7.50, None),
]
TURKISH = [("Turkish Coffee", 3.50, None), ("Turkish Tea", 2.00, None)]
NOT_COFFEE = [
    ("Chai Latte", 4.10, None), ("Dirty Chai Latte", 4.50, None),
    ("Matcha Latte", 4.50, None), ("Hot Chocolate", 4.20, None),
    ("Babyccino", 1.50, None),
]
TEA = [(n, 3.40, None) for n in (
    "English Breakfast", "Earl Grey", "Jasmine Green", "Four Seasons Oolong",
    "Peppermint", "Lemongrass", "Rooibos", "Hibiscus")]

BRUNCH_TURKISH = [
    ("Menemen", 11.50, "slow-cooked tomato & pepper, soft-set eggs, feta, sourdough"),
    ("Turkish Breakfast Bowl", 12.00,
     "tomato & cucumber salad, feta, olives, walnuts, soft boiled egg, simit"),
    ("Sucuk & Kaşar Melt", 8.50, "sucuk, kaşar, ezme, paprika butter, pressed sourdough"),
    ("Çılbır", 11.00,
     "Turkish poached eggs, strained yoghurt, chilli oil, sourdough, seed mix"),
]
BRUNCH_CLASSICS = [
    ("Avocado on Toast (VG)", 8.50, "add eggs £1.50"),
    ("Syrnyky / Сирники", 11.50,
     "Ukrainian curd cheese pancakes, seasonal jam, honey, soured cream"),
    ("Smoked Salmon & Poached Eggs", 14.50, None),
]
BRUNCH_SWEET = [("Granola Bowl", 7.50, None), ("Toasted Banana Bread", 7.00, None)]

MORNING_TOAST = [
    ("Toasted Banana Bread", 7.00, None),
    ("Avocado on Toast (VG)", 8.50, None),
    ("Feta & Roasted Pepper", 8.00, None),
    ("Sucuk & Kaşar Melt", 8.50, "sucuk, kaşar, ezme, paprika butter, pressed sourdough"),
]
MORNING_CROISSANT = [
    ("The Caprese", 8.00, None),
    ("Smoked Salmon & Avocado", 9.50, None),
]

BAKERY = [
    ("Croissant", 3.20, None), ("Almond Croissant", 4.20, None),
    ("Cinnamon Bun", 4.00, None), ("Spinach & Cheese Börek", 4.00, None),
    ("Banana Bread", 4.20, None), ("Orange Cake", 4.20, None),
    ("Mixed Berry Muffin", 4.50, None), ("Sesame Cookie", 3.80, None),
]
CAKES = [
    ("San Sebastián Cheesecake", 7.00, None), ("Honey Cake", 5.80, None),
    ("Napoleon Cake", 6.50, None), ("Coffee & Pecan Cake", 5.80, None),
    ("Gateau Chocolat", 5.80, None), ("Glazed Cheesecake Bar", 4.00, None),
    ("Macaron", 4.00, None),
]
# Not on sale (Taha, 05.10.2026) — in menu-master but kept off the site:
# Cheese Ball, Hazelnut Brownie, Donut, Matcha Cookie, Vegan Almond Joys, Tiramisu,
# Chai Latte Cake, Pavlova, Lemon Meringue Tart, Raspberry Tart

# ───────────────────────── FAQ DATA ─────────────────────────
FAQ = [
    ("Visiting", [
        ("Where is WOLK Coffee & Cakes?",
         "16 Hill Rise, Richmond, London TW10 6UA. On Hill Rise, between Richmond "
         "Bridge and Richmond Hill."),
        ("What are the opening hours?", "Every day, 7:30am–5:30pm."),
        ("How far is WOLK from Richmond station?", "About 10 minutes on foot."),
        ("Do I need to book?", "No. WOLK is walk-in only, including weekend brunch."),
        ("Is WOLK dog friendly?", "Yes. Dogs are welcome."),
        ("Is there Wi-Fi? Can I work from WOLK?",
         "Yes. There is Wi-Fi and laptops are welcome when the shop isn't busy."),
        ("Is there outdoor seating?", "Yes. There are tables outside."),
        ("Is the entrance step-free?", "Yes. There is no step at the entrance."),
    ]),
    ("Brunch & food", [
        ("When is weekend brunch served?", "Saturday and Sunday only, 8am–2pm."),
        ("Do you serve brunch on weekdays?",
         "No. Brunch is Saturday & Sunday, 8am–2pm. On weekdays, Morning at WOLK is "
         "served until 2pm: toasts and croissant sandwiches."),
        ("What is menemen?",
         "A Turkish egg dish: slow-cooked tomato and pepper with soft-set eggs. Ours "
         "comes with feta and sourdough."),
        ("What is çılbır?",
         "Turkish poached eggs on strained yoghurt with chilli oil, served with "
         "sourdough."),
        ("What are syrnyky?",
         "Ukrainian curd cheese pancakes, served with seasonal jam, honey and soured "
         "cream."),
        ("Is there a vegan option?",
         "Yes. Avocado on Toast is vegan, and oat and coconut milk are available for "
         "drinks."),
        ("Where can I find allergen information?",
         "Ask our team before you order."),
    ]),
    ("Coffee & drinks", [
        ("What coffee do you serve?",
         "Espresso drinks, batch brew, single origin pour over and Turkish coffee."),
        ("Do you have decaf and plant milks?",
         "Yes. Decaf coffee, oat milk and coconut milk."),
        ("Do you use flavoured syrups?",
         "Only our own. Syrups and infusions are made in house."),
        ("Do you serve Turkish coffee and Turkish tea?",
         "Yes. Turkish coffee is £3.50 and Turkish tea is £2.00."),
        ("Do you sell coffee beans?", "Yes. Bags to take home start at £12.00."),
    ]),
    ("Cakes", [
        ("Do you have Basque cheesecake?",
         "Yes. San Sebastián cheesecake, also called Basque cheesecake, is baked on "
         "site and sold by the slice at £7.00."),
        ("Can I order a whole cake?",
         "Yes. Order at wolkcakes.co.uk with 48 hours' notice and collect from the "
         "shop."),
    ]),
]

# ───────────────────────── LOGO ─────────────────────────
# Vector redraw of WOLK_HQ "Logo/wolklogo2 siyah.png". The "COFFEE & MORE" subline
# is the Istanbul name and is left out. Replace with the original vector if found.
LOGO_ICON = '<g fill="none" stroke="currentColor" stroke-width="1.5"><line class="ray" style="--i:0" pathLength="1" x1="80.83" y1="107.8" x2="80.83" y2="0"/><line class="ray" style="--i:3" pathLength="1" x1="61.0" y1="113.5" x2="1.1" y2="40.0"/><line class="ray" style="--i:1" pathLength="1" x1="69.9" y1="109.5" x2="45.7" y2="42.0"/><line class="ray" style="--i:5" pathLength="1" x1="53.3" y1="119.8" x2="14.9" y2="94.8"/><line class="ray" style="--i:4" pathLength="1" x1="100.66" y1="113.5" x2="160.56" y2="40.0"/><line class="ray" style="--i:2" pathLength="1" x1="91.76" y1="109.5" x2="115.96" y2="42.0"/><line class="ray" style="--i:6" pathLength="1" x1="108.36" y1="119.8" x2="146.76" y2="94.8"/><circle class="ring" pathLength="1" cx="80.83" cy="145.33" r="37.5"/><circle class="ring" pathLength="1" cx="80.83" cy="154.67" r="37.5"/></g><g class="look"><circle class="pupil" cx="80.83" cy="150" r="12.75" fill="currentColor"/></g>'
LOGO_WORD = '<g fill="currentColor"><polygon points="11.25,214.25 21.4,246.9 27.7,246.9 35.6,223.9 43.1,246.9 49.4,246.9 59.4,214.25 54.2,214.25 45.8,238.4 38.3,214.25 33.2,214.25 25.3,238.4 17.0,214.25"/><polygon points="101.25,214.25 107.25,214.25 107.25,241.7 123.1,241.7 123.1,246.9 101.25,246.9"/><polygon points="127.95,214.25 133.8,214.25 133.8,229.8 149.1,214.25 155.6,214.25 143.0,228.9 155.9,246.9 149.4,246.9 138.6,233.9 133.8,238.75 133.8,246.9 127.95,246.9"/><circle cx="78.68" cy="230.68" r="3.5"/></g><circle cx="78.68" cy="230.68" r="14.3" fill="none" stroke="currentColor" stroke-width="6"/>'
WORDMARK_SVG = ('<svg viewBox="10 212.5 147 36.5" aria-hidden="true" focusable="false">'
                + LOGO_WORD + "</svg>")
EYE_SVG = ('<svg class="eye" viewBox="-1 -1 163.66 195.5" role="img" '
           'aria-label="WOLK logo">' + LOGO_ICON + "</svg>")
LOGO_FILE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 169.66 258" '
             'color="#000">' + LOGO_ICON + LOGO_WORD + "</svg>")
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
           '<rect width="48" height="48" fill="#FAF6EE"/>'
           '<circle cx="24" cy="24" r="14.3" fill="none" stroke="#000" stroke-width="6"/>'
           '<circle cx="24" cy="24" r="3.5" fill="#000"/></svg>')

# ───────────────────────── HOME STORY ─────────────────────────
# One ring and one dot, in the logo's own line. They become a Turkish coffee cup,
# the route from Istanbul to London, a pour, a cake, two eggs, and the logo again.
STAGE_SVG = '<svg viewBox="-200 -200 400 400" fill="none" stroke="currentColor" stroke-width="2"><path class="route" d="M120 90Q70 -130 -120 -80" opacity="0"/><path class="spiral" d="M0.0 -0.0 L0.0 -0.3 L0.1 -0.6 L0.2 -0.9 L0.4 -1.2 L0.6 -1.5 L0.9 -1.7 L1.2 -1.9 L1.5 -2.1 L1.9 -2.2 L2.3 -2.3 L2.7 -2.3 L3.1 -2.3 L3.6 -2.2 L4.0 -2.1 L4.5 -1.9 L4.9 -1.6 L5.3 -1.3 L5.7 -0.9 L6.1 -0.5 L6.5 0.0 L6.8 0.5 L7.0 1.1 L7.2 1.7 L7.4 2.4 L7.5 3.1 L7.5 3.8 L7.4 4.6 L7.3 5.3 L7.1 6.1 L6.9 6.9 L6.5 7.6 L6.1 8.4 L5.6 9.1 L5.0 9.8 L4.3 10.4 L3.6 11.1 L2.8 11.6 L1.9 12.1 L1.0 12.6 L0.0 12.9 L-1.0 13.2 L-2.1 13.4 L-3.2 13.5 L-4.4 13.5 L-5.6 13.4 L-6.7 13.2 L-7.9 12.9 L-9.1 12.5 L-10.3 12.0 L-11.4 11.4 L-12.5 10.7 L-13.6 9.9 L-14.6 8.9 L-15.5 7.9 L-16.4 6.8 L-17.2 5.6 L-17.9 4.3 L-18.5 2.9 L-19.0 1.5 L-19.4 0.0 L-19.6 -1.5 L-19.8 -3.1 L-19.8 -4.8 L-19.7 -6.4 L-19.4 -8.0 L-19.0 -9.7 L-18.5 -11.3 L-17.8 -12.9 L-17.0 -14.5 L-16.0 -16.0 L-14.9 -17.4 L-13.7 -18.8 L-12.3 -20.1 L-10.9 -21.3 L-9.3 -22.4 L-7.6 -23.4 L-5.8 -24.2 L-3.9 -24.9 L-2.0 -25.4 L-0.0 -25.8 L2.1 -26.1 L4.1 -26.2 L6.3 -26.1 L8.4 -25.8 L10.5 -25.4 L12.6 -24.8 L14.7 -24.0 L16.7 -23.0 L18.7 -21.9 L20.6 -20.6 L22.4 -19.1 L24.0 -17.5 L25.6 -15.7 L27.1 -13.8 L28.4 -11.7 L29.5 -9.6 L30.5 -7.3 L31.3 -5.0 L31.9 -2.5 L32.3 -0.0 L32.5 2.6 L32.5 5.2 L32.4 7.8 L32.0 10.4 L31.3 13.0 L30.5 15.5 L29.5 18.1 L28.2 20.5 L26.8 22.9 L25.1 25.1 L23.3 27.3 L21.3 29.3 L19.1 31.1 L16.7 32.8 L14.2 34.3 L11.6 35.6 L8.8 36.8 L6.0 37.7 L3.0 38.3 L0.0 38.8 L-3.1 39.0 L-6.2 38.9 L-9.3 38.6 L-12.4 38.1 L-15.5 37.3 L-18.5 36.3 L-21.4 35.0 L-24.3 33.5 L-27.1 31.7 L-29.7 29.7 L-32.2 27.5 L-34.5 25.1 L-36.6 22.5 L-38.6 19.7 L-40.3 16.7 L-41.8 13.6 L-43.0 10.3 L-44.0 7.0 L-44.8 3.5 L-45.2 0.0 L-45.4 -3.6 L-45.3 -7.2 L-44.9 -10.8 L-44.2 -14.4 L-43.3 -17.9 L-42.0 -21.4 L-40.5 -24.8 L-38.7 -28.1 L-36.6 -31.3 L-34.3 -34.3 L-31.7 -37.1 L-28.9 -39.7 L-25.8 -42.1 L-22.6 -44.3 L-19.2 -46.3 L-15.6 -47.9 L-11.8 -49.3 L-8.0 -50.4 L-4.0 -51.2 L-0.0 -51.7 L4.1 -51.9 L8.2 -51.7 L12.3 -51.2 L16.4 -50.4 L20.4 -49.2 L24.3 -47.8 L28.2 -46.0 L31.9 -43.9 L35.5 -41.5 L38.8 -38.8 L42.0 -35.9 L45.0 -32.7 L47.7 -29.2 L50.1 -25.5 L52.2 -21.6 L54.1 -17.6 L55.6 -13.3 L56.8 -9.0 L57.7 -4.5 L58.2 -0.0 L58.3 4.6 L58.1 9.2 L57.5 13.8 L56.5 18.4 L55.2 22.9 L53.5 27.3 L51.5 31.6 L49.1 35.7 L46.4 39.7 L43.4 43.4 L40.1 46.9 L36.5 50.2 L32.6 53.2 L28.5 55.8 L24.1 58.2 L19.6 60.2 L14.9 61.9 L10.0 63.2 L5.0 64.1 L0.0 64.6 L-5.1 64.7 L-10.2 64.5 L-15.3 63.8 L-20.4 62.7 L-25.3 61.2 L-30.2 59.3 L-34.9 57.0 L-39.5 54.4 L-43.9 51.3 L-48.0 48.0 L-51.8 44.3 L-55.4 40.3 L-58.7 36.0 L-61.6 31.4 L-64.2 26.6 L-66.4 21.6 L-68.2 16.4 L-69.6 11.0 L-70.5 5.6 L-71.1 0.0 L-71.2 -5.6 L-70.8 -11.2 L-70.1 -16.8 L-68.8 -22.4 L-67.2 -27.8 L-65.1 -33.1 L-62.5 -38.3 L-59.6 -43.3 L-56.3 -48.0 L-52.5 -52.5 L-48.5 -56.7 L-44.1 -60.6 L-39.3 -64.2 L-34.3 -67.4 L-29.1 -70.1 L-23.6 -72.5 L-17.9 -74.5 L-12.0 -75.9 L-6.1 -77.0 L-0.0 -77.5 L6.1 -77.6 L12.2 -77.2 L18.3 -76.3 L24.4 -75.0 L30.3 -73.1 L36.1 -70.8 L41.7 -68.0 L47.1 -64.8 L52.2 -61.2 L57.1 -57.1 L61.7 -52.7 L65.9 -47.9 L69.7 -42.7 L73.1 -37.3 L76.1 -31.5 L78.7 -25.6 L80.7 -19.4 L82.3 -13.0 L83.4 -6.6 L84.0 -0.0" opacity="0"/><path class="handle" d="M81 -16C122 -16 122 16 81 16" opacity="0"/><circle class="rA" cx="0" cy="21.66" r="46.9"/><circle class="rB" cx="0" cy="33.34" r="46.9"/><path class="gap" d="M0 0L0 -100A100 100 0 0 1 78.18 -62.35Z" stroke="none" opacity="0"/><line class="ry" x1="0" y1="-25.25" x2="0" y2="-160"/><line class="ry" x1="13.66" y1="-23.13" x2="43.91" y2="-107.5"/><line class="ry" x1="24.79" y1="-18.13" x2="99.66" y2="-110"/><line class="ry" x1="34.41" y1="-10.25" x2="82.41" y2="-41.5"/><line class="ry" x1="-34.41" y1="-10.25" x2="-82.41" y2="-41.5"/><line class="ry" x1="-24.79" y1="-18.13" x2="-99.66" y2="-110"/><line class="ry" x1="-13.66" y1="-23.13" x2="-43.91" y2="-107.5"/><circle class="rB2" cx="0" cy="33.34" r="46.9" opacity="0"/><circle class="d2" cx="0" cy="27.5" r="15.94" fill="currentColor" stroke="none" opacity="0"/><path class="slice" d="M0 0L0 -96A96 96 0 0 1 75.06 -59.86Z" opacity="0"/><circle class="d" cx="0" cy="27.5" r="15.94" fill="currentColor" stroke="none"/><g class="word" stroke="none" transform="translate(-101.04 -160) scale(1.25)">__WORD__</g><g class="lab" stroke="none" fill="currentColor" opacity="0"><text x="120" y="122" text-anchor="middle">IST · 2020</text><text x="-120" y="-102" text-anchor="middle">LON · 2025</text></g></svg>'.replace("__WORD__", LOGO_WORD)

STORY_JS = r"""
(function(){var st=document.querySelector('.story');if(!st)return;
var stage=st.querySelector('.stage'),svg=stage.querySelector('svg');
function q(s){return svg.querySelector(s)}
var A=q('.rA'),B=q('.rB'),D=q('.d'),E=q('.rB2'),F=q('.d2'),
R=[].slice.call(svg.querySelectorAll('.ry')),route=q('.route'),spiral=q('.spiral'),
handle=q('.handle'),slice=q('.slice'),gap=q('.gap'),word=q('.word'),lab=q('.lab'),
cap=stage.querySelector('.cap'),chs=[].slice.call(st.querySelectorAll('.ch'));
if(!route.getTotalLength||!chs.length)return;
var RL=route.getTotalLength(),SL=spiral.getTotalLength(),
reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,
caps=['Istanbul, 2020','Istanbul to London','Brew','Bake','Cook','16 Hill Rise'],
Z=[0,0,0,0,0],none=[Z,Z,Z,Z,Z,Z,Z],cut=[],i,a,
logo=[[0,-25.25,0,-160,1],[13.66,-23.13,43.91,-107.5,1],[24.79,-18.13,99.66,-110,1],
[34.41,-10.25,82.41,-41.5,1],[-34.41,-10.25,-82.41,-41.5,1],[-24.79,-18.13,-99.66,-110,1],
[-13.66,-23.13,-43.91,-107.5,1]],
seeds=[[-4,-88,8,-91,1],[66,-62,75,-55,1],[92,-18,95,-6,1],[-10,82,2,79,1],[-84,50,-76,59,1],
[-96,-22,-93,-34,1],[-52,-76,-42,-82,1]];
for(i=0;i<7;i++){a=-Math.PI/2+i*2*Math.PI/7;cut.push([0,0,96*Math.cos(a),96*Math.sin(a),1]);}
function L(x,y,t){return x+(y-x)*t}
function cl(t){return t<0?0:t>1?1:t}
function ez(t){return t*t*(3-2*t)}
/* x: handle, route, routeDraw, spiral, spiralDraw, slice, sliceOut, word, labels */
function scene(n,u){var p,e=ez(u),dx;
if(n===0)return{A:[0,0,84,1],B:[0,0,74,1],D:[0,0,L(54,64,e),1],E:[42,28,38,0],F:[42,28,13,0],R:none,x:[1,0,0,0,0,0,0,0,0]};
if(n===1){p=route.getPointAtLength(RL*e);return{A:[120,90,9,1],B:[-120,-80,9,1],D:[p.x,p.y,6,1],E:[42,28,38,0],F:[42,28,13,0],R:none,x:[0,1,e,0,0,0,0,0,1]};}
if(n===2){p=spiral.getPointAtLength(SL*u);return{A:[0,0,110,1],B:[0,0,98,1],D:[p.x,p.y,7,1],E:[42,28,38,0],F:[42,28,13,0],R:none,x:[0,0,1,1,u,0,0,0,0]};}
if(n===3)return{A:[0,0,118,1],B:[0,0,96,1],D:[0,0,3,1],E:[42,28,38,0],F:[42,28,13,0],R:cut,x:[0,0,1,0,1,1,42*e,0,0]};
if(n===4){dx=L(-8,8,e);return{A:[0,0,118,1],B:[-38,-14,38,1],D:[-38+dx,-14,13,1],E:[42,28,38,1],F:[42+dx,28,13,1],R:seeds,x:[0,0,1,0,1,0,0,0,0]};}
return{A:[0,21.66,46.9,1],B:[0,33.34,46.9,1],D:[0,27.5,15.94,1],E:[0,33.34,46.9,0],F:[0,27.5,15.94,0],R:logo,x:[0,0,1,0,1,0,0,1,0]};}
function mix(s,t,k){var o={},key,j,m;for(key in s){if(key==='R'){o.R=[];for(j=0;j<7;j++){o.R[j]=[];for(m=0;m<5;m++)o.R[j][m]=L(s.R[j][m],t.R[j][m],k);}}
else{o[key]=[];for(j=0;j<s[key].length;j++)o[key][j]=L(s[key][j],t[key][j],k);}}return o;}
function circ(el,v){el.setAttribute('cx',v[0].toFixed(2));el.setAttribute('cy',v[1].toFixed(2));el.setAttribute('r',Math.max(0,v[2]).toFixed(2));el.setAttribute('opacity',v[3].toFixed(3));}
var last=-9,lastCap=-1;
function draw(P){var n=Math.max(0,Math.min(5,Math.floor(P))),f=P-n,k=ez(cl((f-.3)/.4)),
s=scene(n,cl((P-(n-.3))/.6)),j,r,x;
if(n<5&&k>0)s=mix(s,scene(n+1,cl((P-(n+.7))/.6)),k);
circ(A,s.A);circ(B,s.B);circ(D,s.D);circ(E,s.E);circ(F,s.F);
for(j=0;j<7;j++){r=s.R[j];R[j].setAttribute('x1',r[0].toFixed(2));R[j].setAttribute('y1',r[1].toFixed(2));R[j].setAttribute('x2',r[2].toFixed(2));R[j].setAttribute('y2',r[3].toFixed(2));R[j].setAttribute('opacity',r[4].toFixed(3));}
x=s.x;handle.setAttribute('opacity',x[0].toFixed(3));
route.setAttribute('opacity',x[1].toFixed(3));route.setAttribute('stroke-dasharray',RL);route.setAttribute('stroke-dashoffset',(RL*(1-x[2])).toFixed(2));
spiral.setAttribute('opacity',x[3].toFixed(3));spiral.setAttribute('stroke-dasharray',SL);spiral.setAttribute('stroke-dashoffset',(SL*(1-x[4])).toFixed(2));
slice.setAttribute('opacity',x[5].toFixed(3));gap.setAttribute('opacity',x[5].toFixed(3));
slice.setAttribute('transform','translate('+(x[6]*.4339).toFixed(2)+' '+(-x[6]*.901).toFixed(2)+')');
word.setAttribute('opacity',x[7].toFixed(3));lab.setAttribute('opacity',x[8].toFixed(3));
stage.classList.toggle('dark',P>3.5&&P<4.5);
stage.style.setProperty('--p',cl((P+.3)/5.6).toFixed(4));
j=Math.max(0,Math.min(5,Math.round(P)));
if(j!==lastCap){lastCap=j;cap.textContent='0'+(j+1)+' / 06  '+caps[j];
chs.forEach(function(c,m){c.classList.toggle('on',m===j)});}}
function prog(){var sy=window.pageYOffset||0,vh=window.innerHeight,sr=stage.getBoundingClientRect(),
stacked=sr.width>st.clientWidth*.9,y=sy+(stacked?sr.height+(vh-sr.height)/2:vh/2),
C=chs.map(function(c){var b=c.getBoundingClientRect();return b.top+sy+b.height/2}),m,P;
if(y<=C[0])P=(y-C[0])/(C[1]-C[0]);
else if(y>=C[5])P=5+(y-C[5])/(C[5]-C[4]);
else{for(m=0;m<5;m++)if(y<C[m+1])break;P=m+(y-C[m])/(C[m+1]-C[m]);}
P=Math.max(-.3,Math.min(5.3,P));return reduce?Math.round(P):P;}
var tick=false;
function frame(){tick=false;var P=prog();if(Math.abs(P-last)>.0005){last=P;draw(P);}}
function ask(){if(!tick){tick=true;requestAnimationFrame(frame);}}
st.classList.add('live');
addEventListener('scroll',ask,{passive:true});addEventListener('resize',ask);addEventListener('load',ask);
frame();})();
"""

# ───────────────────────── STYLES ─────────────────────────
CSS = """
/* Layout: a printed menu card. Mono label in the margin, serif content beside it,
   prices set right. Hierarchy comes from space, never from colour. */
:root{
  --cream:#FAF6EE; --ink:#000000; --paper:#FFFFFF;
  --display:"DM Serif Display",Georgia,"Times New Roman",serif;
  --text:"DM Serif Text",Georgia,"Times New Roman",serif;
  --mono:"DM Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --measure:40rem; --gutter:clamp(1rem,4vw,2rem);
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2.5rem; --s5:4rem;
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--text);
  font-size:1.0625rem;line-height:1.55}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:.2em}
a:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.wrap{max-width:62rem;margin-inline:auto;padding-inline:var(--gutter)}

.top{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;
  gap:var(--s2) var(--s4);padding-block:var(--s3)}
.mark{display:block;color:var(--ink)}
.mark svg{display:block;height:1.5rem;width:auto}
.nav{display:flex;flex-wrap:wrap;gap:.25rem 1.25rem;margin:0;padding:0;list-style:none;
  font-family:var(--mono);font-size:.75rem;letter-spacing:.08em;text-transform:uppercase}
.nav a{display:inline-block;padding-block:.375rem;text-decoration:none;
  border-bottom:1px solid transparent}
.nav a:hover,.nav a[aria-current="page"]{border-bottom-color:var(--ink)}

.hero{display:grid;gap:var(--s3);max-width:46rem;padding-block:var(--s5) var(--s4)}
.eyebrow{margin:0;font-family:var(--mono);font-size:.75rem;letter-spacing:.1em;
  text-transform:uppercase}
h1{margin:0;font-family:var(--display);font-weight:400;
  font-size:clamp(2.25rem,7vw,4.25rem);line-height:1.02;text-wrap:balance}
.lede{margin:0;max-width:var(--measure);font-size:1.1875rem}
.status{margin:0;font-family:var(--mono);font-size:.8125rem}

.row{display:grid;grid-template-columns:11rem minmax(0,1fr);gap:var(--s2) var(--s4);
  padding-block:var(--s4);border-top:1px solid var(--ink)}
.row>h2{margin:0;padding-top:.5rem;font-family:var(--mono);font-weight:500;
  font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}
.body{display:grid;gap:var(--s2);min-width:0;max-width:var(--measure)}
.body p{margin:0}
.body h3{margin:0;font-family:var(--display);font-weight:400;font-size:1.625rem;
  line-height:1.15;text-wrap:balance}
.body h3:not(:first-child){margin-top:var(--s3)}
@media (max-width:44rem){.row{grid-template-columns:minmax(0,1fr)}.row>h2{padding-top:0}}

.menu{display:grid;gap:.875rem;margin:0;padding:0;list-style:none}
.menu li{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:var(--s3);
  align-items:baseline}
.menu .n{font-size:1.125rem;line-height:1.3}
.menu .p{font-family:var(--mono);font-size:.875rem;font-variant-numeric:tabular-nums;
  white-space:nowrap}
.menu .d{grid-column:1/-1;font-family:var(--mono);font-size:.8125rem;line-height:1.5}
.note,.more{font-family:var(--mono);font-size:.8125rem;line-height:1.5}
.facts{display:grid;gap:.375rem;margin:0;padding:0;list-style:none}
.qa{display:grid;gap:.375rem}
.qa+.qa{margin-top:var(--s2)}
.qa h3{font-size:1.3125rem}
.qa h3:not(:first-child){margin-top:0}
address{font-style:normal}

.foot{margin-top:var(--s5);background:var(--ink);color:var(--cream)}
.foot .wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));
  gap:var(--s4);padding-block:var(--s4)}
.foot h2{margin:0 0 var(--s1);font-family:var(--mono);font-weight:500;font-size:.75rem;
  letter-spacing:.1em;text-transform:uppercase}
.foot p,.foot ul{margin:0;padding:0;list-style:none;font-size:.9375rem}
.foot a:focus-visible,.dark a:focus-visible{outline-color:var(--cream)}
.btn{display:inline-block;padding:.8125rem 1.125rem;border:1px solid var(--ink);
  background:var(--ink);color:var(--cream);font-family:var(--mono);font-size:.75rem;
  letter-spacing:.08em;text-transform:uppercase;text-decoration:none;line-height:1.2;
  transition:background-color .15s ease,color .15s ease}
.btn:hover{background:var(--paper);color:var(--ink)}
.btn.ghost{background:transparent;color:var(--ink)}
.btn.ghost:hover{background:var(--ink);color:var(--cream)}
.ctas{display:flex;flex-wrap:wrap;gap:.75rem;margin:0}
.top{row-gap:var(--s2)}
.order{font-family:var(--mono);font-size:.75rem;letter-spacing:.08em;
  text-transform:uppercase;text-decoration:none;padding:.4375rem .75rem;
  border:1px solid var(--ink);white-space:nowrap}
.order:hover{background:var(--ink);color:var(--cream)}
.navwrap{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s2) 1.5rem}
@media (max-width:44rem){.top{display:grid;grid-template-columns:minmax(0,1fr) auto;
  align-items:center}.navwrap{display:contents}.order{grid-column:2;grid-row:1}
  .top nav{grid-column:1/-1}}
[hidden]{display:none!important}

/* home */
.hero-home{grid-template-columns:minmax(0,1fr) minmax(9rem,16rem);align-items:end;
  gap:var(--s4);max-width:none}
.hero-home .t{display:grid;gap:var(--s3);min-width:0;max-width:46rem}
.eye{display:block;width:100%;height:auto;color:var(--ink);overflow:visible}
.eye .ray,.eye .ring{stroke-dasharray:1}
.eye .pupil{transform-box:fill-box;transform-origin:center}
@media (max-width:44rem){.hero-home{grid-template-columns:minmax(0,1fr);
  padding-block:var(--s4)}.hero-home .art{order:-1;width:8.5rem}}

.tick{overflow:hidden;background:var(--ink);color:var(--cream);padding-block:.875rem}
.track{display:flex}
.track p{margin:0;padding-inline:var(--gutter);font-family:var(--mono);font-size:.75rem;
  letter-spacing:.12em;text-transform:uppercase;line-height:1.9}
.track p+p{display:none}
.track span::after{content:"·";margin-inline:1.25rem}

.duo{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));
  margin-top:var(--s5)}
.panel{display:grid;gap:var(--s2);align-content:start;min-width:0;
  padding:var(--s4) clamp(1.25rem,4vw,2.5rem);background:var(--paper);color:var(--ink)}
.panel.dark{background:var(--ink);color:var(--cream)}
.panel h2{margin:0;font-family:var(--display);font-weight:400;
  font-size:clamp(2rem,5vw,3.25rem);line-height:1.05;text-wrap:balance}
.panel p{margin:0}
.tag{display:inline-block;margin-left:.5rem;padding:.0625rem .5rem;
  border:1px solid currentColor;letter-spacing:.1em}
.trio{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));
  gap:var(--s4);margin-top:var(--s5)}
.col{display:grid;gap:var(--s2);align-content:start;min-width:0;padding-top:var(--s3);
  border-top:1px solid var(--ink)}
.col h2{margin:0;font-family:var(--display);font-weight:400;font-size:2rem;line-height:1.1}
.col p,.col address{margin:0}
.more a::after{content:" →";display:inline-block;transition:transform .2s ease-out}
.more a:hover::after{transform:translateX(.25rem)}

.story{display:grid;grid-template-columns:minmax(0,1fr) minmax(18rem,28rem);
  gap:0 var(--s5);align-items:start;margin-top:var(--s4)}
.stage{position:sticky;top:max(1rem,calc(50vh - 14rem));order:2;aspect-ratio:1;
  background:var(--paper);color:var(--ink);--sbg:var(--paper)}
.stage.dark{background:var(--ink);color:var(--cream);--sbg:var(--ink)}
.stage svg{display:block;width:100%;height:100%}
.stage .gap,.stage .slice{fill:var(--sbg)}
.stage text{font-family:var(--mono);font-size:11px;letter-spacing:.1em}
.stage .cap{position:absolute;left:1rem;bottom:.875rem;margin:0;font-family:var(--mono);
  font-size:.6875rem;letter-spacing:.1em;text-transform:uppercase;white-space:pre}
.stage .bar{position:absolute;left:0;bottom:0;width:100%;height:2px;background:currentColor;
  transform-origin:0 50%;transform:scaleX(var(--p,1))}
.chapters{margin:0;padding:0;list-style:none;min-width:0}
.ch{display:grid;gap:var(--s2);align-content:center;max-width:30rem;min-height:86vh}
.ch h2{margin:0;font-family:var(--display);font-weight:400;
  font-size:clamp(2.25rem,5.5vw,3.75rem);line-height:1.02;text-wrap:balance}
.ch p,.ch address{margin:0}
@media (max-width:52rem){
  .story{grid-template-columns:minmax(0,1fr);margin-top:0}
  .stage{order:0;top:env(safe-area-inset-top,0px);z-index:2;aspect-ratio:auto;
    height:42vh;height:42svh;border-bottom:1px solid var(--ink)}
  .stage.dark{border-bottom-color:var(--cream)}
  .ch{align-content:start;min-height:66vh;min-height:66svh;padding-top:var(--s4)}
}

@media (prefers-reduced-motion:no-preference){
  .stage{transition:background-color .45s ease,color .45s ease}
  .eye .ring{animation:draw .9s cubic-bezier(.6,0,.2,1) backwards}
  .eye .ring+.ring{animation-delay:.15s}
  .eye .ray{animation:draw .7s cubic-bezier(.6,0,.2,1) backwards;
    animation-delay:calc(.55s + var(--i)*.08s)}
  .eye .pupil{animation:pop .5s cubic-bezier(.3,1.6,.5,1) .35s backwards,
    blink 7s 3s infinite}
  .eye .look{transition:transform .25s ease-out}
  .hero-home .t>*{animation:rise .7s cubic-bezier(.2,.7,.2,1) backwards}
  .hero-home .t>:nth-child(2){animation-delay:.08s}
  .hero-home .t>:nth-child(3){animation-delay:.16s}
  .hero-home .t>:nth-child(4){animation-delay:.24s}
  .track{width:max-content;animation:tick 40s linear infinite}
  .track p{padding-inline:0;white-space:nowrap}
  .track p+p{display:block}
  .tick:hover .track{animation-play-state:paused}
}
@media (prefers-reduced-motion:no-preference) and (hover:none){
  .eye .look{animation:look 9s ease-in-out 2s infinite}
}
@keyframes draw{from{stroke-dashoffset:1}}
@keyframes pop{from{transform:scale(0)}}
@keyframes blink{0%,95%,100%{transform:scaleY(1)}97.5%{transform:scaleY(.06)}}
@keyframes rise{from{opacity:0;transform:translateY(.75rem)}}
@keyframes tick{to{transform:translateX(-50%)}}
@keyframes look{0%,100%{transform:translate(0,0)}20%{transform:translate(-7px,2px)}
  45%{transform:translate(6px,-3px)}70%{transform:translate(2px,6px)}}
"""

STATUS_JS = """
(function(){var el=document.querySelector('[data-status]');if(!el)return;try{
var parts=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/London',weekday:'short',
hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()),m={};
parts.forEach(function(x){m[x.type]=x.value});
var t=(Number(m.hour)%24)*60+Number(m.minute),wk=m.weekday==='Sat'||m.weekday==='Sun',s;
if(t>=450&&t<1050){s='Open now, until 5:30pm.';
if(wk&&t>=480&&t<840)s+=' Weekend brunch is on until 2pm.';}
else{s=t<450?'Closed now. Opens today at 7:30am.':'Closed now. Opens tomorrow at 7:30am.';}
el.textContent=s;
var p=document.querySelector('[data-days="'+(wk?'we':'wk')+'"] .tag');if(p)p.hidden=false;
}catch(err){}})();
(function(){var svg=document.querySelector('.eye');
if(!svg||!window.matchMedia||matchMedia('(prefers-reduced-motion: reduce)').matches||
!matchMedia('(hover: hover)').matches)return;
var look=svg.querySelector('.look');
addEventListener('pointermove',function(ev){var r=svg.getBoundingClientRect(),
dx=ev.clientX-(r.left+r.width*.5),dy=ev.clientY-(r.top+r.height*.77),
d=Math.hypot(dx,dy)||1,k=Math.min(d/40,9)/d;
look.style.transform='translate('+(dx*k).toFixed(2)+'px,'+(dy*k).toFixed(2)+'px)';},
{passive:true});})();
"""

# ───────────────────────── HTML HELPERS ─────────────────────────
PAGES = ["", "menu", "weekend-brunch", "morning", "coffee", "cakes", "visit", "faq",
         "about"]
NAV = [("menu", "Menu"), ("weekend-brunch", "Weekend Brunch"), ("morning", "Morning"),
       ("coffee", "Coffee"), ("cakes", "Cakes"), ("visit", "Visit")]


class Ctx:
    def __init__(self, preview):
        self.preview = preview

    def href(self, slug):
        if self.preview:
            return "index.html" if slug == "" else f"{slug}.html"
        return "/" if slug == "" else f"/{slug}/"


def canonical(slug):
    return f"{DOMAIN}/" if slug == "" else f"{DOMAIN}/{slug}/"


def menu_list(items):
    out = ['<ul class="menu">']
    for name, price, desc in items:
        p = price if isinstance(price, str) else gbp(price)
        out.append(f'<li><span class="n">{e(name)}</span><span class="p">{e(p)}</span>')
        if desc:
            out.append(f'<span class="d">{e(desc)}</span>')
        out.append("</li>")
    out.append("</ul>")
    return "".join(out)


def row(label, inner):
    return (f'<section class="row"><h2>{e(label)}</h2>'
            f'<div class="body">{inner}</div></section>')


def hero(eyebrow, h1, lede, status=False, ctas=""):
    s = ('<p class="status" data-status>Open every day, 7:30am–5:30pm.</p>'
         if status else "")
    k = f'<p class="ctas">{ctas}</p>' if ctas else ""
    return (f'<div class="hero"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1>'
            f'<p class="lede">{lede}</p>{s}{k}</div>')


def header(ctx, slug):
    items = "".join(
        f'<li><a href="{ctx.href(s)}"{" aria-current=\"page\"" if s == slug else ""}>'
        f'{e(t)}</a></li>' for s, t in NAV)
    return (f'<header class="wrap top"><a class="mark" href="{ctx.href("")}" '
            f'aria-label="WOLK Coffee &amp; Cakes, home">{WORDMARK_SVG}</a>'
            f'<div class="navwrap"><nav aria-label="Main"><ul class="nav">{items}</ul></nav>'
            f'<a class="order" href="{cakes_url("header")}" target="_blank" '
            f'rel="noopener">Order a cake<span aria-hidden="true"> ↗</span></a></div></header>')


def footer(ctx):
    return f"""<footer class="foot"><div class="wrap">
<div><h2>Visit</h2><address>WOLK Coffee &amp; Cakes<br>16 Hill Rise, Richmond<br>London TW10 6UA</address>
<p><a href="{MAPS}">Google Maps</a></p></div>
<div><h2>Hours</h2><p>Open every day, 7:30am–5:30pm</p>
<p>Weekend brunch: Saturday &amp; Sunday, 8am–2pm</p></div>
<div><h2>More</h2><ul>
<li><a href="{ctx.href('faq')}">FAQ</a></li>
<li><a href="{ctx.href('about')}">About</a></li>
<li><a href="{cakes_url('footer')}">Whole cakes: wolkcakes.co.uk</a></li>
<li><a href="{INSTAGRAM}">Instagram</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
<div><h2>Istanbul</h2><p>WOLK Coffee &amp; More<br>Yeniköy, Sarıyer</p>
<p>Born in Istanbul, Brewed in London.</p></div>
</div></footer>"""


# ───────────────────────── SCHEMA ─────────────────────────
def cafe_schema():
    feats = ["Dogs welcome", "Free Wi-Fi", "Outdoor seating", "Step-free entrance",
             "Walk-in only", "Oat milk", "Coconut milk", "Decaf coffee"]
    return {
        "@context": "https://schema.org",
        "@type": "CafeOrCoffeeShop",
        "@id": f"{DOMAIN}/#cafe",
        "name": "WOLK Coffee & Cakes",
        "alternateName": ["WOLK Coffee", "WOLK"],
        "slogan": "Born in Istanbul, Brewed in London.",
        "description": ("Specialty coffee shop and bakery at 16 Hill Rise, Richmond, "
                        "London. Coffee all day, cakes baked on site, and a Turkish "
                        "weekend brunch on Saturday and Sunday, 8am–2pm."),
        "url": f"{DOMAIN}/",
        "logo": f"{DOMAIN}/logo.svg",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "16 Hill Rise",
            "addressLocality": "Richmond",
            "addressRegion": "London",
            "postalCode": "TW10 6UA",
            "addressCountry": "GB",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                          "Saturday", "Sunday"],
            "opens": "07:30", "closes": "17:30",
        }],
        "servesCuisine": ["Coffee", "Bakery", "Cakes", "Brunch", "Turkish"],
        "priceRange": "££",
        "currenciesAccepted": "GBP",
        "acceptsReservations": False,
        "hasMenu": f"{DOMAIN}/menu/",
        "hasMap": MAPS,
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": f,
                            "value": True} for f in feats],
        "sameAs": [INSTAGRAM, CAKES_SITE],
    }


def menu_schema():
    def sec(name, items, desc=None):
        s = {"@type": "MenuSection", "name": name, "hasMenuItem": []}
        if desc:
            s["description"] = desc
        for n, p, d in items:
            it = {"@type": "MenuItem", "name": n}
            if d:
                it["description"] = d
            if not isinstance(p, str):
                it["offers"] = {"@type": "Offer", "price": f"{p:.2f}",
                                "priceCurrency": "GBP"}
            s["hasMenuItem"].append(it)
        return s

    return {
        "@context": "https://schema.org", "@type": "Menu",
        "@id": f"{DOMAIN}/menu/#menu", "name": "WOLK Coffee & Cakes menu",
        "url": f"{DOMAIN}/menu/", "inLanguage": "en-GB",
        "provider": {"@id": f"{DOMAIN}/#cafe"},
        "hasMenuSection": [
            sec("Weekend Brunch",
                BRUNCH_TURKISH + BRUNCH_CLASSICS + BRUNCH_SWEET,
                "Saturday & Sunday only, 8am–2pm."),
            sec("Morning at WOLK", MORNING_TOAST + MORNING_CROISSANT,
                "Monday to Friday, until 2pm."),
            sec("Coffee", ESPRESSO_BAR + FILTER + TURKISH[:1]),
            sec("Tea & more", TURKISH[1:] + TEA + NOT_COFFEE),
            sec("Bakery", BAKERY),
            sec("Cakes & pastry", CAKES),
        ],
    }


def faq_schema():
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for _, qs in FAQ for q, a in qs],
    }


# ───────────────────────── PAGES ─────────────────────────
def page_home(c):
    ticker = "".join(f"<span>{e(t)}</span>" for t in (
        "Weekdays we bake", "Weekends we cook", "Born in Istanbul, Brewed in London",
        "Open every day, 7:30am–5:30pm", "Weekend brunch: Saturday & Sunday, 8am–2pm",
        "16 Hill Rise, Richmond"))
    b = ('<div class="wrap"><div class="hero hero-home"><div class="t">'
         '<p class="eyebrow">Born in Istanbul, Brewed in London.</p>'
         "<h1>Specialty coffee, cakes and weekend brunch in Richmond.</h1>"
         '<p class="lede">WOLK Coffee &amp; Cakes is a specialty coffee shop and bakery '
         "at 16 Hill Rise, Richmond, London TW10 6UA. Open every day, 7:30am–5:30pm. "
         "Coffee all day, cakes baked on site, and a Turkish brunch on Saturday and "
         "Sunday.</p>"
         '<p class="status" data-status>Open every day, 7:30am–5:30pm.</p>'
         f'<p class="ctas">{order_btn("home-hero")}'
         f'<a class="btn ghost" href="{c.href("menu")}">See the menu</a></p></div>'
         f'<div class="art">{EYE_SVG}</div></div></div>')
    b += (f'<div class="tick"><div class="track"><p>{ticker}</p>'
          f'<p aria-hidden="true">{ticker}</p></div></div>')
    tag = '<span class="tag" hidden>Today</span>'
    ch = [
        ("Istanbul, March 2020", "", "Born in Istanbul.",
         "<p>WOLK opened in Istanbul in March 2020. Turkish coffee and Turkish tea "
         "are on the menu in Richmond.</p>"),
        ("Richmond, February 2025", "", "Brewed in London.",
         "<p>The Richmond shop opened in February 2025, at 16 Hill Rise. Istanbul's "
         "hospitality, London's specialty coffee.</p>"),
        ("Every day, from 7:30am", "", "Coffee, all day.",
         "<p>Espresso, batch brew, pour over and Turkish coffee. Matcha, chai and tea. "
         "Syrups and infusions are made in house.</p>"
         f'<p class="more"><a href="{c.href("coffee")}">Coffee</a><br>'
         f'<a href="{c.href("menu")}">Full menu with prices</a></p>'),
        ("Monday to Friday", "wk", "Weekdays we bake.",
         "<p>Monday to Friday the kitchen is a bakery. San Sebastián cheesecake, honey "
         "cake and Napoleon, by the slice. Morning at WOLK is served until 2pm: toasts, "
         "croissant sandwiches and the Sucuk &amp; Kaşar Melt.</p>"
         "<p>Whole cakes to order at wolkcakes.co.uk, with 48 hours' notice.</p>"
         f'<p class="ctas">{order_btn("home-bake")}</p>'
         f'<p class="more"><a href="{c.href("cakes")}">Cakes</a><br>'
         f'<a href="{c.href("morning")}">Morning at WOLK</a></p>'),
        ("Saturday & Sunday", "we", "Weekends we cook.",
         "<p>Saturday &amp; Sunday only, 8am–2pm. Menemen. Çılbır. Turkish Breakfast "
         "Bowl. Syrnyky / Сирники. Walk-in only.</p>"
         f'<p class="more"><a href="{c.href("weekend-brunch")}">Weekend Brunch menu</a></p>'),
        ("16 Hill Rise, Richmond", "", "Open every day.",
         "<address>16 Hill Rise, Richmond, London TW10 6UA</address>"
         "<p>7:30am–5:30pm. 10 minutes' walk from Richmond station. Dogs welcome. "
         "Tables outside.</p>"
         f'<p class="more"><a href="{c.href("visit")}">Find us</a><br>'
         f'<a href="{c.href("faq")}">FAQ</a></p>'),
    ]
    items = "".join(
        f'<li class="ch"{" data-days=" + chr(34) + d + chr(34) if d else ""}>'
        f'<p class="eyebrow">{e(eb)}{tag if d else ""}</p><h2>{e(h)}</h2>{body}</li>'
        for eb, d, h, body in ch)
    b += ('<div class="wrap"><div class="story">'
          f'<div class="stage" aria-hidden="true">{STAGE_SVG}'
          '<p class="cap">WOLK</p><span class="bar"></span></div>'
          f'<ol class="chapters">{items}</ol></div></div>')
    site = {"@context": "https://schema.org", "@type": "WebSite",
            "@id": f"{DOMAIN}/#website", "name": "WOLK Coffee & Cakes",
            "url": f"{DOMAIN}/", "inLanguage": "en-GB",
            "publisher": {"@id": f"{DOMAIN}/#cafe"}}
    return dict(
        title="WOLK Coffee & Cakes | Specialty Coffee, Cakes & Weekend Brunch in "
              "Richmond, London",
        desc="Specialty coffee shop and bakery at 16 Hill Rise, Richmond TW10. Open "
             "daily 7:30am–5:30pm. Cakes baked on site. Turkish weekend brunch, "
             "Saturday & Sunday 8am–2pm.",
        body=b, schema=[cafe_schema(), site], js=True, raw=True, story=True)


def page_menu(c):
    b = hero("WOLK Coffee & Cakes, Richmond", "Menu",
             "Everything served at 16 Hill Rise, with prices. Open every day, "
             "7:30am–5:30pm.")
    b += row("Weekend Brunch",
             '<p class="note">Saturday &amp; Sunday only, 8am–2pm.</p>'
             "<h3>Turkish Mornings</h3>" + menu_list(BRUNCH_TURKISH) +
             "<h3>House Classics</h3>" + menu_list(BRUNCH_CLASSICS) +
             "<h3>Something Sweet</h3>" + menu_list(BRUNCH_SWEET))
    b += row("Morning at WOLK",
             '<p class="note">Monday to Friday, until 2pm.</p>'
             "<h3>On Toast</h3>" + menu_list(MORNING_TOAST) +
             "<h3>Croissant Sandwiches</h3>" + menu_list(MORNING_CROISSANT))
    b += row("Coffee",
             "<h3>Espresso Bar</h3>" + menu_list(ESPRESSO_BAR) +
             "<h3>Filter</h3>" + menu_list(FILTER) +
             "<h3>Turkish</h3>" + menu_list(TURKISH) +
             '<p class="note">Decaf, oat milk and coconut milk are available. Syrups '
             "and infusions are made in house.</p>")
    b += row("Tea & more",
             "<h3>Tea</h3>" + menu_list(TEA) +
             "<h3>Chai, Matcha, Chocolate</h3>" + menu_list(NOT_COFFEE))
    b += row("Bakery", menu_list(BAKERY) +
             '<p class="note">Baked on site. The counter changes daily.</p>')
    b += row("Cakes & pastry", menu_list(CAKES) +
             '<p class="note">By the slice. Whole cakes to order at wolkcakes.co.uk, '
             "with 48 hours' notice.</p>"
             f'<p class="ctas">{order_btn("menu")}</p>')
    b += row("Allergens", "<p>Ask our team before you order.</p>")
    return dict(
        title="Menu | Coffee, Brunch, Bakery & Cakes | WOLK Richmond",
        desc="Full menu with prices at WOLK Coffee & Cakes, 16 Hill Rise, Richmond: "
             "coffee, tea, weekday toasts and croissant sandwiches, Turkish weekend "
             "brunch, bakery and cakes.",
        body=b, schema=[cafe_schema(), menu_schema()])


def page_brunch(c):
    b = hero("Saturday & Sunday only, 8am–2pm", "Weekend Brunch at WOLK",
             "16 Hill Rise, Richmond. Walk-in only. Weekdays we bake. Weekends we cook.")
    b += row("Turkish Mornings", menu_list(BRUNCH_TURKISH))
    b += row("House Classics", menu_list(BRUNCH_CLASSICS))
    b += row("Something Sweet", menu_list(BRUNCH_SWEET))
    b += row("Good to know",
             "<p>Brunch is served Saturday and Sunday only, 8am–2pm. No booking: walk "
             "in. Dogs welcome. Tables outside.</p>"
             "<p>Allergens: ask our team before you order.</p>"
             f'<p class="more">On a weekday? <a href="{c.href("morning")}">Morning at '
             "WOLK</a> is served until 2pm.</p>")
    return dict(
        title="Weekend Brunch in Richmond | Menemen, Çılbır, Turkish Breakfast | WOLK",
        desc="Weekend brunch at WOLK, 16 Hill Rise, Richmond. Saturday & Sunday only, "
             "8am–2pm. Menemen, çılbır, Turkish Breakfast Bowl, syrnyky. Walk-in only.",
        body=b, schema=[cafe_schema()])


def page_morning(c):
    b = hero("Monday to Friday, until 2pm", "Morning at WOLK",
             "Toasts and croissant sandwiches, made to order at 16 Hill Rise, Richmond. "
             "Brunch is Saturday &amp; Sunday.")
    b += row("On Toast", menu_list(MORNING_TOAST))
    b += row("Croissant Sandwiches", menu_list(MORNING_CROISSANT))
    b += row("Good to know",
             "<p>Weekdays we bake. The kitchen makes cakes and pastry Monday to Friday, "
             "so the counter is full from 7:30am.</p>"
             "<p>Allergens: ask our team before you order.</p>"
             f'<p class="more"><a href="{c.href("weekend-brunch")}">Weekend Brunch</a>: '
             "Saturday &amp; Sunday, 8am–2pm.</p>")
    return dict(
        title="Weekday Breakfast in Richmond | Morning at WOLK",
        desc="Morning at WOLK: toasts and croissant sandwiches, Monday to Friday until "
             "2pm at 16 Hill Rise, Richmond. Brunch is Saturday & Sunday.",
        body=b, schema=[cafe_schema()])


def page_coffee(c):
    b = hero("Specialty coffee in Richmond", "Coffee at WOLK",
             "Espresso, batch brew, pour over and Turkish coffee at 16 Hill Rise. Every "
             "day, 7:30am–5:30pm.")
    b += row("Espresso Bar", menu_list(ESPRESSO_BAR))
    b += row("Filter", menu_list(FILTER))
    b += row("Turkish", menu_list(TURKISH))
    b += row("Not coffee", menu_list(NOT_COFFEE) +
             f'<p class="more"><a href="{c.href("menu")}">Tea and the full menu</a></p>')
    b += row("Good to know",
             "<p>Decaf, oat milk and coconut milk are available.</p>"
             "<p>Syrups and infusions are made in house.</p>"
             "<p>Coffee beans to take home, from £12.00 a bag.</p>")
    return dict(
        title="Specialty Coffee in Richmond | Espresso, Pour Over, Turkish Coffee | WOLK",
        desc="Specialty coffee at WOLK, 16 Hill Rise, Richmond: espresso bar, batch "
             "brew, single origin pour over and Turkish coffee. Open daily "
             "7:30am–5:30pm.",
        body=b, schema=[cafe_schema()])


def page_cakes(c):
    b = hero("Baked on site, Monday to Friday", "Cakes at WOLK",
             "San Sebastián cheesecake, honey cake, Napoleon and more, by the slice at "
             "16 Hill Rise, Richmond. The counter changes daily.",
             ctas=order_btn("cakes-hero"))
    b += row("By the slice", menu_list(CAKES) +
             '<p class="note">San Sebastián cheesecake is also called Basque '
             "cheesecake.</p>")
    b += row("Bakery", menu_list(BAKERY))
    b += row("Whole cakes",
             "<p>Whole cakes to order at wolkcakes.co.uk. 48 hours' notice, collection "
             "from 16 Hill Rise.</p>"
             f'<p class="ctas">{order_btn("cakes-whole")}</p>')
    b += row("Allergens", "<p>Ask our team before you order.</p>")
    return dict(
        title="Cakes in Richmond | San Sebastián Cheesecake, Honey Cake, Napoleon | WOLK",
        desc="Cakes baked on site at WOLK, 16 Hill Rise, Richmond: San Sebastián "
             "(Basque) cheesecake, honey cake, Napoleon and more by the slice. Whole "
             "cakes to order at wolkcakes.co.uk.",
        body=b, schema=[cafe_schema()])


def page_visit(c):
    b = hero("16 Hill Rise, Richmond", "Visit WOLK",
             "On Hill Rise, between Richmond Bridge and Richmond Hill.", status=True)
    b += row("Address",
             "<address>WOLK Coffee &amp; Cakes<br>16 Hill Rise<br>Richmond, London "
             "TW10 6UA</address>"
             f'<p class="more"><a href="{MAPS}">Open in Google Maps</a></p>')
    b += row("Hours",
             '<ul class="facts"><li>Open every day, 7:30am–5:30pm</li>'
             "<li>Morning at WOLK: Monday to Friday, until 2pm</li>"
             "<li>Weekend brunch: Saturday &amp; Sunday, 8am–2pm</li></ul>")
    b += row("Getting here",
             "<p>10 minutes' walk from Richmond station. Close to Richmond Hill, "
             "Terrace Gardens, the Thames path and Richmond Park.</p>")
    b += row("Good to know",
             '<ul class="facts"><li>Walk-in only, no booking</li><li>Dogs welcome</li>'
             "<li>Tables outside</li><li>Step-free entrance</li>"
             "<li>Wi-Fi. Laptops welcome when the shop isn't busy</li>"
             "<li>Decaf, oat milk and coconut milk</li></ul>")
    b += row("Contact", f'<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>')
    return dict(
        title="Visit WOLK | 16 Hill Rise, Richmond TW10 6UA | Opening Hours",
        desc="WOLK Coffee & Cakes, 16 Hill Rise, Richmond, London TW10 6UA. Open every "
             "day 7:30am–5:30pm. 10 minutes' walk from Richmond station. Walk-in only, "
             "dogs welcome, tables outside.",
        body=b, schema=[cafe_schema()], js=True)


def page_faq(c):
    b = hero("WOLK Coffee & Cakes, Richmond", "Questions",
             "Short answers about visiting, brunch, coffee and cakes at 16 Hill Rise.")
    for group, qs in FAQ:
        inner = "".join(f'<div class="qa"><h3>{e(q)}</h3><p>{e(a)}</p></div>'
                        for q, a in qs)
        b += row(group, inner)
    return dict(
        title="FAQ | WOLK Coffee & Cakes, Richmond",
        desc="Opening hours, weekend brunch times, dogs, Wi-Fi, booking, outdoor "
             "seating, plant milks and whole cake orders at WOLK Coffee & Cakes, "
             "Richmond.",
        body=b, schema=[cafe_schema(), faq_schema()])


def page_about(c):
    b = hero("About WOLK", "Born in Istanbul, Brewed in London.",
             "WOLK opened in Istanbul in March 2020. The Richmond shop opened in "
             "February 2025, at 16 Hill Rise.")
    b += row("Richmond",
             "<p>WOLK Coffee &amp; Cakes is a neighbourhood coffee shop in Richmond. "
             "Istanbul's hospitality, London's specialty coffee.</p>"
             "<p>Open every day, 7:30am–5:30pm.</p>")
    b += row("The kitchen",
             "<h3>Weekdays we bake. Weekends we cook.</h3>"
             "<p>Monday to Friday the kitchen is a bakery: cakes, pastry and bakes made "
             "here. On Saturday and Sunday it cooks brunch, 8am–2pm: menemen, çılbır, "
             "Turkish Breakfast Bowl and syrnyky.</p>"
             f'<p class="more"><a href="{c.href("weekend-brunch")}">Weekend Brunch</a> · '
             f'<a href="{c.href("cakes")}">Cakes</a></p>')
    b += row("Coffee",
             "<p>Espresso, batch brew, pour over and Turkish coffee. Syrups and "
             "infusions are made in house.</p>"
             f'<p class="more"><a href="{c.href("coffee")}">Coffee</a></p>')
    b += row("Istanbul", "<p>WOLK Coffee &amp; More, Yeniköy, Sarıyer, Istanbul.</p>")
    b += row("Whole cakes",
             "<p>Order at wolkcakes.co.uk. 48 hours' notice, collection from the "
             "Richmond shop.</p>"
             f'<p class="ctas">{order_btn("about")}</p>')
    return dict(
        title="About WOLK | Born in Istanbul, Brewed in London",
        desc="WOLK opened in Istanbul in March 2020 and in Richmond, London in "
             "February 2025. A neighbourhood specialty coffee shop and bakery at 16 "
             "Hill Rise.",
        body=b, schema=[cafe_schema()])


BUILDERS = {"": page_home, "menu": page_menu, "weekend-brunch": page_brunch,
            "morning": page_morning, "coffee": page_coffee, "cakes": page_cakes,
            "visit": page_visit, "faq": page_faq, "about": page_about}


# ───────────────────────── RENDER ─────────────────────────
def ld(objs):
    return "".join('<script type="application/ld+json">'
                   + json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
                   + "</script>" for o in objs)


def render(slug, preview, fragment=False):
    c = Ctx(preview)
    p = BUILDERS[slug](c)
    js = f"<script>{STATUS_JS}</script>" if p.get("js") else ""
    if p.get("story"):
        js += f"<script>{STORY_JS}</script>"
    inner = p["body"] if p.get("raw") else f'<div class="wrap">{p["body"]}</div>'
    content = (f'{header(c, slug)}<main>{inner}</main>'
               f'{footer(c)}{js}')
    fonts = (f'<link rel="preconnect" href="https://fonts.googleapis.com">'
             f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             f'<link rel="stylesheet" href="{FONTS}">')
    if fragment:  # the preview host supplies its own document skeleton
        return (f"<title>WOLK Coffee Website</title>{fonts}<style>{CSS}</style>"
                f'{ld(p["schema"])}{content}')
    url = canonical(slug)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="WOLK Coffee &amp; Cakes">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta name="theme-color" content="#FAF6EE">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{fonts}
<style>{CSS}</style>
{ld(p["schema"])}
</head>
<body>
{content}
</body>
</html>
"""


def page_404():
    c = Ctx(False)
    body = hero("Page not found", "Nothing here.",
                f'Try the <a href="/menu/">menu</a> or <a href="/visit/">find us</a> at '
                "16 Hill Rise, Richmond.")
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | WOLK Coffee &amp; Cakes</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head>
<body>{header(c, None)}<main class="wrap">{body}</main>{footer(c)}</body></html>
"""


ROBOTS = f"""# WOLK Coffee & Cakes — every crawler is welcome, AI search included.
User-agent: *
Allow: /

User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: bingbot
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""

LLMS = f"""# WOLK Coffee & Cakes

> Specialty coffee shop and bakery at 16 Hill Rise, Richmond, London TW10 6UA. Open every day, 7:30am–5:30pm. Coffee all day, cakes baked on site, and a Turkish weekend brunch on Saturday and Sunday, 8am–2pm.

Key facts:
- Address: 16 Hill Rise, Richmond, London TW10 6UA. 10 minutes' walk from Richmond station.
- Hours: every day, 7:30am–5:30pm.
- Weekend brunch: Saturday and Sunday only, 8am–2pm. Menemen, çılbır, Turkish Breakfast Bowl, syrnyky. There is no brunch on weekdays.
- Weekdays: Morning at WOLK (toasts and croissant sandwiches) until 2pm.
- Walk-in only. Dogs welcome. Tables outside. Step-free entrance. Wi-Fi.
- Decaf, oat milk and coconut milk available. Syrups and infusions are made in house.
- Whole cakes are ordered at https://www.wolkcakes.co.uk/ with 48 hours' notice.
- Contact: {EMAIL}

## Pages

- [Menu]({DOMAIN}/menu/): everything served, with prices
- [Weekend Brunch]({DOMAIN}/weekend-brunch/): Saturday and Sunday, 8am–2pm
- [Morning at WOLK]({DOMAIN}/morning/): weekday menu, until 2pm
- [Coffee]({DOMAIN}/coffee/): espresso bar, batch brew, pour over, Turkish coffee
- [Cakes]({DOMAIN}/cakes/): San Sebastián (Basque) cheesecake, honey cake, Napoleon by the slice
- [Visit]({DOMAIN}/visit/): address, hours, directions
- [FAQ]({DOMAIN}/faq/): dogs, Wi-Fi, booking, seating, plant milks
- [About]({DOMAIN}/about/): Istanbul since March 2020, Richmond since February 2025
"""


def sitemap():
    urls = "".join(f"<url><loc>{canonical(s)}</loc><lastmod>{LASTMOD}</lastmod></url>\n"
                   for s in PAGES)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}</urlset>\n")


def main():
    dist, prev = ROOT / "dist", ROOT / "preview"
    for d in (dist, prev):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir()
    for slug in PAGES:
        out = dist / slug / "index.html" if slug else dist / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(slug, preview=False), encoding="utf-8")
        name = "index.html" if slug == "" else f"{slug}.html"
        (prev / name).write_text(
            render(slug, preview=True, fragment=(slug == "")), encoding="utf-8")
    (dist / "404.html").write_text(page_404(), encoding="utf-8")
    (dist / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (dist / "llms.txt").write_text(LLMS, encoding="utf-8")
    (dist / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (dist / "logo.svg").write_text(LOGO_FILE, encoding="utf-8")
    (dist / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
