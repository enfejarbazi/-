'use strict';
const normalize = text => text.normalize('NFKC').replace(/[يى]/g,'ی').replace(/ك/g,'ک').replace(/[\u200c\u200d]/g,' ').toLocaleLowerCase('fa').replace(/\s+/g,' ').trim();
const search = document.querySelector('#site-search');
if (search) {
  const cards = [...document.querySelectorAll('.search-card')];
  const status = document.querySelector('#search-status');
  const filter = () => {
    const terms = normalize(search.value).split(' ').filter(Boolean);
    let count = 0;
    for (const card of cards) { const text = normalize(card.textContent); card.hidden = !terms.every(term => text.includes(term)); if (!card.hidden) count++; }
    status.textContent = count ? `${count.toLocaleString('fa-IR')} مطلب پیدا شد` : 'نتیجه‌ای پیدا نشد. یک عبارت کوتاه‌تر امتحان کنید.';
  };
  search.addEventListener('input',filter); filter();
}
const urlForm = document.querySelector('#url-tool');
if (urlForm) urlForm.addEventListener('submit', event => {
  event.preventDefault();
  const input = document.querySelector('#url-input').value.trim();
  const output = document.querySelector('#url-output');
  try {
    if (!/^https?:\/\//i.test(input)) throw new Error('آدرس را با https:// یا http:// وارد کنید.');
    const url = new URL(input);
    if (!url.hostname || !/^https?:$/.test(url.protocol)) throw new Error('فقط آدرس وب معتبر پذیرفته می‌شود.');
    const lines = [`نام میزبان: ${url.hostname}`,`پروتکل: ${url.protocol.slice(0,-1)}`,`مسیر: ${url.pathname}`];
    if (url.protocol !== 'https:') lines.push('هشدار: این آدرس HTTPS ندارد.');
    if (url.username || url.password) lines.push('هشدار: آدرس شامل بخش نام کاربری یا رمز است؛ نوشته قبل از @ نام میزبان نیست.');
    if (url.hostname.includes('xn--')) lines.push('هشدار: نام میزبان شامل دامنه بین‌المللی است؛ حروف آن را جداگانه بررسی کنید.');
    lines.push('این ابزار فقط اجزای آدرس را جدا می‌کند و رسمی بودن، دسترس‌پذیری یا امنیت سایت را تأیید نمی‌کند.');
    output.replaceChildren(...lines.map(line => { const p = document.createElement('p'); p.textContent = line; return p; }));
  } catch(error) { output.textContent = error.message || 'آدرس معتبر نیست.'; }
});
const oddsForm = document.querySelector('#odds-tool');
if (oddsForm) oddsForm.addEventListener('submit',event => {
  event.preventDefault();
  const odds = Number(document.querySelector('#odds-input').value);
  const amount = Number(document.querySelector('#amount-input').value);
  const output = document.querySelector('#odds-output');
  if (!Number.isFinite(odds) || !Number.isFinite(amount) || odds <= 1 || amount <= 0 || !Number.isFinite(odds * amount)) { output.textContent = 'ضریب باید بیشتر از ۱ و مبلغ مثبت باشد.'; return; }
  output.textContent = `احتمال ضمنی: ${(100 / odds).toLocaleString('fa-IR',{maximumFractionDigits:2})}٪ — بازگشت کل فرضی در صورت برد: ${(amount * odds).toLocaleString('fa-IR',{maximumFractionDigits:2})} — سود خالص فرضی: ${(amount * (odds - 1)).toLocaleString('fa-IR',{maximumFractionDigits:2})}. این محاسبه پیش‌بینی یا پیشنهاد شرط نیست.`;
});
