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

    function num(el) {
        var n = parseFloat(el.value);
        return Number.isFinite(n) ? n : 0;
    }

    function money(n) {
        return Math.round(n).toLocaleString("fa-IR") + " تومان";
    }

    function update(event) {
        if (event) event.preventDefault();

        var b = num(bankroll);
        var s = num(stake);
        var c = num(cashout);
        var x = num(crash);

        if (s <= 0 || c < 1 || x < 1) {
            returned.textContent = "—";
            profit.textContent = "—";
            risk.textContent = "—";
            message.textContent = "مبلغ شرط و ضریب‌ها رو درست وارد کن.";
            return;
        }

        var success = c <= x;
        var r = success ? s * c : 0;
        var p = success ? r - s : -s;
        var rp = b > 0 ? (s / b) * 100 : 0;

        returned.textContent = money(r);
        profit.textContent = (p >= 0 ? "+" : "") + money(p);
        risk.textContent = b > 0 ? rp.toFixed(2) + "%" : "—";

        message.textContent = success
            ? "تو این سناریوی فرضی، Cashout قبل از Crash قرار گرفته و برداشت موفق فرض می‌شه."
            : "تو این سناریوی فرضی، Crash زودتر از Cashout اتفاق افتاده و مبلغ همون شرط از دست می‌ره.";
    }

    form.addEventListener("submit", update);

    [bankroll, stake, cashout, crash].forEach(function (el) {
        el.addEventListener("input", update);
    });

    update();
})();
