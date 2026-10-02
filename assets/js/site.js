(function () {
  "use strict";

  var form = document.getElementById("crashCalculator");
  if (!form) return;

  var bankroll = document.getElementById("bankroll");
  var stake = document.getElementById("stake");
  var cashout = document.getElementById("cashout");
  var crash = document.getElementById("crash");

  var returned = document.getElementById("returned");
  var profit = document.getElementById("profit");
  var risk = document.getElementById("risk");
  var message = document.getElementById("calcMessage");

  function n(el) {
    var value = parseFloat(el.value);
    return Number.isFinite(value) ? value : 0;
  }

  function money(value) {
    return Math.round(value).toLocaleString("fa-IR") + " تومان";
  }

  function update(e) {
    if (e) e.preventDefault();

    var b = n(bankroll);
    var s = n(stake);
    var c = n(cashout);
    var x = n(crash);

    if (s <= 0 || c < 1 || x < 1) {
      returned.textContent = "—";
      profit.textContent = "—";
      risk.textContent = "—";
      message.textContent = "مبلغ شرط و ضریب‌ها رو درست وارد کن.";
      return;
    }

    var ok = c <= x;
    var r = ok ? s * c : 0;
    var p = ok ? r - s : -s;
    var rp = b > 0 ? (s / b) * 100 : 0;

    returned.textContent = money(r);
    profit.textContent = (p >= 0 ? "+" : "") + money(p);
    risk.textContent = b > 0 ? rp.toFixed(2) + "%" : "—";

    message.textContent = ok
      ? "تو این سناریوی فرضی، Cashout قبل از Crash قرار گرفته و برداشت موفق فرض می‌شه."
      : "تو این سناریوی فرضی، Crash زودتر از Cashout اتفاق افتاده و مبلغ همون شرط از دست می‌ره.";
  }

  form.addEventListener("submit", update);

  [bankroll, stake, cashout, crash].forEach(function (el) {
    el.addEventListener("input", update);
  });

  update();
})();

/* ==========================================================
   LAZY LOAD VIDEO
   The MP4 src is not assigned until the player approaches
   the viewport.
========================================================== */

(function () {
    "use strict";

    var video = document.getElementById("crashLazyVideo");

    if (!video) {
        return;
    }

    var loaded = false;

    function loadVideo() {
        if (loaded) {
            return;
        }

        var sources = video.querySelectorAll("source[data-src]");

        sources.forEach(function (source) {
            source.src = source.dataset.src;
            source.removeAttribute("data-src");
        });

        video.load();
        loaded = true;
    }

    /*
     * Load slightly before the user reaches the player.
     * This keeps initial page weight low while avoiding
     * an obvious delay when Play is pressed.
     */
    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        loadVideo();
                        observer.disconnect();
                    }
                });
            },
            {
                rootMargin: "600px 0px",
                threshold: 0.01
            }
        );

        observer.observe(video);
    } else {
        /*
         * Older-browser fallback.
         */
        loadVideo();
    }

    /*
     * Interaction fallbacks in case the browser delays the
     * IntersectionObserver callback.
     */
    video.addEventListener("pointerenter", loadVideo, {
        once: true
    });

    video.addEventListener("touchstart", loadVideo, {
        once: true,
        passive: true
    });

    video.addEventListener("focus", loadVideo, {
        once: true
    });
})();
