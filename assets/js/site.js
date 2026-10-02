(function () {
    "use strict";

    /* ------------------------------------------------------
       Calculator
    ------------------------------------------------------ */

    var form = document.getElementById("crashCalculator");

    if (form) {
        var bankroll = document.getElementById("bankroll");
        var stake = document.getElementById("stake");
        var cashout = document.getElementById("cashout");
        var crash = document.getElementById("crash");

        var returned = document.getElementById("returned");
        var profit = document.getElementById("profit");
        var risk = document.getElementById("risk");
        var message = document.getElementById("calcMessage");

        function numberFrom(el) {
            var value = parseFloat(el.value);
            return Number.isFinite(value) ? value : 0;
        }

        function money(value) {
            return Math.round(value).toLocaleString("fa-IR") + " تومان";
        }

        function updateCalculator(event) {
            if (event) {
                event.preventDefault();
            }

            var total = numberFrom(bankroll);
            var bet = numberFrom(stake);
            var out = numberFrom(cashout);
            var bust = numberFrom(crash);

            if (bet <= 0 || out < 1 || bust < 1) {
                returned.textContent = "—";
                profit.textContent = "—";
                risk.textContent = "—";
                message.textContent = "مبلغ شرط و ضریب‌ها رو درست وارد کن.";
                return;
            }

            var success = out <= bust;
            var returnedAmount = success ? bet * out : 0;
            var profitAmount = success ? returnedAmount - bet : -bet;
            var riskPercent = total > 0 ? (bet / total) * 100 : 0;

            returned.textContent = money(returnedAmount);
            profit.textContent =
                (profitAmount >= 0 ? "+" : "") +
                money(profitAmount);

            risk.textContent =
                total > 0
                    ? riskPercent.toFixed(2) + "%"
                    : "—";

            message.textContent = success
                ? "تو این سناریوی فرضی، Cashout قبل از Crash قرار گرفته و برداشت موفق فرض می‌شه."
                : "تو این سناریوی فرضی، Crash زودتر از Cashout اتفاق افتاده و مبلغ همون شرط از دست می‌ره.";
        }

        form.addEventListener("submit", updateCalculator);

        [bankroll, stake, cashout, crash].forEach(function (el) {
            if (el) {
                el.addEventListener("input", updateCalculator);
            }
        });

        updateCalculator();
    }

    /* ------------------------------------------------------
       Video lazy loading
       The MP4 source is NOT attached at initial page load.
       It is attached only when video gets near viewport.
       Any failure is caught so it cannot break the page.
    ------------------------------------------------------ */

    var video = document.getElementById("lazyCrashVideo");
    var source = document.getElementById("lazyCrashVideoSource");
    var status = document.getElementById("videoStatus");

    if (!video || !source) {
        return;
    }

    var loaded = false;

    function setStatus(text) {
        if (status) {
            status.textContent = text;
        }
    }

    function loadVideo() {
        if (loaded) {
            return;
        }

        try {
            var url = source.getAttribute("data-src");

            if (!url) {
                return;
            }

            source.setAttribute("src", url);
            source.removeAttribute("data-src");

            video.load();

            loaded = true;

            setStatus("آماده پخش");
        } catch (error) {
            setStatus("بارگذاری ویدئو ناموفق بود");
        }
    }

    video.addEventListener(
        "click",
        loadVideo,
        { once: true }
    );

    video.addEventListener(
        "play",
        loadVideo,
        { once: true }
    );

    video.addEventListener(
        "error",
        function () {
            setStatus("خطا در پخش ویدئو");
        }
    );

    if ("IntersectionObserver" in window) {
        try {
            var observer = new IntersectionObserver(
                function (entries, obs) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            loadVideo();
                            obs.unobserve(entry.target);
                        }
                    });
                },
                {
                    rootMargin: "250px 0px",
                    threshold: 0.01
                }
            );

            observer.observe(video);
        } catch (error) {
            /* Do not load automatically if observer fails.
               User can still click the player to load it. */
        }
    }
})();
