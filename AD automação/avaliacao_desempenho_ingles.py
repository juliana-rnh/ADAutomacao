import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import google.generativeai as genai
import os

# ==========================================
# CONFIGURAÇÃO DA API
# ==========================================
# Defina sua chave do Gemini aqui
# Exemplo:
# GOOGLE_API_KEY=sua_chave_aqui
#
# No Windows:
# setx GOOGLE_API_KEY "sua_chave"
#
# Depois reinicie o terminal.
# ==========================================

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AvaliacaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Inteligente de Avaliação")
        self.root.geometry("1300x950")

        self.campos = {}

        self.criar_interface()

    def criar_interface(self):
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.frame = scrollable_frame

        titulo = tk.Label(
            self.frame,
            text="Sistema Inteligente de Avaliação de Colaboradores",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)

        self.criar_campo("Nome do colaborador")
        self.criar_campo("Cargo")
        self.criar_campo("Tempo de empresa")

        secoes = [
            "Profundidade Técnica",
            "Abrangência Técnica",
            "Velocidade de Entrega",
            "Qualidade das Entregas",
            "Autonomia",
            "Curiosidade e Aprendizado",
            "Conhecimento de Negócio e Sistemas",
            "Comunicação e Participação",
            "Postura Profissional",
            "Pontos Observados",
            "Problemas Observados",
            "Observações Gerais"
        ]

        for secao in secoes:
            self.criar_area(secao)

        btn_salvar = tk.Button(
            self.frame,
            text="Gerar Relatórios com IA",
            bg="#1565c0",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.gerar_relatorios
        )

        btn_salvar.pack(pady=20)

    def criar_campo(self, nome):
        frame = tk.Frame(self.frame)
        frame.pack(fill="x", padx=10, pady=5)

        label = tk.Label(frame, text=nome, width=25, anchor="w", font=("Arial", 10, "bold"))
        label.pack(side="left")

        entry = tk.Entry(frame, width=100)
        entry.pack(side="left", fill="x", expand=True)

        self.campos[nome] = entry

    def criar_area(self, nome):
        label = tk.Label(
            self.frame,
            text=nome,
            font=("Arial", 12, "bold")
        )
        label.pack(anchor="w", padx=10, pady=(15, 5))

        texto = scrolledtext.ScrolledText(self.frame, height=7, wrap=tk.WORD)
        texto.pack(fill="both", padx=10, pady=5)

        self.campos[nome] = texto

    def obter_texto(self, campo):
        widget = self.campos[campo]

        if isinstance(widget, tk.Entry):
            return widget.get().strip()

        return widget.get("1.0", tk.END).strip()

    def montar_prompt(self, dados):

        prompt = f"""Analyze this employee evaluation and provide:
1. Executive summary
2. Strengths
3. Development areas
4. Career plan
5. Promotion recommendation (yes/no)
6. Overall rating (0-10)
7. Rating justification

Be objective, professional, and focus on observable behaviors.

EMPLOYEE DATA
Name: {dados['nome']}
Position: {dados['cargo']}
Tenure: {dados['tempo']}

Technical Depth: {dados['profundidade']}
Technical Scope: {dados['abrangencia']}
Delivery Speed: {dados['velocidade']}
Quality: {dados['qualidade']}
Autonomy: {dados['autonomia']}
Learning: {dados['curiosidade']}
Business Knowledge: {dados['negocio']}
Communication: {dados['comunicacao']}
Professionalism: {dados['postura']}
Strengths: {dados['pontos_observados']}
Issues: {dados['problemas_observados']}
General Notes: {dados['observacoes']}
"""

        return prompt

    def chamar_ia(self, prompt):
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction="You are an experienced technical director evaluating employee performance."
        )

        resposta = model.generate_content(prompt)

        return resposta.text

    def gerar_relatorios(self):
        try:
            nome = self.obter_texto("Nome do colaborador")

            if not nome:
                messagebox.showerror("Erro", "Informe o nome do colaborador")
                return

            dados = {
                "nome": nome,
                "cargo": self.obter_texto("Cargo"),
                "tempo": self.obter_texto("Tempo de empresa"),
                "profundidade": self.obter_texto("Profundidade Técnica"),
                "abrangencia": self.obter_texto("Abrangência Técnica"),
                "velocidade": self.obter_texto("Velocidade de Entrega"),
                "qualidade": self.obter_texto("Qualidade das Entregas"),
                "autonomia": self.obter_texto("Autonomia"),
                "curiosidade": self.obter_texto("Curiosidade e Aprendizado"),
                "negocio": self.obter_texto("Conhecimento de Negócio e Sistemas"),
                "comunicacao": self.obter_texto("Comunicação e Participação"),
                "postura": self.obter_texto("Postura Profissional"),
                "pontos_observados": self.obter_texto("Pontos Observados"),
                "problemas_observados": self.obter_texto("Problemas Observados"),
                "observacoes": self.obter_texto("Observações Gerais")
            }

            prompt = self.montar_prompt(dados)

            messagebox.showinfo(
                "IA",
                "A IA irá gerar os relatórios agora. Isso pode levar alguns segundos."
            )

            resposta_ia = self.chamar_ia(prompt)

            data = datetime.now().strftime("%Y%m%d_%H%M%S")

            pasta = os.getcwd()

            arquivo = os.path.join(
                pasta,
                f"avaliacao_ia_{nome}_{data}.txt"
            )

            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(resposta_ia)

            messagebox.showinfo(
                "Sucesso",
                (f"Relatório gerado com sucesso!\n\n"
                 f"{arquivo}")
            )

        except Exception as e:
            messagebox.showerror(
                "Erro",
                (f"Erro ao gerar relatório:\n\n"
                 f"{str(e)}")
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AvaliacaoApp(root)
    root.mainloop()