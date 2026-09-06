from __future__ import annotations
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from analyzer import analyze_video


class KiwiAIApp:
    def __init__(self, root: tk.Tk):
        self.root = root; root.title("KiwiAI | شمارش کیوی ردیفی"); root.geometry("640x330")
        self.video = tk.StringVar(); self.weights = tk.StringVar(); self.status = tk.StringVar(value="ویدئو و وزن YOLOv5m را انتخاب کن.")
        for row, (label, variable, command) in enumerate((("ویدئوی یک ردیف", self.video, self.pick_video), ("وزن best.pt", self.weights, self.pick_weights))):
            tk.Label(root, text=label).grid(row=row, column=0, padx=12, pady=14, sticky="w")
            tk.Entry(root, textvariable=variable, width=58).grid(row=row, column=1, padx=8)
            tk.Button(root, text="انتخاب", command=command).grid(row=row, column=2, padx=8)
        tk.Button(root, text="شروع شمارش", command=self.start, bg="#16803c", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=1, pady=22)
        tk.Label(root, textvariable=self.status, wraplength=590, justify="right").grid(row=3, column=0, columnspan=3, padx=16, pady=18)
        self.count = tk.Label(root, text="تعداد تأییدشده: —", font=("Arial", 18, "bold")); self.count.grid(row=4, column=0, columnspan=3)

    def pick_video(self): self.video.set(filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.avi *.mov")]))
    def pick_weights(self): self.weights.set(filedialog.askopenfilename(filetypes=[("PyTorch", "*.pt")]))
    def start(self):
        if not self.video.get() or not self.weights.get(): return messagebox.showwarning("KiwiAI", "اول ویدئو و فایل best.pt را انتخاب کن.")
        threading.Thread(target=self.run, daemon=True).start()
    def run(self):
        output = str(Path(self.video.get()).with_name(Path(self.video.get()).stem + "_counted.mp4"))
        self.root.after(0, self.status.set, "در حال تشخیص، رهگیری و تأیید دوکانتینری…")
        try:
            total = analyze_video(self.video.get(), self.weights.get(), output, lambda p, c: self.root.after(0, self.status.set, f"پیشرفت {p:.0%} | تعداد {c}"))
            self.root.after(0, self.count.config, {"text": f"تعداد تأییدشده: {total}"}); self.root.after(0, self.status.set, f"تمام شد. ویدئوی خروجی: {output}")
        except Exception as error: self.root.after(0, messagebox.showerror, "خطا", str(error))

if __name__ == "__main__":
    KiwiAIApp(tk.Tk()).root.mainloop()
