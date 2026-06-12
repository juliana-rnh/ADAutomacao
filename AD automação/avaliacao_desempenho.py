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

        prompt = f"""Analise esta avaliação de colaborador e forneça:
1. Resumo executivo
2. Pontos fortes
3. Áreas de desenvolvimento
4. Plano de carreira
5. Recomendação de promoção (sim/não)
6. Nota geral (0-10)
7. Justificativa da nota

Seja objetivo, profissional e foque em comportamentos observáveis.

DADOS DO COLABORADOR
Nome: {dados['nome']}
Cargo: {dados['cargo']}
Tempo de empresa: {dados['tempo']}

Profundidade Técnica: {dados['profundidade']}
Abrangência Técnica: {dados['abrangencia']}
Velocidade de Entrega: {dados['velocidade']}
Qualidade: {dados['qualidade']}
Autonomia: {dados['autonomia']}
Aprendizado: {dados['curiosidade']}
Conhecimento de Negócio: {dados['negocio']}
Comunicação: {dados['comunicacao']}
Postura Profissional: {dados['postura']}
Pontos Fortes: {dados['pontos_observados']}
Problemas: {dados['problemas_observados']}
Observações: {dados['observacoes']}

Não responda o meu prompt com "É, claro, com certeza e etc." Traga apenas a avaliação.
"""

        return prompt

    def chamar_ia(self, prompt):
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction="Você é um diretor técnico experiente em avaliação de desempenho."
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