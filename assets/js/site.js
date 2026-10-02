(function () {
    "use strict";

    var form = document.getElementById("crashCalculator");

    if (!form) {
        return;
    }

    var bankroll = document.getElementById("bankroll");
    var stake = document.getElementById("stake");
    var cashout = document.getElementById("cashout");
    var crash = document.getElementById("crash");

    var returned = document.getElementById("returned");
    var profit = document.getElementById("profit");
    var risk = document.getElementById("risk");
    var message = document.getElementById("calcMessage");

    function getNumber(el) {
        var value = parseFloat(el.value);
        return Number.isFinite(value) ? value : 0;
    }

    function money(value) {
        return Math.round(value).toLocaleString("fa-IR") + " تومان";
    }

    function update(event) {
        if (event) {
            event.preventDefault();
        }

        var total = getNumber(bankroll);
        var bet = getNumber(stake);
        var out = getNumber(cashout);
        var bust = getNumber(crash);

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

    form.addEventListener("submit", update);

    [bankroll, stake, cashout, crash].forEach(function (el) {
        if (el) {
            el.addEventListener("input", update);
        }
    });

    update();
})();
