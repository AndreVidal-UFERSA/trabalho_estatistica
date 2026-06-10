from tkinter import *
from tkinter import ttk, messagebox

from Estimador import Estimador
from graficos import mostrar_grafico


class Aplicacao(Tk):
    def __init__(self):
        """
        Inicializa a janela principal da aplicação, definindo o título,
        o tamanho inicial da tela e disparando a construção dos elementos visuais.
        """
        super().__init__()

        self.title("Teste de Hipótese")
        self.geometry("700x500")

        # Chama o método responsável por renderizar a interface do usuário (UI)
        self.criar_widgets()

    def criar_widgets(self) -> None:
        """
        Cria, configura e posiciona todos os componentes visuais (widgets)
        da interface usando gerenciadores de layout (pack e grid).
        """

        # --- SEÇÃO 1: CAMPO DE ENTRADA DA AMOSTRA ---
        Label(
            self,
            text="Amostra (números separados por vírgula ou espaço)"
        ).pack(pady=(10, 0))

        # Caixa de texto multilinha para suportar grandes volumes de dados da amostra
        self.txt_amostra = Text(self, height=5)
        self.txt_amostra.pack(fill=X, padx=10)

        # --- SEÇÃO 2: PARÂMETROS DO TESTE (GRID LOGÍSTICO) ---
        # Frame utilizado para agrupar e organizar os campos numéricos lado a lado
        frame_hipotese = Frame(self)
        frame_hipotese.pack(fill=X, padx=10, pady=10)

        # Campo: Média sob a hipótese nula (μ₀)
        Label(frame_hipotese, text="Média da hipótese (μ₀):").grid(
            row=0,
            column=0,
            sticky=W
        )

        self.entry_mu0 = Entry(frame_hipotese)
        self.entry_mu0.grid(row=0, column=1, padx=5)

        # Campo: Nível de significância do teste (α)
        Label(frame_hipotese, text="α:").grid(
            row=0,
            column=2,
            sticky=W
        )

        self.entry_alpha = Entry(frame_hipotese)
        self.entry_alpha.insert(0, "0.05") # Define 5% como o padrão estatístico comum
        self.entry_alpha.grid(row=0, column=3, padx=5)

        # Campo: Média alternativa (μ₁) para cálculo do Erro Tipo II (Beta)
        Label(frame_hipotese, text="μ₁:").grid(
            row=0,
            column=4,
            sticky=W
        )

        self.entry_mu1 = Entry(frame_hipotese)
        self.entry_mu1.grid(
            row=0,
            column=5,
            padx=5
        )

        # Campo: Tamanho amostral customizado para simulação nas curvas CCO
        Label(frame_hipotese, text="n do cco:").grid(
            row=0,
            column=6,
            sticky=W
        )

        self.entry_n_cco = Entry(frame_hipotese)
        self.entry_n_cco.grid(
            row=0,
            column=7,
            padx=5
        )

        # --- SEÇÃO 3: SELEÇÃO DE TIPOS DE TESTE E GRÁFICOS ---
        # Rótulo e Combobox para a cauda do teste estatístico
        Label(frame_hipotese, text="Tipo de teste:").grid(
            row=1,
            column=0,
            sticky=W,
            pady=10
        )

        self.tipo_teste = StringVar(value="bilateral")
        self.tipo_grafico = StringVar(value="bilateral")

        ttk.Combobox(
            frame_hipotese,
            textvariable=self.tipo_teste,
            state="readonly",
            values=[
                "bilateral",
                "unilateral à direita",
                "unilateral à esquerda"
            ]
        ).grid(row=1, column=1, columnspan=2, sticky=W)

        # Rótulo e Combobox para determinar o comportamento do Quadrante [1, 0] do Matplotlib
        Label(frame_hipotese, text="Tipo de gráfico:").grid(
            row=1,
            column=3,
            sticky=W,
            pady=10
        )

        ttk.Combobox(
            frame_hipotese,
            textvariable=self.tipo_grafico,
            state="readonly",
            values=[
                "bilateral",
                "histograma",
            ]
        ).grid(row=1, column=4, columnspan=2, sticky=W)

        # --- SEÇÃO 4: BOTÃO DE DISPARO ---
        # Botão principal que aciona o motor de cálculos estatísticos e plotagem
        Button(
            self,
            text="Executar Teste",
            command=self.executar_teste
        ).pack(pady=10)

        # --- SEÇÃO 5: VISUALIZAÇÃO DO RELATÓRIO ---
        Label(self, text="Resultado").pack()

        # Área de texto protegida que exibirá o relatório detalhado formatado
        self.txt_resultado = Text(self, height=15)
        self.txt_resultado.pack(
            fill=BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    def obter_amostra(self) -> list[float]:
        """
        Extrai o texto bruto digitado pelo usuário, limpa e padroniza os delimitadores
        (espaços ou vírgulas) e converte o resultado em uma lista de floats estruturada.
        """
        # Captura todo o texto contido na caixa do início (1.0) até o fim (END)
        texto = self.txt_amostra.get("1.0", END)

        # Permite separar valores por vírgula ou espaço substituindo vírgulas por espaços simples
        texto = texto.replace(",", " ")

        # Divide a string e gera a lista via list comprehension ignorando espaços extras
        return [
            float(valor)
            for valor in texto.split()
        ]

    def executar_teste(self) -> None:
        """
        Gerenciador central do teste de hipótese. Controla o fluxo de captura de dados,
        processamento matemático via classe Estimador, formatação do relatório textual
        no widget Tkinter e renderização da janela de gráficos.
        """
        try:
            # Obtém a amostra informada pelo usuário
            amostra = self.obter_amostra()

            # Cria o objeto responsável pelos cálculos estatísticos descritivos e inferenciais
            estimador = Estimador(amostra)

            # Exibe os valores no terminal para depuração
            estimador.mostrar_valores()

            # Leitura e conversão dos parâmetros quantitativos informados na UI
            mu0 = float(self.entry_mu0.get())
            alpha = float(self.entry_alpha.get())
            mu1 = float(self.entry_mu1.get())

            # Caso o usuário informe um valor inválido ou zerado/negativo,
            # utiliza o tamanho padrão da amostra coletada (estimador.n)
            if int(self.entry_n_cco.get()) <= 0:
                n_cco = estimador.n
            else:
                n_cco = int(self.entry_n_cco.get())

            # Captura as strings de configuração selecionadas nos Comboboxes
            tipo = self.tipo_teste.get()
            tipo_grafico = self.tipo_grafico.get()

            # --- PROCESSAMENTO CONDICIONAL DO MODELO MATEMÁTICO ---
            # Seleciona o tipo de teste e calcula valor-p e erro tipo II correspondentes
            if tipo == "bilateral":
                valor_p = estimador.valor_p_bilateral(mu0)

                beta = estimador.beta_bilateral(
                    mu0,
                    mu1,
                    alpha
                )

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ ≠ {mu0}"
                )

            elif tipo == "unilateral à direita":
                valor_p = estimador.valor_p_unilateral_maior(mu0)

                beta = estimador.beta_unilateral_maior(
                    mu0,
                    mu1,
                    alpha
                )

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ > {mu0}"
                )

            else:
                valor_p = estimador.valor_p_unilateral_menor(mu0)

                beta = estimador.beta_unilateral_menor(
                    mu0,
                    mu1,
                    alpha
                )

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ < {mu0}"
                )

            # Estatística de teste padronizada (Z-score ou t-score aproximado)
            estatistica = estimador.z_escore(mu0)

            # Critério de Decisão Estatística: Rejeita H0 se o valor-p for estritamente menor que alfa
            rejeita = valor_p < alpha

            # --- CONSTRUÇÃO DO CORPO TEXTUAL DO RELATÓRIO ---
            resultado = []

            # Bloco 1: Métricas descritivas observadas
            resultado.append("=== Estatísticas da Amostra ===")
            resultado.append(f"n = {estimador.n}")
            resultado.append(
                f"Média = {estimador.media_amostral:.6f}"
            )
            resultado.append(
                f"Desvio padrão = {estimador.desvio_padrao_amostral:.6f}"
            )
            resultado.append(
                f"Erro padrão = {estimador.erro_padrao:.6f}"
            )
            resultado.append(
                f"Variância = {estimador.variancia_amostral:.6f}"
            )

            # Bloco 2: Definição formal das hipóteses do teste em execução
            resultado.append("")
            resultado.append("=== Hipóteses ===")
            resultado.append(descricao)

            # Bloco 3: Evidências estatísticas e nível de significância crítico
            resultado.append("")
            resultado.append("=== Resultado ===")
            resultado.append(
                f"Estatística de teste = {estatistica:.6f}"
            )
            resultado.append(
                f"Valor-p = {valor_p:.6f}"
            )
            resultado.append(
                f"α = {alpha:.6f}"
            )

            # Bloco 4: Fronteiras de corte teóricas para consulta do analista
            resultado.append("")
            resultado.append("=== Valores críticos ===")
            resultado.append(
                f"Valor crítico bilateral = {estimador.valor_critico_bilateral(alpha):.6f}"
                f"\nValor crítico unilateral à direita = {estimador.valor_critico_unilateral_maior(alpha):.6f}"
                f"\nValor crítico unilateral à esquerda = {estimador.valor_critico_unilateral_menor(alpha):.6f}"
            )

            # Bloco 5: Probabilidade do erro de segunda espécie (Beta) e Poder do teste para μ₁
            resultado.append("")
            resultado.append("=== Erro Tipo II e Poder ===")
            resultado.append(
                f"μ₁ = {mu1:.6f}"
            )
            resultado.append(
                f"β = {beta:.6f}"
            )

            resultado.append("")

            # Bloco 6: Veredito e inferência baseados no critério de rejeição
            if rejeita:
                resultado.append(
                    "Conclusão: Rejeitar H0"
                )
            else:
                resultado.append(
                    "Conclusão: Não rejeitar H0"
                )

            # --- ATUALIZAÇÃO DA INTERFACE GRÁFICA (SAÍDA) ---
            # Limpa qualquer resíduo de relatórios anteriores do campo de texto
            self.txt_resultado.delete("1.0", END)
            # Insere a nova string construída unindo os elementos da lista com quebras de linha
            self.txt_resultado.insert(
                END,
                "\n".join(resultado)
            )

            # Dispara a sub-rotina do matplotlib para renderizar os 4 quadrantes analíticos
            mostrar_grafico(
                estimador,
                alpha,
                mu0,
                n_cco,
                tipo_grafico
            )

        except Exception as erro:
            # Captura falhas de digitação, divisão por zero ou conversões inválidas, 
            # exibindo em uma caixa de diálogo segura do sistema operacional
            messagebox.showerror(
                "Erro",
                str(erro)
            )


if __name__ == "__main__":
    # Ponto de entrada do script: instancia o loop de eventos infinito do Tkinter
    Aplicacao().mainloop()