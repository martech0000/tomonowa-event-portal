// Explicit Japan Standard Time keeps event expiry consistent for all visitors.
(() => {
  const now = Date.now();
  const cards = [...document.querySelectorAll('[data-event-end]')];
  const upcoming = cards.filter(card => {
    const ended = now >= Date.parse(card.dataset.eventEnd);
    if (ended) {
      card.classList.add('event-ended');
      card.classList.remove('featured');
      card.querySelector('.event-status').textContent = '開催終了';
      const link = card.querySelector('.booking-link');
      if (link) {
        const label = document.createElement('p');
        label.className = 'button booking-closed';
        label.textContent = 'このイベントは終了しました';
        link.replaceWith(label);
        card.querySelector('.ticket-bottom > small').textContent = '次回の開催をお楽しみに。';
      }
    }
    return !ended;
  });
  if (now >= Date.parse('2026-09-18T22:30:00+09:00')) document.querySelector('[data-campaign]').hidden = true;
  const next = upcoming[0];
  const dateLabel = document.querySelector('[data-next-date]');
  const mobileLabel = document.querySelector('[data-mobile-date]');
  if (next) {
    next.classList.add('featured');
    next.querySelector('.event-status').textContent = '次回開催';
    const [, month, day] = next.dataset.eventDate.split('-');
    dateLabel.textContent = `${month}.${day} `;
    const weekday = document.createElement('small');
    weekday.textContent = 'FRI';
    dateLabel.append(weekday);
    mobileLabel.textContent = `${Number(month)}.${day} FRI`;
  } else {
    document.querySelector('.next-label').textContent = 'TOMONOWA PARTY';
    dateLabel.textContent = '次回開催をお楽しみに';
    dateLabel.classList.add('no-events');
    document.querySelector('[data-next-info]').hidden = true;
    mobileLabel.textContent = '次回はご案内予定';
    mobileLabel.classList.add('no-events');
    document.querySelector('.booking-guide').textContent = '掲載中のイベントは終了しました。次回の開催をお楽しみに。';
    document.querySelector('.hero .button').firstChild.textContent = 'イベント情報を見る ';
    document.querySelector('.closing .button').firstChild.textContent = 'イベント情報を見る ';
    document.querySelector('.mobile-booking a').firstChild.textContent = 'イベント情報 ';
  }
})();
