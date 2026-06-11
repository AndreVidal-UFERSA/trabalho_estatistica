import math
import statistics

import matplotlib.pyplot as plt
import numpy as np
from Estimador import Estimador

def mostrar_grafico_duas_amostras(est_A, est_B, alpha=0.05):
    """
    Gera a Curva Característica de Operação (CCO) para o teste de duas amostras independentes.
    Mostra o Erro Tipo II (Beta) em função da verdadeira diferença entre as médias.
    """
    # 1. Calcula o erro padrão combinado real das duas amostras
    erro_combinado = np.sqrt((est_A.variancia_amostral / est_A.n) + (est_B.variancia_amostral / est_B.n))
    
    # 2. Encontra o valor crítico Z para um teste bilateral
    z_critico = statistics.NormalDist().inv_cdf(1 - alpha / 2)
    
    # 3. Cria um intervalo de possíveis diferenças reais entre as médias (Eixo X do gráfico)
    # Vamos cobrir desde uma diferença de -6 até +6 para o gráfico ficar amplo
    valores_diferenca_real = np.linspace(-6, 6, 500)
    
    # 4. Calcula o Beta para cada uma dessas diferenças reais
    betas = []
    dist_normal = statistics.NormalDist(mu=0, sigma=1)
    
    for d in valores_diferenca_real:
        # Fórmula teórica do Beta para duas amostras (bilateral)
        termo_superior = z_critico - (d / erro_combinado)
        termo_inferior = -z_critico - (d / erro_combinado)
        
        beta_d = dist_normal.cdf(termo_superior) - dist_normal.cdf(termo_inferior)
        betas.append(beta_d)
        
    # 5. Descobre a posição da nossa diferença amostral observada no gráfico
    diferenca_observada = est_A.media_amostral - est_B.media_amostral # 50 - 52 = -2.0
    termo_sup_obs = z_critico - (diferenca_observada / erro_combinado)
    termo_inf_obs = -z_critico - (diferenca_observada / erro_combinado)
    beta_observado = dist_normal.cdf(termo_sup_obs) - dist_normal.cdf(termo_inf_obs)

    # 6. Construção do Gráfico CCO usando Matplotlib
    plt.figure("Curva Característica de Operação (CCO)", figsize=(10, 6))
    
    plt.plot(valores_diferenca_real, betas, color="purple", linewidth=2.5, label="Curva CCO ($\beta$)")
    plt.fill_between(valores_diferenca_real, betas, color="purple", alpha=0.1)
    
    # Ponto marcador indicando o cenário atual da sua amostra (Diferença de -2.0)
    plt.plot(diferenca_observada, beta_observado, "ro", markersize=8, 
             label=f"Sua Amostra ($\Delta$ = {diferenca_observada:.2f}, $\beta$ = {beta_observado:.4f})")
    
    # Linhas guias tracejadas apontando para o nosso ponto
    plt.axvline(diferenca_observada, color="red", linestyle=":", alpha=0.7)
    plt.axhline(beta_observado, color="red", linestyle=":", alpha=0.7)
    
    # Títulos e formatação
    plt.title("Curva Característica de Operação (CCO) - Duas Amostras", fontsize=14, pad=15)
    plt.xlabel("Verdadeira Diferença entre as Médias ($\mu_A - \mu_B$)", fontsize=12)
    plt.ylabel("Probabilidade de Erro Tipo II ($\beta$)", fontsize=12)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(fontsize=11, loc="upper right")
    
    plt.tight_layout()
    plt.show()

def mostrar_grafico(estimador: Estimador, alpha: float, mu0: float, n_cco: int, tipo_grafico: str) -> None:
    """
    Gera uma matriz de gráficos 2x2 para análise estatística da amostra e dos testes de hipótese.
    Inclui curvas normais com regiões de rejeição, histogramas e Curvas Características de Operação (CCO).
    """
    # Inicializa a matriz de subplots 2x2 para renderizar os 4 gráficos simultaneamente
    fig, ax = plt.subplots(2, 2)

    # O intervalo de simulação das alternativas deve orbitar a hipótese testada (mu0)
    # Gera 200 pontos de médias alternativas (μ) partindo de μ0 até 5 erros padrões acima
    mus = np.linspace(mu0, mu0 + 5 * estimador.erro_padrao, 200)
    betas = []

    # Para mostrar o efeito do tamanho da amostra, podemos calcular o beta para diferentes tamanhos de amostra
    # Define três tamanhos de amostra para comparação: metade de n_cco (mínimo 2), o próprio n_cco, e o dobro
    tamanhos_n = [max(2, n_cco // 2), n_cco, n_cco * 2]

    # Loop para simular o valor do erro Tipo II (beta) original para cada média alternativa (μ)
    for mu in mus:
        beta = estimador.beta_unilateral_maior(
            media_hipotese=mu0,
            media_alternativa=mu,
            alfa=alpha
        )

        betas.append(beta)
        
        print(f"μ={mu} -> β={beta}")

    # --- QUADRANTE [0, 1]: GRÁFICO DA REGIÃO DE REJEIÇÃO UNILATERAL (MAIOR E MENOR) ---
    chart_uni = ax[0, 1]
    chart_uni.set_title("Região de rejeição maior e menor")

    # Extrai os parâmetros estimados da amostra real para desenhar a curva de densidade de probabilidade
    mu = estimador.media_amostral
    sigma = estimador.desvio_padrao_amostral

    # Define o eixo X cobrindo 4 desvios padrões para a esquerda e para a direita da média
    x = np.linspace(
        mu - 4 * sigma,
        mu + 4 * sigma,
        500
    )

    # Equação matemática da densidade de probabilidade de uma distribuição Normal
    y = (
        1 / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    )

    # Plota a linha da distribuição normal estimada
    chart_uni.plot(
        x,
        y,
        linewidth=2,
        label="Normal estimada"
    )

    chart_uni.legend()

    # Filtra e preenche com hachuras a região de rejeição à direita (Unilateral Maior)
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

    # Filtra e preenche com hachuras a região de rejeição à esquerda (Unilateral Menor)
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

    # --- QUADRANTE [1, 0]: CONDICIONAL BASEADO NO TIPO DE GRÁFICO ---
    if tipo_grafico == "bilateral":
        # Se for bilateral, o quadrante [1, 0] exibe as duas caudas de rejeição simétricas
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

        # Filtra e hachura a cauda superior da rejeição bilateral (alfa / 2)
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

        # Filtra e hachura a cauda inferior da rejeição bilateral (alfa / 2 negativo)
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
    else:
        # Se não for bilateral, o quadrante [1, 0] exibe o Histograma da amostra confrontado com a Normal
        histogram = ax[1, 0]
        histogram.set_title("Histograma da amostra")

        # Plota as barras de frequência relativa (densidade) dos dados reais da amostra
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

        # Sobrepõe a curva normal teórica sobre o histograma real
        histogram.plot(
            x,
            y,
            linewidth=2,
            label="Normal estimada"
        )

        histogram.legend()

    # --- QUADRANTE [1, 1]: CURVA CARACTERÍSTICA DE OPERAÇÃO (CCO) - ERRO TIPO II (β) ---
    cco = ax[1, 1]
    cco.set_title("CCO")

    # Plota a curva CCO mostrando como a probabilidade beta varia em função de diferentes tamanhos de amostra (n)
    for n_teste in tamanhos_n:
        # Recalcula o erro padrão escalonado para o tamanho 'n' da simulação atual
        erro_padrao_simulado = estimador.desvio_padrao_amostral / math.sqrt(n_teste)
        
        betas_n = []
        for mu in mus:
            # Encontra o valor Z crítico unilateral para o alpha estabelecido
            z_critico = statistics.NormalDist().inv_cdf(1 - alpha)
            # Define a fronteira de corte em unidades da variável original
            ponto_corte = mu0 + (z_critico * erro_padrao_simulado)
            # Calcula o score Z para a hipótese alternativa μ sob avaliação
            z_beta = (ponto_corte - mu) / erro_padrao_simulado
            # Integra a probabilidade acumulada (CDF) para obter o beta correspondente
            betas_n.append(statistics.NormalDist().cdf(z_beta))
            
        # O Matplotlib vai plotar uma linha de cada cor automaticamente para cada n
        cco.plot(mus, betas_n, label=f"n = {n_teste}")
    
    # Formatação dos eixos do gráfico CCO (Beta)
    cco.set_xlabel("μ")
    cco.set_ylabel("β")
    cco.set_xlim(mu0, mus[mus.size - 1])
    cco.grid(True, linestyle=":", alpha=0.6)
    cco.legend()

    # --- QUADRANTE [0, 0]: CURVA CARACTERÍSTICA DE OPERAÇÃO DO PODER DO TESTE (1 - β) ---
    # Sobrescreve a variável de referência 'cco' para apontar agora ao quadrante superior esquerdo
    cco = ax[0, 0]
    cco.set_title("CCO PODER")

    # Plota o Poder do Teste (1 - beta) em função das médias alternativas para cada 'n'
    for n_teste in tamanhos_n:
        # Recalcula o erro padrão escalonado para o tamanho 'n' da simulação atual
        erro_padrao_simulado = estimador.desvio_padrao_amostral / math.sqrt(n_teste)
        
        betas_n = []
        for mu in mus:
            z_critico = statistics.NormalDist().inv_cdf(1 - alpha)
            ponto_corte = mu0 + (z_critico * erro_padrao_simulado)
            z_beta = (ponto_corte - mu) / erro_padrao_simulado
            # Calcula o complemento da CDF, ou seja, a probabilidade de rejeitar H0 corretamente (Poder = 1 - beta)
            betas_n.append(1-(statistics.NormalDist().cdf(z_beta)))
            
        # O Matplotlib vai plotar uma linha de cada cor automaticamente para cada n
        cco.plot(mus, betas_n, label=f"n = {n_teste}")
    
    # Formatação dos eixos do gráfico CCO PODER
    cco.set_xlabel("μ")
    cco.set_ylabel("β") # Mantido idêntico ao original, mapeando o eixo Y do gráfico superior esquerdo
    cco.set_xlim(mu0, mus[mus.size - 1])
    cco.grid(True, linestyle=":", alpha=0.6)
    cco.legend()

    # Ajusta os espaçamentos automáticos dos subplots para evitar sobreposição de textos/títulos
    plt.tight_layout()
    # Exibe a janela gráfica final com as 4 visualizações geradas
    plt.show()