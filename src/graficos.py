import matplotlib.pyplot as plt
import numpy as np
from Estimador import Estimador

def mostrar_grafico(estimador: Estimador) -> None:
    fig, ax = plt.subplots(2, 2)

    histogram = ax[0, 0]
    histogram.set_title("Histograma da amostra")

    histogram.hist(
        estimador.amostra,
        density=True,
        bins="auto",
        alpha=0.7
    )

    mu = estimador.media_amostral
    sigma = estimador.desvio_padrao_amostral

    x = np.linspace(
        mu - 4 * sigma,
        mu + 4 * sigma,
        500
    )

    y = (
        1 / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    )

    histogram.plot(
        x,
        y,
        linewidth=2,
        label="Normal estimada"
    )

    histogram.legend()

    plt.tight_layout()
    plt.show()
    