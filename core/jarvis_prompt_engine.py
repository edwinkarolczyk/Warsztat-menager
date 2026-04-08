# version: 1.0
from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from dotenv import load_dotenv

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - środowiska bez pakietu openai
    openai = None  # type: ignore[assignment]

load_dotenv()

_API_KEY = os.getenv("OPENAI_API_KEY")
if openai is not None:
    openai.api_key = _API_KEY

DEFAULT_MODEL = "gpt-3.5-turbo"

_MODEL_PRICING = {
    "gpt-3.5-turbo": (0.0005 / 1000, 0.0015 / 1000),
    "gpt-3.5-turbo-0125": (0.0005 / 1000, 0.0015 / 1000),
    "gpt-4": (0.03 / 1000, 0.06 / 1000),
    "gpt-4-turbo": (0.01 / 1000, 0.03 / 1000),
}

_WM_LOG_PATH = Path("wm.log")
_MONTHLY_STATS: defaultdict[str, dict[str, float | int]] = defaultdict(
    lambda: {"cost": 0.0, "fallbacks": 0}
)


def _append_wm_log(message: str) -> None:
    try:
        with _WM_LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(f"{message}\n")
    except Exception:
        pass


def _match_pricing_key(model: str) -> str | None:
    lower_model = model.lower()
    for candidate in _MODEL_PRICING:
        if lower_model.startswith(candidate):
            return candidate
    return None


def _estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float | None:
    key = _match_pricing_key(model)
    if key is None:
        return None
    prompt_price, completion_price = _MODEL_PRICING[key]
    return prompt_tokens * prompt_price + completion_tokens * completion_price


def _log_ai_usage(model: str, response: Any, *, fallback: bool) -> tuple[int, int, float]:
    usage = getattr(response, "usage", None)
    if usage is None and isinstance(response, Mapping):
        usage = response.get("usage")
    if isinstance(usage, Mapping):
        prompt_tokens = int(usage.get("prompt_tokens") or 0)
        completion_tokens = int(usage.get("completion_tokens") or 0)
        total_tokens = int(usage.get("total_tokens") or prompt_tokens + completion_tokens)
    else:
        prompt_tokens = completion_tokens = total_tokens = 0
    cost = _estimate_cost(model, prompt_tokens, completion_tokens) or 0.0
    month_key = datetime.now().strftime("%Y-%m")
    stats = _MONTHLY_STATS[month_key]
    stats["cost"] = float(stats.get("cost", 0.0)) + float(cost)
    if fallback:
        stats["fallbacks"] = int(stats.get("fallbacks", 0)) + 1

    _append_wm_log(
        "[JARVIS][AI] "
        f"model={model} tokens_in={prompt_tokens} tokens_out={completion_tokens} "
        f"cost={cost:.3f} USD fallback={str(fallback).lower()}"
    )
    _append_wm_log(
        "[JARVIS][AI][MONTH] "
        f"{month_key} cost={stats['cost']:.3f} USD fallback_count={int(stats['fallbacks'])}"
    )
    return prompt_tokens, completion_tokens, cost


def _classify_exception(exc: Exception) -> str:
    details = f"{type(exc).__name__} {exc}".lower()
    if "quota" in details or "limit" in details:
        return "quota"
    if "auth" in details or "key" in details:
        return "auth"
    if "timeout" in details or "connect" in details or "network" in details:
        return "connect"
    return "error"


def _strings_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, (str, int, float)) and str(item)]
    return []


def _offline_summary(data: Mapping[str, Any]) -> str:
    if not isinstance(data, Mapping):
        return "- Brak danych wejściowych."

    points: list[str] = []

    narzedzia = data.get("narzedzia")
    if not isinstance(narzedzia, Mapping):
        narzedzia = {}
    maszyny = data.get("maszyny")
    if not isinstance(maszyny, Mapping):
        maszyny = {}
    zlecenia = data.get("zlecenia")
    if not isinstance(zlecenia, Mapping):
        zlecenia = {}
    operatorzy = data.get("operatorzy")
    if not isinstance(operatorzy, Mapping):
        operatorzy = {}

    idle_tools = _strings_list(narzedzia.get("idle"))
    if idle_tools:
        preview = ", ".join(idle_tools[:5])
        points.append(f"Narzędzia wolne ({len(idle_tools)}): {preview}")

    open_tasks = narzedzia.get("open_tasks")
    if isinstance(open_tasks, int) and open_tasks > 0:
        points.append(f"Otwarte zadania narzędzi: {open_tasks}")

    alert_ids = _strings_list(maszyny.get("alert_ids"))
    if alert_ids:
        preview = ", ".join(alert_ids[:5])
        points.append(f"Alerty/awarie na maszynach ({len(alert_ids)}): {preview}")

    overdue_service = maszyny.get("service_overdue")
    if isinstance(overdue_service, int) and overdue_service > 0:
        overdue_ids = _strings_list(maszyny.get("service_overdue_ids"))
        snippet = f" np. {', '.join(overdue_ids[:5])}" if overdue_ids else ""
        points.append(f"Zaległe przeglądy maszyn: {overdue_service}{snippet}")

    overdue_tasks = zlecenia.get("overdue")
    if isinstance(overdue_tasks, int) and overdue_tasks > 0:
        overdue_ids = _strings_list(zlecenia.get("tasks_overdue_ids"))
        detail = f" np. {', '.join(overdue_ids[:5])}" if overdue_ids else ""
        points.append(f"Zadania po terminie: {overdue_tasks}{detail}")

    due_soon = zlecenia.get("due_soon")
    if isinstance(due_soon, int) and due_soon > 0:
        soon_ids = _strings_list(zlecenia.get("tasks_due_soon_ids"))
        detail = f" np. {', '.join(soon_ids[:5])}" if soon_ids else ""
        points.append(f"Przeglądy zbliżające się do terminu: {due_soon}{detail}")

    unassigned = zlecenia.get("unassigned")
    if isinstance(unassigned, int) and unassigned > 0:
        points.append(f"Zadania bez przydziału: {unassigned}")

    workload = operatorzy.get("obciazenie")
    if isinstance(workload, Mapping) and workload:
        top = sorted(workload.items(), key=lambda item: item[1], reverse=True)[:3]
        formatted = ", ".join(f"{user}: {count}" for user, count in top)
        points.append(f"Największe obciążenie operatorów: {formatted}")

    if not points:
        fallback_candidates = [
            narzedzia.get("count") if isinstance(narzedzia, Mapping) else None,
            zlecenia.get("tasks_count") if isinstance(zlecenia, Mapping) else None,
            operatorzy.get("aktywni") if isinstance(operatorzy, Mapping) else None,
        ]
        labels = [
            "Monitorowane narzędzia",
            "Łączna liczba zadań",
            "Aktywni operatorzy",
        ]
        for value, label in zip(fallback_candidates, labels):
            if isinstance(value, int) and value >= 0:
                points.append(f"{label}: {value}")
        if not points:
            points.append("Brak istotnych alertów w danych warsztatu.")

    if len(points) > 4:
        points = points[:4]

    while len(points) < 2:
        points.append("Monitorowanie kontynuowane – brak dodatkowych alertów.")

    return "\n".join(f"- {text}" for text in points)


def _build_prompt(data: Mapping[str, Any], question: str | None = None) -> str:
    pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
    prompt = (
        "Oto dane operacyjne z systemu Warsztat Menager (statystyki narzędzi, zadań, maszyn):\n"
        f"{pretty_json}\n\n"
        "Wygeneruj krótkie podsumowanie operacyjne z rekomendacjami. Uwzględnij anomalie, przestoje, nadmiar zadań, zaległe przeglądy. "
        "Zwróć listę 2–4 najważniejszych punktów."
    )
    if question:
        stripped = question.strip()
        if stripped:
            prompt = (
                f"{prompt}\n\n"
                "Użytkownik pyta o dane warsztatu. Odpowiadaj krótko i konkretnie, bazuj na przekazanych statystykach.\n"
                f'Pytanie: "{stripped}"'
            )
    return prompt

def summarize_wm_data(
    stats_dict: dict,
    model: str = DEFAULT_MODEL,
    allow_ai: bool = True,
    question: str | None = None,
    *,
    return_metadata: bool = False,
) -> Any:
    payload: Mapping[str, Any] = stats_dict or {}
    question_text = question.strip() if isinstance(question, str) else ""

    meta: dict[str, Any] = {
        "text": "",
        "requested_model": model,
        "model": model,
        "used_ai": False,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cost": 0.0,
        "fallback_model": None,
        "fallback_reason": None,
        "offline_reason": None,
        "question": question_text or None,
    }

    def _finalize(text: str) -> Any:
        meta["text"] = text.strip()
        return meta if return_metadata else meta["text"]

    if allow_ai and openai is not None and _API_KEY:
        attempt_models = [model]
        fallback_reason: str | None = None
        if model.lower().startswith("gpt-4"):
            fallback_model = DEFAULT_MODEL
            if fallback_model.lower() not in {m.lower() for m in attempt_models}:
                attempt_models.append(fallback_model)

        for idx, current_model in enumerate(attempt_models):
            try:
                prompt = _build_prompt(payload, question=question_text or None)
                response = openai.ChatCompletion.create(
                    model=current_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Jesteś analitykiem danych systemu produkcyjnego Warsztat Menager.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=500,
                )
                prompt_tokens, completion_tokens, cost = _log_ai_usage(
                    current_model, response, fallback=idx > 0
                )
                meta.update(
                    {
                        "used_ai": True,
                        "model": current_model,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "cost": cost,
                    }
                )
                if idx > 0:
                    meta["fallback_model"] = current_model
                    meta["fallback_reason"] = fallback_reason
                return _finalize(response.choices[0].message.content or "")
            except Exception as exc:  # pragma: no cover - zależne od API
                reason = _classify_exception(exc)
                fallback_reason = reason
                next_index = idx + 1
                if next_index < len(attempt_models):
                    _append_wm_log(
                        "[JARVIS][AI] fallback requested="
                        f"{meta['requested_model']} -> {attempt_models[next_index]} (reason: {reason})"
                    )
                    continue
                meta["offline_reason"] = reason
                _append_wm_log(
                    f"[JARVIS][AI] offline-fallback used (reason: {reason})"
                )
                offline = _offline_summary(payload)
                if question_text:
                    offline = (
                        f"(Offline) Brak możliwości odpowiedzi na pytanie \"{question_text}\".\n"
                        f"Raport ogólny:\n{offline}"
                    )
                return _finalize(offline)

    reason = "disabled" if not allow_ai else "no-key"
    if allow_ai and openai is None:
        reason = "no-client"
    meta["offline_reason"] = reason
    _append_wm_log(f"[JARVIS][AI] offline-fallback used (reason: {reason})")
    offline_text = _offline_summary(payload)
    if question_text:
        offline_text = (
            f"(Offline) Brak możliwości odpowiedzi na pytanie \"{question_text}\".\n"
            f"Raport ogólny:\n{offline_text}"
        )
    return _finalize(offline_text)


if __name__ == "__main__":
    fake_data = {
        "narzedzia": {"idle": ["W02", "W14"], "open_tasks": 2},
        "maszyny": {"alert_ids": ["M01"], "service_overdue": 1},
        "zlecenia": {"overdue": 3, "tasks_overdue_ids": ["Z01", "Z02"]},
        "operatorzy": {"obciazenie": {"user_1": 5, "user_2": 2}},
    }
    print(summarize_wm_data(fake_data, allow_ai=False))
