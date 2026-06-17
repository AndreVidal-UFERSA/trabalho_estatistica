import math
import statistics
from tkinter import *
from tkinter import messagebox, ttk

from Estimador import Estimador
from graficos import mostrar_grafico
from graficos import mostrar_grafico, mostrar_grafico_duas_amostras


class JanelaDuasAmostras(Toplevel):
    """
    Sub-janela (Pop-up) para entrada de dados de duas amostras independentes.
    """
    def __init__(self, pai):
        super().__init__(pai)
        self.pai = pai
        self.title("Teste de Duas Amostras Independentes")
        self.geometry("500x450")
        self.transient(pai)  # Mantém a janela sempre acima da principal
        self.focus_set()     # Joga o foco para cá
        
        self.criar_widgets()

    def criar_widgets(self):
        # Amostra A
        Label(self, text="Amostra A (números separados por vírgula ou espaço):").pack(pady=(10, 0))
        self.txt_A = Text(self, height=4)
        self.txt_A.pack(fill=X, padx=10)
        
        # Amostra B
        Label(self, text="Amostra B (números separados por vírgula ou espaço):").pack(pady=(10, 0))
        self.txt_B = Text(self, height=4)
        self.txt_B.pack(fill=X, padx=10)
        
        # Parâmetros adicionais
        frame_param = Frame(self)
        frame_param.pack(fill=X, padx=10, pady=15)
        
        Label(frame_param, text="Nível de Significância (α):").grid(row=0, column=0, sticky=W)
        self.entry_alpha = Entry(frame_param, width=10)
        self.entry_alpha.insert(0, "0.05")
        self.entry_alpha.grid(row=0, column=1, padx=5)
        
        # Botão de Ação interno
        Button(
            self, 
            text="Calcular Teste das Duas Amostras", 
            command=self.processar_teste,
            bg="#c8e6c9",
            fg="black"
        ).pack(pady=10)

    def processar_teste(self):
        try:
            # Captura e limpa o texto da Amostra A
            texto_A = self.txt_A.get("1.0", END).replace(",", " ")
            dados_A = [float(v) for v in texto_A.split()]
            
            # Captura e limpa o texto da Amostra B
            texto_B = self.txt_B.get("1.0", END).replace(",", " ")
            dados_B = [float(v) for v in texto_B.split()]
            
            alpha = float(self.entry_alpha.get())

            if not dados_A or not dados_B:
                raise ValueError("Ambas as amostras precisam ter pelo menos um número!")

            # Instancia os estimadores usando a classe padrão
            est_A = Estimador(dados_A)
            est_B = Estimador(dados_B)

            # Cálculos Inferenciais Combinados (Bilateral)
            p_valor, z_critico, z_calc = Estimador.calculos_inferenciais(est_A, est_B, alpha)
            
            rejeita = abs(z_calc) > z_critico
            conclusao = "Rejeitar H0 (Médias são estatisticamente Diferentes)" if rejeita else "Não Rejeitar H0 (Médias são Iguais)"

            # Montagem do relatório
            relatorio = []
            relatorio.append("=== TESTE DE COMPARAÇÃO DE DUAS MÉDIAS ===")
            relatorio.append(f"Amostra A: n = {est_A.n} | Média = {est_A.media_amostral:.4f} | Var = {est_A.variancia_amostral:.4f}")
            relatorio.append(f"Amostra B: n = {est_B.n} | Média = {est_B.media_amostral:.4f} | Var = {est_B.variancia_amostral:.4f}")
            relatorio.append("\n=== Hipóteses ===")
            relatorio.append("H0: μA = μB\nH1: μA ≠ μB")
            relatorio.append("\n=== Resultados Obtidos ===")
            relatorio.append(f"Estatística Z calculada = {z_calc:.6f}")
            relatorio.append(f"Região Crítica (RC) = Z < {-z_critico:.4f} ou Z > {z_critico:.4f}")
            relatorio.append(f"Nível de significância (α) = {alpha:.2f}")
            relatorio.append(f"Valor-p obtido = {p_valor:.6f} ({p_valor:.4e})")
            relatorio.append(f"\nDecisão Formal: {conclusao}")

            # Atualiza a caixa de texto da janela principal e fecha o pop-up
            self.pai.txt_resultado.delete("1.0", END)
            self.pai.txt_resultado.insert(END, "\n".join(relatorio))
            # ... (código anterior da montagem do relatório) ...
            self.pai.txt_resultado.delete("1.0", END)
            self.pai.txt_resultado.insert(END, "\n".join(relatorio))

            # ESSA LINHA DISPARA O GRÁFICO ANTES DE FECHAR O POP-UP:
            mostrar_grafico_duas_amostras(est_A, est_B, alpha)

            self.destroy()
        except Exception as erro:
            messagebox.showerror("Erro no Cálculo", str(erro), parent=self)


class Aplicacao(Tk):
    def __init__(self):
        super().__init__()
        self.title("Teste de Hipótese")
        self.geometry("730x530")
        self.criar_widgets()

    def criar_widgets(self) -> None:
        # --- SEÇÃO 1: CAMPO DE ENTRADA DA AMOSTRA (UMA AMOSTRA) ---
        Label(self, text="Amostra (números separados por vírgula ou espaço) - Teste Clássico").pack(pady=(10, 0))
        self.txt_amostra = Text(self, height=5)
        self.txt_amostra.pack(fill=X, padx=10)

        # --- SEÇÃO 2: PARÂMETROS DO TESTE (GRID LOGÍSTICO) ---
        frame_hipotese = Frame(self)
        frame_hipotese.pack(fill=X, padx=10, pady=10)

        Label(frame_hipotese, text="Média da hipótese (μ₀):").grid(row=0, column=0, sticky=W)
        self.entry_mu0 = Entry(frame_hipotese)
        self.entry_mu0.grid(row=0, column=1, padx=5)

        Label(frame_hipotese, text="α:").grid(row=0, column=2, sticky=W)
        self.entry_alpha = Entry(frame_hipotese)
        self.entry_alpha.insert(0, "0.05")
        self.entry_alpha.grid(row=0, column=3, padx=5)

        Label(frame_hipotese, text="μ₁:").grid(row=0, column=4, sticky=W)
        self.entry_mu1 = Entry(frame_hipotese)
        self.entry_mu1.grid(row=0, column=5, padx=5)

        Label(frame_hipotese, text="n do cco:").grid(row=0, column=6, sticky=W)
        self.entry_n_cco = Entry(frame_hipotese)
        self.entry_n_cco.grid(row=0, column=7, padx=5)

        Label(frame_hipotese, text="Tipo de teste:").grid(row=1, column=0, sticky=W, pady=10)
        self.tipo_teste = StringVar(value="bilateral")
        self.tipo_grafico = StringVar(value="bilateral")

        ttk.Combobox(frame_hipotese, textvariable=self.tipo_teste, state="readonly",
                     values=["bilateral", "unilateral à direita", "unilateral à esquerda"]).grid(row=1, column=1, columnspan=2, sticky=W)

        Label(frame_hipotese, text="Tipo de gráfico:").grid(row=1, column=3, sticky=W, pady=10)
        ttk.Combobox(frame_hipotese, textvariable=self.tipo_grafico, state="readonly",
                     values=["bilateral", "histograma"]).grid(row=1, column=4, columnspan=2, sticky=W)

        # --- SEÇÃO 4: BOTÕES DE DISPARO ---
        frame_botoes = Frame(self)
        frame_botoes.pack(pady=5)

        Button(frame_botoes, text="Executar Teste Clássico (1 Amostra)", command=self.executar_teste).grid(row=0, column=0, padx=5)
        
        # MODIFICADO: Esse botão agora abre o menu pop-up dinâmico
        Button(
            frame_botoes, 
            text="Abrir Menu: Duas Amostras", 
            command=self.abrir_menu_duas_amostras,
            bg="#e1f5fe"
        ).grid(row=0, column=1, padx=5)

        # --- SEÇÃO 5: VISUALIZAÇÃO DO RELATÓRIO ---
        Label(self, text="Resultado").pack()
        self.txt_resultado = Text(self, height=15)
        self.txt_resultado.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def obter_amostra(self) -> list[float]:
        texto = self.txt_amostra.get("1.0", END).replace(",", " ")
        return [float(valor) for valor in texto.split()]

    def abrir_menu_duas_amostras(self):
        """Dispara a abertura da sub-janela"""
        JanelaDuasAmostras(self)

    def executar_teste(self) -> None:
        try:
            amostra = self.obter_amostra()
            estimador = Estimador(amostra)
            estimador.mostrar_valores()

            mu0 = float(self.entry_mu0.get())
            alpha = float(self.entry_alpha.get())
            mu1 = float(self.entry_mu1.get())

            if int(self.entry_n_cco.get()) <= 0:
                n_cco = estimador.n
            else:
                n_cco = int(self.entry_n_cco.get())

            tipo = self.tipo_teste.get()
            tipo_grafico = self.tipo_grafico.get()

            if tipo == "bilateral":
                valor_p = estimador.valor_p_bilateral(mu0)
                beta = estimador.beta_bilateral(mu0, mu1, alpha, estimador.erro_padrao)
                descricao = f"H0: μ = {mu0}\nH1: μ ≠ {mu0}"
            elif tipo == "unilateral à direita":
                valor_p = estimador.valor_p_unilateral_maior(mu0)
                beta = estimador.beta_unilateral_maior(mu0, mu1, alpha, estimador.erro_padrao)
                descricao = f"H0: μ = {mu0}\nH1: μ > {mu0}"
            else:
                valor_p = estimador.valor_p_unilateral_menor(mu0)
                beta = estimador.beta_unilateral_menor(mu0, mu1, alpha, estimador.erro_padrao)
                descricao = f"H0: μ = {mu0}\nH1: μ < {mu0}"

            estatistica = estimador.z_escore(mu0)
            rejeita = valor_p < alpha

            resultado = ["=== Estatísticas da Amostra ===", f"n = {estimador.n}",
                         f"Média = {estimador.media_amostral:.6f}", f"Desvio padrão = {estimador.desvio_padrao_amostral:.6f}",
                         f"Erro padrão = {estimador.erro_padrao:.6f}", f"Variância = {estimador.variancia_amostral:.6f}",
                         "\n=== Hipóteses ===", descricao, "\n=== Resultado ===", f"Estatística de teste = {estatistica:.6f}",
                         f"Valor-p = {valor_p:.6f}", f"α = {alpha:.6f}", "\n=== Valores críticos ===",
                         f"Valor crítico bilateral = {estimador.valor_critico_bilateral(alpha):.6f}\nValor crítico unilateral à direita = {estimador.valor_critico_unilateral_maior(alpha):.6f}\nValor crítico unilateral à esquerda = {estimador.valor_critico_unilateral_menor(alpha):.6f}",
                         "\n=== Erro Tipo II e Poder ===", f"μ₁ = {mu1:.6f}", f"β = {beta:.6f}\n"]

            if rejeita:
                resultado.append("Conclusão: Rejeitar H0")
            else:
                resultado.append("Conclusão: Não rejeitar H0")

            self.txt_resultado.delete("1.0", END)
            self.txt_resultado.insert(END, "\n".join(resultado))

            mostrar_grafico(estimador, alpha, mu0, n_cco, tipo_grafico)

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))


if __name__ == "__main__":
    Aplicacao().mainloop()