"""
Telegram bot для отслеживания курсов валют.

Функциональность:
- Подписка на валютные пары (например, USD/RUB, EUR/RUB)
- Настраиваемый порог изменений (по умолчанию 1%)
- Периодические уведомления (по умолчанию раз в день)
- Команды: /start, /stop, /subscribe, /unsubscribe, /rates, /set_threshold, /help
- Хранение подписок в state.json
"""

from __future__ import annotations

import datetime
import json
import logging
import time
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from supervisor.telegram import get_tg, split_telegram, _send_markdown_telegram
from supervisor.state import load_state, save_state

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# State keys
# ---------------------------------------------------------------------------
STATE_SUBSCRIPTIONS = "exchange_bot_subscriptions"  # Dict[user_id -> List[Subscription]]
STATE_LAST_RATES = "exchange_bot_last_rates"       # Dict[pair -> rate]
STATE_LAST_CHECK = "exchange_bot_last_check"      # timestamp
STATE_USER_THRESHOLDS = "exchange_bot_thresholds" # Dict[user_id -> float] (percent)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Subscription:
    def __init__(self, user_id: int, base: str, quote: str, interval_minutes: int = 1440):
        self.user_id = user_id
        self.base = base.upper()
        self.quote = quote.upper()
        self.interval_minutes = interval_minutes  # 1440 = once per day
        self.last_sent: Optional[float] = None

    def key(self) -> str:
        return f"{self.base}/{self.quote}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "base": self.base,
            "quote": self.quote,
            "interval_minutes": self.interval_minutes,
            "last_sent": self.last_sent,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Subscription":
        sub = cls(
            user_id=d["user_id"],
            base=d["base"],
            quote=d["quote"],
            interval_minutes=d.get("interval_minutes", 1440),
        )
        sub.last_sent = d.get("last_sent")
        return sub

# ---------------------------------------------------------------------------
# Rate fetching
# ---------------------------------------------------------------------------

RATES_API_BASE = "https://api.exchangerate-api.com/v4/latest"

def fetch_rates(base: str = "USD") -> Optional[Dict[str, float]]:
    """Fetch exchange rates from exchangerate-api.com (free, no key)."""
    try:
        url = f"{RATES_API_BASE}/{base}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("base") != base:
            log.warning("Unexpected base in response: %s", data.get("base"))
            return None
        rates = data.get("rates", {})
        if not isinstance(rates, dict):
            return None
        return rates
    except Exception as e:
        log.error("Failed to fetch rates for base %s: %s", base, e)
        return None

def get_pair_rate(base: str, quote: str) -> Optional[float]:
    """Get the rate for base/quote by fetching from base."""
    rates = fetch_rates(base)
    if rates is None:
        return None
    return rates.get(quote)

# ---------------------------------------------------------------------------
# Bot logic
# ---------------------------------------------------------------------------

def format_rate_message(base: str, quote: str, rate: float, change_percent: float = 0.0) -> str:
    """Format a rate update message."""
    emoji = "📈" if change_percent > 0 else "📉" if change_percent < 0 else "➡️"
    change_str = f"({change_percent:+.2f}%)" if change_percent != 0 else ""
    return f"{emoji} *{base}/{quote}*: {rate:.4f} {change_str}"

def load_subscriptions() -> List[Subscription]:
    st = load_state()
    raw = st.get(STATE_SUBSCRIPTIONS, {})
    subs = []
    for user_id_str, sub_list in raw.items():
        user_id = int(user_id_str)
        for sub_dict in sub_list:
            subs.append(Subscription.from_dict({**sub_dict, "user_id": user_id}))
    return subs

def save_subscriptions(subs: List[Subscription]) -> None:
    st = load_state()
    by_user: Dict[str, List[Dict[str, Any]]] = {}
    for sub in subs:
        uid = str(sub.user_id)
        if uid not in by_user:
            by_user[uid] = []
        by_user[uid].append(sub.to_dict())
    st[STATE_SUBSCRIPTIONS] = by_user
    save_state(st)

def get_user_threshold(user_id: int) -> float:
    st = load_state()
    thresholds = st.get(STATE_USER_THRESHOLDS, {})
    return thresholds.get(str(user_id), 1.0)  # default 1%

def set_user_threshold(user_id: int, threshold: float) -> None:
    st = load_state()
    if STATE_USER_THRESHOLDS not in st:
        st[STATE_USER_THRESHOLDS] = {}
    st[STATE_USER_THRESHOLDS][str(user_id)] = threshold
    save_state(st)

# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def handle_start(chat_id: int) -> str:
    """Welcome message and help."""
    return (
        "👋 Привет! Я бот для отслеживания курсов валют.\n\n"
        "**Доступные команды:**\n"
        "• /subscribe BASE/QUOTE — подписаться на пару (например, /subscribe USD/RUB)\n"
        "• /unsubscribe BASE/QUOTE — отписаться\n"
        "• /subscriptions — показать ваши подписки\n"
        "• /rates [BASE] — показать все курсы или для конкретной валюты (например, /rates USD)\n"
        "• /set_threshold N — установить порог уведомлений в процентах (по умолчанию 1%)\n"
        "• /help — это сообщение\n\n"
        "Бот будет присылать обновления раз в день и при изменении курса больше port..."
    )

def handle_help(chat_id: int) -> str:
    return handle_start(chat_id)

def handle_subscriptions(chat_id: int) -> str:
    subs = load_subscriptions()
    user_subs = [s for s in subs if s.user_id == chat_id]
    if not user_subs:
        return "У вас пока нет подписок. Добавьте через /subscribe BASE/QUOTE."
    lines = ["*Ваши подписки:*"]
    for sub in user_subs:
        interval_h = sub.interval_minutes / 60
        lines.append(f"• {sub.key()} (обновление каждые {interval_h:.1f} ч)")
    return "\n".join(lines)

def handle_subscribe(chat_id: int, args: str) -> str:
    if not args:
        return "Укажите валютную пару: /subscribe BASE/QUOTE\nНапример: /subscribe USD/RUB"
    try:
        parts = args.strip().split("/")
        if len(parts) != 2:
            return "Неверный формат. Используйте: /subscribe BASE/QUOTE"
        base, quote = parts[0].upper(), parts[1].upper()
        if not base.isalpha() or not quote.isalpha() or len(base) != 3 or len(quote) != 3:
            return "Коды валют должны быть 3-буквенными (например, USD, EUR, RUB)."
    except Exception:
        return "Ошибка разбора команды. Используйте: /subscribe BASE/QUOTE"

    subs = load_subscriptions()
    # Check if already subscribed
    for sub in subs:
        if sub.user_id == chat_id and sub.base == base and sub.quote == quote:
            return f"Вы уже подписаны на {base}/{quote}."

    # Add subscription
    new_sub = Subscription(user_id=chat_id, base=base, quote=quote)
    subs.append(new_sub)
    save_subscriptions(subs)

    return f"✅ Подписка на {base}/{quote} добавлена. Вы будете получать обновления."

def handle_unsubscribe(chat_id: int, args: str) -> str:
    if not args:
        return "Укажите валютную пару: /unsubscribe BASE/QUOTE"
    try:
        parts = args.strip().split("/")
        if len(parts) != 2:
            return "Неверный формат. Используйте: /unsubscribe BASE/QUOTE"
        base, quote = parts[0].upper(), parts[1].upper()
    except Exception:
        return "Ошибка разбора команды."

    subs = load_subscriptions()
    to_remove = [s for s in subs if s.user_id == chat_id and s.base == base and s.quote == quote]
    if not to_remove:
        return f"Вы не подписаны на {base}/{quote}."
    for s in to_remove:
        subs.remove(s)
    save_subscriptions(subs)
    return f"✅ Подписка на {base}/{quote} удалена."

def handle_rates(chat_id: int, args: str) -> str:
    """Show current rates. If args given, show rates for that base currency."""
    base = args.strip().upper() if args else "USD"
    rates = fetch_rates(base)
    if rates is None:
        return f"Не удалось получить курсы для {base}. Попробуйте позже."

    lines = [f"*Курсы валют (база: {base})*"]
    # Sort by rate descending for better readability, but keep popular ones near top
    popular = ["RUB", "EUR", "GBP", "JPY", "CNY", "UAH", "KZT"]
    sorted_rates = sorted(rates.items(), key=lambda x: x[1], reverse=True)

    # First show popular, then rest
    shown = set()
    for cur in popular:
        if cur in rates:
            lines.append(f"• {cur}: {rates[cur]:.4f}")
            shown.add(cur)
    for cur, rate in sorted_rates:
        if cur not in shown:
            lines.append(f"• {cur}: {rate:.4f}")
        if len(lines) >= 20:  # limit to avoid huge message
            lines.append(f"... и ещё {len(rates) - len(lines)} валют")
            break

    return "\n".join(lines)

def handle_set_threshold(chat_id: int, args: str) -> str:
    """Set price change threshold in percent for this user."""
    if not args:
        current = get_user_threshold(chat_id)
        return f"Текущий порог уведомлений: {current:.2f}%\nИспользуйте: /set_threshold <percent>"
    try:
        thr = float(args.strip().replace(",", "."))
        if thr < 0 or thr > 100:
            return "Порог должен быть от 0 до 100%."
    except ValueError:
        return "Неверное число. Пример: /set_threshold 1.5"

    set_user_threshold(chat_id, thr)
    return f"✅ Порог уведомлений установлен: {thr:.2f}%"

# ---------------------------------------------------------------------------
# Main bot loop
# ---------------------------------------------------------------------------

def run_check_cycle() -> None:
    """Main periodic check: fetch rates, compare with previous, send notifications."""
    subs = load_subscriptions()
    if not subs:
        return

    now = time.time()
    st = load_state()
    last_check = float(st.get(STATE_LAST_CHECK, 0))
    # We'll check every hour internally, but only send based on subscription intervals
    if now - last_check < 3600:
        return  # check at most hourly

    st[STATE_LAST_CHECK] = now
    save_state(st)

    # Fetch all needed base currencies
    needed_bases = {sub.base for sub in subs}
    rates_by_base = {}
    for base in needed_bases:
        rates = fetch_rates(base)
        if rates:
            rates_by_base[base] = rates

    last_rates = st.get(STATE_LAST_RATES, {})
    to_send: List[Tuple[int, str]] = []  # (chat_id, message)

    for sub in subs:
        if sub.base not in rates_by_base:
            continue
        rates = rates_by_base[sub.base]
        rate = rates.get(sub.quote)
        if rate is None:
            continue

        pair_key = sub.key()
        old_rate = last_rates.get(pair_key)
        last_rates[pair_key] = rate

        # Check interval
        if sub.last_sent is not None:
            elapsed = now - sub.last_sent
            if elapsed < sub.interval_minutes * 60:
                continue  # not time yet

        # Check threshold if we have previous rate
        send = False
        change_percent = 0.0
        if old_rate is not None and old_rate > 0:
            change = (rate - old_rate) / old_rate * 100.0
            threshold = get_user_threshold(sub.user_id)
            if abs(change) >= threshold:
                send = True
                change_percent = change
        else:
            # First time sending or no previous rate: send initial
            send = True

        if send:
            msg = format_rate_message(sub.base, sub.quote, rate, change_percent)
            to_send.append((sub.user_id, msg))
            sub.last_sent = now

    # Save updated last_sent timestamps and last_rates
    st[STATE_LAST_RATES] = last_rates
    # Update subscriptions with new last_sent
    saved_subs = load_subscriptions()  # reload to avoid race? (single process so OK)
    # We'll just save all subs again
    save_subscriptions(subs)

    # Send messages
    tg = get_tg()
    for chat_id, msg in to_send:
        tg.send_message(chat_id, msg, parse_mode="Markdown")

# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register_handlers() -> None:
    """This function would be called from main Telegram bot loop to register commands."""
    # In our integration, we'll handle commands by routing through the main message handler
    pass

def process_message(chat_id: int, text: str) -> Optional[str]:
    """Process incoming Telegram message as command. Returns reply text or None if not a command."""
    if not text.startswith("/"):
        return None

    parts = text.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    handlers = {
        "/start": lambda: handle_start(chat_id),
        "/help": lambda: handle_help(chat_id),
        "/subscribe": lambda: handle_subscribe(chat_id, args),
        "/unsubscribe": lambda: handle_unsubscribe(chat_id, args),
        "/subscriptions": lambda: handle_subscriptions(chat_id),
        "/rates": lambda: handle_rates(chat_id, args),
        "/set_threshold": lambda: handle_set_threshold(chat_id, args),
    }

    if cmd in handlers:
        return handlers[cmd]()
    else:
        return "Неизвестная команда. Используйте /help для списка команд."

# ---------------------------------------------------------------------------
# Entry point for testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Quick test: fetch USD rates
    print("Fetching USD rates...")
    rates = fetch_rates("USD")
    if rates:
        print(f"USD/RUB = {rates.get('RUB')}")
    else:
        print("Failed")