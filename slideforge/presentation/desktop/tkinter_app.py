import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from slideforge.application.use_cases.generate_presentation import GeneratePresentationUseCase
from slideforge.infrastructure.exporters.pptx_exporter import PPTXExporter
from slideforge.theme import get_theme


class SlideForgeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SlideForge AI - Fase 2")
        self.geometry("820x520")
        self.configure(padx=20, pady=20)
        self.doc = tk.StringVar()
        self.banner = tk.StringVar()
        self.output = tk.StringVar()
        self.theme_name = tk.StringVar(value="corporate_blue")
        self.preserve_all = tk.BooleanVar(value=True)
        self.generate_audit = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="Pronto para gerar apresentações com fidelidade visual.")
        tk.Label(self, text="SlideForge AI", font=("Segoe UI", 22, "bold")).pack(pady=(0, 8))
        tk.Label(self, text="Fase 2: fidelidade de conteúdo, imagens e qualidade visual", fg="#445").pack(pady=(0, 15))
        self._row("Documento DOCX/TXT/MD/PDF", self.doc, self._pick_doc)
        self._row("Banner/Logo (PNG/JPG)", self.banner, self._pick_banner)
        self._row("Arquivo de saída (.pptx)", self.output, self._pick_output)
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=8)
        tk.Label(frame, text="Tema", width=24, anchor="w").pack(side="left")
        ttk.Combobox(frame, textvariable=self.theme_name, values=["corporate_blue"], state="readonly").pack(side="left", fill="x", expand=True, padx=8)
        tk.Checkbutton(self, text="Preservar todo o conteúdo", variable=self.preserve_all).pack(anchor="w")
        tk.Checkbutton(self, text="Gerar relatório de auditoria", variable=self.generate_audit).pack(anchor="w")
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", pady=(12, 0))
        tk.Button(self, text="GERAR APRESENTAÇÃO", command=self._generate, height=2, font=("Segoe UI", 12, "bold")).pack(fill="x", pady=20)
        tk.Label(self, textvariable=self.status, fg="#445", wraplength=760).pack(fill="x")

    def _row(self, label: str, var: tk.StringVar, command) -> None:
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=8)
        tk.Label(frame, text=label, width=24, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=8)
        tk.Button(frame, text="Selecionar", command=command).pack(side="right")

    def _pick_doc(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Documentos", "*.docx *.txt *.md *.pdf")])
        if path:
            self.doc.set(path)
            if not self.output.get():
                self.output.set(str(Path(path).with_suffix("")) + "_slideforge.pptx")

    def _pick_banner(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if path:
            self.banner.set(path)

    def _pick_output(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".pptx", filetypes=[("PowerPoint", "*.pptx")])
        if path:
            self.output.set(path)

    def _generate(self) -> None:
        try:
            self.progress.start(10)
            self.status.set("Processando documento...")
            self.update_idletasks()
            exporter = PPTXExporter(theme=get_theme(self.theme_name.get()))
            result = GeneratePresentationUseCase(exporter=exporter).execute(self.doc.get(), self.output.get(), banner_path=self.banner.get() or None)
            audit = result.audit
            if self.generate_audit.get():
                Path(self.output.get()).with_suffix(".audit.txt").write_text(audit.as_report(), encoding="utf-8")
            self.status.set(f"Concluído: {result.output_path} | usados={len(audit.used_block_ids)} | imagens={len(audit.used_image_ids)} | não usados={len(audit.unused_block_ids)} | overflows={audit.critical_overflows}")
            messagebox.showinfo("Concluído", f"Apresentação criada em:\n{result.output_path}")
        except Exception as exc:
            self.status.set(f"Erro: {exc}")
            messagebox.showerror("Erro", str(exc))
        finally:
            self.progress.stop()
