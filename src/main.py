from tkinter import *
from tkinter import ttk, messagebox

from Estimador import Estimador
from graficos import mostrar_grafico


class Aplicacao(Tk):
    def __init__(self):
        super().__init__()

        self.title("Teste de Hipótese")
        self.geometry("700x500")

        self.criar_widgets()

    def criar_widgets(self) -> None:
        Label(
            self,
            text="Amostra (números separados por vírgula ou espaço)"
        ).pack(pady=(10, 0))

        self.txt_amostra = Text(self, height=5)
        self.txt_amostra.pack(fill=X, padx=10)

        frame_hipotese = Frame(self)
        frame_hipotese.pack(fill=X, padx=10, pady=10)

        Label(frame_hipotese, text="Média da hipótese (μ₀):").grid(
            row=0,
            column=0,
            sticky=W
        )

        self.entry_mu0 = Entry(frame_hipotese)
        self.entry_mu0.grid(row=0, column=1, padx=5)

        Label(frame_hipotese, text="α:").grid(
            row=0,
            column=2,
            sticky=W
        )

        self.entry_alpha = Entry(frame_hipotese)
        self.entry_alpha.insert(0, "0.05")
        self.entry_alpha.grid(row=0, column=3, padx=5)

        Label(frame_hipotese, text="Tipo de teste:").grid(
            row=1,
            column=0,
            sticky=W,
            pady=10
        )

        self.tipo_teste = StringVar(value="bilateral")

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

        Button(
            self,
            text="Executar Teste",
            command=self.executar_teste
        ).pack(pady=10)

        Label(self, text="Resultado").pack()

        self.txt_resultado = Text(self, height=15)
        self.txt_resultado.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def obter_amostra(self) -> list[float]:
        texto = self.txt_amostra.get("1.0", END)

        texto = texto.replace(",", " ")

        return [
            float(valor)
            for valor in texto.split()
        ]

    def executar_teste(self) -> None:
        try:
            amostra = self.obter_amostra()

            estimador = Estimador(amostra)

            mostrar_grafico(estimador)

            mu0 = float(self.entry_mu0.get())
            alpha = float(self.entry_alpha.get())

            tipo = self.tipo_teste.get()

            if tipo == "bilateral":
                valor_p = estimador.valor_p_bilateral(mu0)

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ ≠ {mu0}"
                )

            elif tipo == "unilateral à direita":
                valor_p = estimador.valor_p_unilateral_maior(mu0)

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ > {mu0}"
                )

            else:
                valor_p = estimador.valor_p_unilateral_menor(mu0)

                descricao = (
                    f"H0: μ = {mu0}\n"
                    f"H1: μ < {mu0}"
                )

            estatistica = estimador.z_escore(mu0)

            rejeita = valor_p < alpha

            resultado = []

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

            resultado.append("")
            resultado.append("=== Hipóteses ===")
            resultado.append(descricao)

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

            resultado.append("")

            if rejeita:
                resultado.append(
                    "Conclusão: Rejeitar H0"
                )
            else:
                resultado.append(
                    "Conclusão: Não rejeitar H0"
                )

            self.txt_resultado.delete("1.0", END)
            self.txt_resultado.insert(
                END,
                "\n".join(resultado)
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )


if __name__ == "__main__":
    Aplicacao().mainloop()
