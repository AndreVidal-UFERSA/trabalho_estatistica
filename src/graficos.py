import matplotlib.pyplot as plt
import numpy as np
from Estimador import Estimador

def mostrar_grafico(estimador: Estimador, alpha: float) -> None:
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

    histogram = ax[0, 1]
    histogram.set_title("Região de rejeição maior e menor")

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

    x_hatch = x[x >= estimador.valor_critico_unilateral_maior(alpha)]
    y_hatch = y[x >= estimador.valor_critico_unilateral_maior(alpha)]

    histogram.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_unilateral_maior(alpha):.6f}"
    )

    x_hatch = x[x <= estimador.valor_critico_unilateral_menor(alpha)]
    y_hatch = y[x <= estimador.valor_critico_unilateral_menor(alpha)]

    histogram.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_unilateral_menor(alpha):.6f}"
    )

    histogram.legend()

    histogram = ax[1, 0]
    histogram.set_title("Região de rejeição biliateral")

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

    x_hatch = x[x >= estimador.valor_critico_bilateral(alpha)]
    y_hatch = y[x >= estimador.valor_critico_bilateral(alpha)]

    histogram.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_bilateral(alpha):.6f}"
    )

    x_hatch = x[x <= estimador.valor_critico_bilateral(alpha) * -1]
    y_hatch = y[x <= estimador.valor_critico_bilateral(alpha) * -1]

    histogram.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_bilateral(alpha)*-1:.6f}"
    )

    histogram.legend()

    plt.tight_layout()
    plt.show()
    