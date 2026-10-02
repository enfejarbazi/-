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

    var returnEl = document.getElementById("returnValue");
    var profitEl = document.getElementById("profitValue");
    var riskEl = document.getElementById("riskValue");
    var messageEl = document.getElementById("toolMessage");

    function numberValue(el) {
        var value = parseFloat(el.value);

        if (!Number.isFinite(value)) {
            return 0;
        }

        return value;
    }

    function money(value) {
        return Math.round(value).toLocaleString("fa-IR") + " تومان";
    }

    function calculate(event) {
        if (event) {
            event.preventDefault();
        }

        var b = numberValue(bankroll);
        var s = numberValue(stake);
        var c = numberValue(cashout);
        var x = numberValue(crash);

        if (s <= 0 || c < 1 || x < 1) {
            returnEl.textContent = "—";
            profitEl.textContent = "—";
            riskEl.textContent = "—";

            messageEl.textContent =
                "برای محاسبه، مبلغ شرط و ضرایب معتبر وارد کنید.";

            return;
        }

        var won = c <= x;

        var returned = won ? s * c : 0;
        var profit = won ? returned - s : -s;

        var riskPercent = b > 0
            ? (s / b) * 100
            : 0;

        returnEl.textContent = money(returned);

        profitEl.textContent =
            (profit >= 0 ? "+" : "") +
            money(profit);

        riskEl.textContent =
            b > 0
                ? riskPercent.toFixed(2) + "%"
                : "—";

        if (won) {
            messageEl.textContent =
                "در این سناریوی آموزشی، ضریب Cashout پیش از نقطه Crash قرار دارد و برداشت با موفقیت فرض می شود.";
        } else {
            messageEl.textContent =
                "در این سناریوی آموزشی، Crash پیش از Cashout رخ داده و مبلغ همان شرط از دست می رود.";
        }
    }

    form.addEventListener("submit", calculate);

    [bankroll, stake, cashout, crash].forEach(function (el) {
        el.addEventListener("input", calculate);
    });

    calculate();
})();
