# version: 1.0
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.jarvis_prompt_engine import summarize_wm_data


class JarvisPanel(tk.Frame):
    def __init__(self, master=None, data_callback=None):
        super().__init__(master)
        self.data_callback = data_callback or (lambda: {})
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        label = ttk.Label(
            self,
            text="🧠 Jarvis – analiza operacyjna Warsztat Menager",
            font=("Segoe UI", 14, "bold"),
        )
        label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.text = tk.Text(self, wrap="word", height=20)
        self.text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        analyze_btn = ttk.Button(
            btn_frame,
            text="🔍 Analizuj teraz",
            command=self._run_jarvis,
        )
        analyze_btn.pack(side="left")

        export_btn = ttk.Button(
            btn_frame,
            text="💾 Zapisz wynik",
            command=self._export_text,
        )
        export_btn.pack(side="right")

    def _run_jarvis(self):
        self.text.delete("1.0", tk.END)
        try:
            data = self.data_callback()
            wynik = summarize_wm_data(data)
            self.text.insert(tk.END, wynik)
        except Exception as exc:
            messagebox.showerror(
                "Błąd Jarvisa",
                f"Nie udało się przeanalizować danych:\n{exc}",
            )

    def _export_text(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Brak treści", "Brak danych do zapisania.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Plik tekstowy", "*.txt"), ("Markdown", "*.md")],
            title="Zapisz podsumowanie Jarvisa",
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo(
                    "Zapisano",
                    f"Wynik zapisany do pliku:\n{filepath}",
                )
            except Exception as exc:
                messagebox.showerror(
                    "Błąd zapisu",
                    f"Nie udało się zapisać pliku:\n{exc}",
                )


if __name__ == "__main__":

    def fake_data():
        return {
            "maszyny": {"awaryjne": ["M-01"], "przestoje_min": 45},
            "narzędzia": {"nieużywane": ["N-16"]},
            "zadania": {"nowe": 3, "w_toku": 5, "zakończone": 10},
            "operatorzy": {"Ola": {"zadania": 2}, "Jacek": {"zadania": 6}},
        }

    root = tk.Tk()
    root.title("Jarvis – test panelu")
    panel = JarvisPanel(master=root, data_callback=fake_data)
    panel.pack(fill="both", expand=True)
    root.mainloop()
