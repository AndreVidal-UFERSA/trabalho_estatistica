import math
import statistics

import matplotlib.pyplot as plt
import numpy as np
from Estimador import Estimador

def mostrar_grafico(estimador: Estimador, alpha: float, mu0: float, n_cco: int) -> None:
    fig, ax = plt.subplots(2, 2)

    # O intervalo de simulação das alternativas deve orbitar a hipótese testada (mu0)
    mus = np.linspace(mu0, mu0 + 5 * estimador.erro_padrao, 200)
    betas = []

    # Para mostrar o efeito do tamanho da amostra, podemos calcular o beta para diferentes tamanhos de amostra
    tamanhos_n = [max(2, n_cco // 2),n_cco, n_cco * 2]

    for mu in mus:
        beta = estimador.beta_unilateral_maior(
            media_hipotese=mu0,
            media_alternativa=mu,
            alfa=alpha
        )

        betas.append(beta)
        
        print(f"μ={mu} -> β={beta}")

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

    chart_uni = ax[0, 1]
    chart_uni.set_title("Região de rejeição maior e menor")

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

    chart_uni.plot(
        x,
        y,
        linewidth=2,
        label="Normal estimada"
    )

    chart_uni.legend()

    x_hatch = x[x >= estimador.valor_critico_unilateral_maior(alpha) + mu0]
    y_hatch = y[x >= estimador.valor_critico_unilateral_maior(alpha) + mu0]

    chart_uni.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_unilateral_maior(alpha) + mu0:.6f}"
    )

    x_hatch = x[x <= estimador.valor_critico_unilateral_menor(alpha) + mu0]
    y_hatch = y[x <= estimador.valor_critico_unilateral_menor(alpha) + mu0]

    chart_uni.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_unilateral_menor(alpha) + mu0:.6f}"
    )

    chart_uni.legend()

    chart_bil = ax[1, 0]
    chart_bil.set_title("Região de rejeição biliateral")

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

    chart_bil.plot(
        x,
        y,
        linewidth=2,
        label="Normal estimada"
    )

    chart_bil.legend()

    x_hatch = x[x >= estimador.valor_critico_bilateral(alpha) + mu0]
    y_hatch = y[x >= estimador.valor_critico_bilateral(alpha) + mu0]

    chart_bil.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_bilateral(alpha) + mu0:.6f}"
    )

    x_hatch = x[x <= estimador.valor_critico_bilateral(alpha) * -1 + mu0]
    y_hatch = y[x <= estimador.valor_critico_bilateral(alpha) * -1 + mu0]

    chart_bil.fill_between(
        x_hatch,
        y_hatch,
        0,
        hatch='///',
        alpha=0.3,
        edgecolor='black',
        label=f"Região de rejeição em {estimador.valor_critico_bilateral(alpha)*-1 + mu0:.6f}"
    )

    chart_bil.legend()

    cco = ax[1, 1]

    cco.set_title("CCO")

    for n_teste in tamanhos_n:
        erro_padrao_simulado = estimador.desvio_padrao_amostral / math.sqrt(n_teste)
        
        betas_n = []
        for mu in mus:
            z_critico = statistics.NormalDist().inv_cdf(1 - alpha)
            ponto_corte = mu0 + (z_critico * erro_padrao_simulado)
            z_beta = (ponto_corte - mu) / erro_padrao_simulado
            betas_n.append(statistics.NormalDist().cdf(z_beta))
            
        # O Matplotlib vai plotar uma linha de cada cor automaticamente para cada n
        cco.plot(mus, betas_n, label=f"n = {n_teste}")
    
    cco.set_xlabel("μ")
    cco.set_ylabel("β")
    cco.set_xlim(mu0, mus[mus.size - 1])

    cco.grid(True, linestyle=":", alpha=0.6)

    cco.legend()

    plt.tight_layout()
    plt.show()
    