# version: 1.0
"""Panel Jarvisa osadzony w głównym GUI brygadzisty."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from core.jarvis_engine import JarvisReport, get_notifications, run_analysis_report


class JarvisPanel(ttk.Frame):
    """Panel pozwalający brygadziście uruchomić analizę Jarvisa i przeglądać alerty."""

    def __init__(self, master: Optional[tk.Misc] = None, *, auto_minutes: int | None = None):
        super().__init__(master)
        self.history: list[tuple[datetime, JarvisReport, str | None]] = []
        self.last_report_path: Path | None = None
        self._auto_job: str | None = None
        self._notifications_job: str | None = None
        self._notify_refresh_ms = self._read_notify_refresh_ms()
        self._auto_minutes_var = tk.IntVar(value=max(1, auto_minutes or self._default_interval_minutes()))
        self._auto_enabled = tk.BooleanVar(value=False)
        self.question_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.allow_ai = self._read_allow_ai()
        self._apply_model_from_config()
        self._build_ui()
        self._update_status(
            f"Model: {self.model_var.get()} | AI {'włączone' if self.allow_ai else 'wyłączone'}"
        )
        self.bind("<Destroy>", self._on_destroy, add="+")
        self.refresh_notifications()

    # ------------------------------------------------------------------
    def _default_interval_minutes(self) -> int:
        try:
            from config_manager import ConfigManager

            interval_sec = ConfigManager().get("jarvis.auto_interval_sec", 900)
        except Exception:
            interval_sec = 900

        try:
            interval = int(interval_sec)
        except (TypeError, ValueError):
            interval = 900

        if interval <= 0:
            interval = 900

        return max(1, interval // 60 or 1)

    # ------------------------------------------------------------------
    def _read_notify_refresh_ms(self) -> int:
        try:
            from config_manager import ConfigManager

            raw_value = ConfigManager().get("jarvis.notify.refresh_ms", 10000)
        except Exception:
            raw_value = 10000

        try:
            refresh = int(raw_value)
        except (TypeError, ValueError):
            refresh = 10000

        return max(1000, refresh)

    # ------------------------------------------------------------------
    def _available_models(self) -> list[str]:
        return ["gpt-3.5-turbo", "gpt-4-turbo"]

    # ------------------------------------------------------------------
    def _read_allow_ai(self) -> bool:
        try:
            from config_manager import ConfigManager

            return bool(ConfigManager().get("jarvis.allow_ai", True))
        except Exception:
            return True

    # ------------------------------------------------------------------
    def _read_model_from_config(self) -> str:
        try:
            from config_manager import ConfigManager

            value = ConfigManager().get("jarvis.model", "gpt-3.5-turbo")
        except Exception:
            value = "gpt-3.5-turbo"

        text = str(value).strip()
        if not text:
            text = "gpt-3.5-turbo"
        return text

    # ------------------------------------------------------------------
    def _apply_model_from_config(self) -> None:
        current = self._read_model_from_config()
        options = self._available_models()
        if current not in options:
            options.append(current)
        self._model_options = sorted(set(options))
        self.model_var.set(current)

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=2)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="ew")

        ttk.Label(
            header,
            text="🧠 Jarvis – analiza operacyjna",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        model_frame = ttk.Frame(header)
        model_frame.pack(side="right")
        ttk.Label(model_frame, text="Model:").pack(side="left")
        self.model_combo = ttk.Combobox(
            model_frame,
            values=self._model_options,
            textvariable=self.model_var,
            state="readonly",
            width=15,
        )
        self.model_combo.pack(side="left", padx=(4, 0))
        self.model_combo.bind("<<ComboboxSelected>>", self._on_model_change)

        summary_frame = ttk.LabelFrame(self, text="Podsumowanie")
        summary_frame.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="nsew")
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)

        self.summary_text = ScrolledText(summary_frame, wrap="word", height=16, state="disabled")
        self.summary_text.grid(row=0, column=0, sticky="nsew")

        ttk.Label(self, text="Powiadomienia Jarvisa").grid(
            row=2, column=0, sticky="w", pady=(10, 0), padx=12
        )
        self.notifications = ScrolledText(self, height=6, state="disabled", wrap="word")
        self.notifications.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 5), padx=12)
        self.notifications.tag_config("red", foreground="red")
        self.notifications.tag_config("orange", foreground="orange")
        self.notifications.tag_config("green", foreground="green")

        alerts_frame = ttk.LabelFrame(self, text="Alerty (lokalne)")
        alerts_frame.grid(row=4, column=0, padx=12, pady=(0, 8), sticky="nsew")
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.rowconfigure(0, weight=1)

        self.alerts_tree = ttk.Treeview(
            alerts_frame,
            columns=("level", "message"),
            show="headings",
            height=6,
        )
        self.alerts_tree.heading("level", text="Poziom")
        self.alerts_tree.heading("message", text="Szczegóły")
        self.alerts_tree.column("level", width=90, anchor="center")
        self.alerts_tree.column("message", anchor="w")
        alerts_scroll = ttk.Scrollbar(alerts_frame, orient="vertical", command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=alerts_scroll.set)
        self.alerts_tree.grid(row=0, column=0, sticky="nsew")
        alerts_scroll.grid(row=0, column=1, sticky="ns")
        self._refresh_alerts([])

        question_frame = ttk.Frame(self)
        question_frame.grid(row=5, column=0, padx=12, pady=(0, 8), sticky="ew")
        question_frame.columnconfigure(0, weight=1)

        self.question_entry = ttk.Entry(question_frame, textvariable=self.question_var)
        self.question_entry.grid(row=0, column=0, sticky="ew")
        self.question_entry.bind("<Return>", self._on_question_return)

        ttk.Button(question_frame, text="Wyślij", command=self._send_question).grid(
            row=0,
            column=1,
            padx=(8, 0),
            sticky="e",
        )

        controls = ttk.Frame(self)
        controls.grid(row=6, column=0, padx=12, pady=(0, 8), sticky="ew")
        controls.columnconfigure(0, weight=1)

        left_controls = ttk.Frame(controls)
        left_controls.grid(row=0, column=0, sticky="w")

        ttk.Button(left_controls, text="Analizuj teraz", command=self._on_analyze).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(left_controls, text="Zapisz raport", command=self._on_save).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(left_controls, text="Historia", command=self._show_history).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(left_controls, text="Otwórz ostatni raport", command=self._open_last_report).pack(
            side="left", padx=(0, 8)
        )

        auto_frame = ttk.Frame(controls)
        auto_frame.grid(row=0, column=1, sticky="e")

        ttk.Checkbutton(
            auto_frame,
            text="Auto co X min",
            variable=self._auto_enabled,
            command=self._toggle_auto,
        ).pack(side="left")

        ttk.Spinbox(
            auto_frame,
            from_=1,
            to=240,
            width=4,
            textvariable=self._auto_minutes_var,
            command=self._toggle_auto,
        ).pack(side="left", padx=(4, 0))

        status_label = ttk.Label(self, textvariable=self.status_var, style="WM.Muted.TLabel")
        status_label.grid(row=7, column=0, padx=12, pady=(0, 12), sticky="ew")

    # ------------------------------------------------------------------
    def _update_status(self, text: str) -> None:
        self.status_var.set(text)

    # ------------------------------------------------------------------
    def refresh_notifications(self) -> None:
        if not hasattr(self, "notifications"):
            return

        try:
            notes = get_notifications()
        except Exception:
            notes = []

        self.notifications.configure(state="normal")
        self.notifications.delete("1.0", "end")
        for note in notes[-10:]:
            try:
                level = int(note.get("level", 0))
            except Exception:
                level = 0
            color = "green"
            if level >= 4:
                color = "red"
            elif level == 3:
                color = "orange"
            message = str(note.get("message", ""))
            timestamp = str(note.get("time", ""))
            self.notifications.insert("end", f"[{timestamp}] {message}\n", color)
        self.notifications.configure(state="disabled")

        if self._notifications_job is not None:
            try:
                self.after_cancel(self._notifications_job)
            except Exception:
                pass
            self._notifications_job = None

        if self.winfo_exists():
            self._notifications_job = self.after(
                self._notify_refresh_ms, self.refresh_notifications
            )

    # ------------------------------------------------------------------
    def _refresh_alerts(self, alerts: list) -> None:
        tree = self.alerts_tree
        for item in tree.get_children():
            tree.delete(item)
        if not alerts:
            tree.insert("", "end", values=("-", "Brak alertów – wszystko w normie."))
            return
        for alert in alerts:
            try:
                level = getattr(alert, "level", "info")
                message = getattr(alert, "message", "")
                detail = getattr(alert, "detail", None)
            except Exception:
                level = "info"
                message = str(alert)
                detail = None
            if detail:
                message = f"{message} ({detail})"
            tree.insert("", "end", values=(level.upper(), message))

    # ------------------------------------------------------------------
    def _display_report(self, report: JarvisReport, *, question: str | None, timestamp: datetime) -> None:
        text_widget = self.summary_text
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        content = report.summary.strip() if report.summary else ""
        if question:
            formatted = f"Pytanie: {question}\n\nOdpowiedź:\n{content or '(brak danych)'}"
        else:
            formatted = content or "Brak danych do wyświetlenia."
        text_widget.insert("1.0", formatted)
        text_widget.configure(state="disabled")
        text_widget.see("end")

        self._refresh_alerts(report.alerts)

        model_used = report.metadata.get("model") or self.model_var.get()
        tokens_in = report.metadata.get("prompt_tokens")
        tokens_out = report.metadata.get("completion_tokens")
        cost = report.metadata.get("cost")
        fallback = report.metadata.get("fallback_model")
        offline_reason = report.metadata.get("offline_reason")

        parts = [f"Czas: {timestamp:%Y-%m-%d %H:%M:%S}", f"Model: {model_used}"]
        parts.append(f"AI: {'włączone' if self.allow_ai else 'wyłączone'}")
        if report.metadata.get("used_ai"):
            if isinstance(tokens_in, int) and isinstance(tokens_out, int):
                parts.append(f"Tokens in/out: {tokens_in}/{tokens_out}")
            if isinstance(cost, (int, float)) and cost:
                parts.append(f"Koszt ≈ ${float(cost):.4f}")
        else:
            parts.append("Tryb offline")
            if offline_reason:
                parts.append(f"Powód: {offline_reason}")
        if fallback:
            parts.append(f"Fallback: {fallback}")
        if self.last_report_path and self.last_report_path.exists():
            parts.append(f"Raport: {self.last_report_path.name}")
        self._update_status(" | ".join(parts))

    # ------------------------------------------------------------------
    def _execute_analysis(self, *, question: str | None = None) -> None:
        model = self.model_var.get().strip() or None
        self.allow_ai = self._read_allow_ai()
        allow_flag = self.allow_ai
        try:
            report = run_analysis_report(model=model, allow_ai=allow_flag, question=question)
        except Exception as exc:
            messagebox.showerror("Jarvis", f"Nie udało się uruchomić analizy Jarvisa:\n{exc}")
            return

        metadata_path = report.metadata.get("report_path")
        if isinstance(metadata_path, str):
            candidate = Path(metadata_path)
            self.last_report_path = candidate if candidate.exists() else None
        else:
            self.last_report_path = None

        timestamp = datetime.now()
        self.history.append((timestamp, report, question))
        if len(self.history) > 50:
            self.history = self.history[-50:]

        self._display_report(report, question=question, timestamp=timestamp)

    # ------------------------------------------------------------------
    def _on_analyze(self) -> None:
        self._execute_analysis()

    # ------------------------------------------------------------------
    def _send_question(self) -> None:
        question = self.question_var.get().strip()
        if not question:
            self.question_entry.focus_set()
            return

        self._execute_analysis(question=question)
        self.question_var.set("")
        self.question_entry.focus_set()

    # ------------------------------------------------------------------
    def _on_question_return(self, _event: Optional[tk.Event] = None) -> None:
        self._send_question()

    # ------------------------------------------------------------------
    def _on_save(self) -> None:
        content = self.summary_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Jarvis", "Brak raportu do zapisania.")
            return

        default_name = f"jarvis-{datetime.now():%Y%m%d-%H%M%S}.txt"
        path = filedialog.asksaveasfilename(
            title="Zapisz raport Jarvisa",
            defaultextension=".txt",
            filetypes=[("Plik tekstowy", "*.txt"), ("Markdown", "*.md"), ("Wszystkie", "*.*")],
            initialfile=default_name,
        )
        if not path:
            return

        try:
            Path(path).write_text(content, encoding="utf-8")
        except Exception as exc:
            messagebox.showerror("Jarvis", f"Nie udało się zapisać raportu:\n{exc}")
        else:
            messagebox.showinfo("Jarvis", f"Raport zapisany do pliku:\n{path}")

    # ------------------------------------------------------------------
    def _show_history(self) -> None:
        if not self.history:
            messagebox.showinfo("Jarvis", "Brak zapisanych wyników analizy.")
            return

        lines = []
        for ts, report, question in reversed(self.history[-10:]):
            header = f"{ts:%Y-%m-%d %H:%M:%S}"
            if question:
                header += f" | pytanie: {question}"
            body = report.summary.strip() if report.summary else "(brak podsumowania)"
            lines.append(f"{header}\n{body}")
        messagebox.showinfo("Historia Jarvisa", "\n\n".join(lines))

    # ------------------------------------------------------------------
    def _open_last_report(self) -> None:
        if not self.last_report_path or not self.last_report_path.exists():
            messagebox.showinfo("Jarvis", "Brak automatycznie zapisanego raportu.")
            return

        path = self.last_report_path
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            messagebox.showerror("Jarvis", f"Nie udało się otworzyć raportu:\n{exc}")

    # ------------------------------------------------------------------
    def _on_model_change(self, _event: Optional[tk.Event] = None) -> None:
        new_model = self.model_var.get().strip()
        if not new_model:
            return
        try:
            from config_manager import ConfigManager

            cfg = ConfigManager()
            cfg.set("jarvis.model", new_model)
            cfg.save_all()
            self._update_status(
                f"Zapisano model: {new_model} | AI {'włączone' if self.allow_ai else 'wyłączone'}"
            )
        except Exception as exc:
            messagebox.showerror("Jarvis", f"Nie udało się zapisać modelu:\n{exc}")
            self._apply_model_from_config()
            self.model_combo.configure(values=self._model_options)

    # ------------------------------------------------------------------
    def _toggle_auto(self) -> None:
        if self._auto_enabled.get():
            self._schedule_auto()
        else:
            self._cancel_auto()

    # ------------------------------------------------------------------
    def _schedule_auto(self) -> None:
        self._cancel_auto()
        try:
            minutes = int(self._auto_minutes_var.get())
        except (TypeError, ValueError):
            minutes = self._default_interval_minutes()
        minutes = max(1, minutes)
        delay = minutes * 60 * 1000
        self._auto_job = self.after(delay, self._auto_run)

    # ------------------------------------------------------------------
    def _auto_run(self) -> None:
        self._auto_job = None
        self._execute_analysis()
        if self._auto_enabled.get():
            self._schedule_auto()

    # ------------------------------------------------------------------
    def _cancel_auto(self) -> None:
        if self._auto_job is not None:
            try:
                self.after_cancel(self._auto_job)
            except Exception:
                pass
            self._auto_job = None

    # ------------------------------------------------------------------
    def _on_destroy(self, _event: Optional[tk.Event] = None) -> None:
        self._cancel_auto()
        if self._notifications_job is not None:
            try:
                self.after_cancel(self._notifications_job)
            except Exception:
                pass
            self._notifications_job = None


__all__ = ["JarvisPanel"]

