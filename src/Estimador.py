import math
import statistics

class Estimador:
    def __init__(self, amostra: list[float]):
        """
        Inicializa o objeto Estimador, responsável pelo cálculo de estatísticas descritivas
        e inferenciais. Requer uma lista de números reais contendo pelo menos duas observações.
        """
        # Validação obrigatória para viabilizar o cálculo do desvio padrão amostral (graus de liberdade n - 1)
        if (len(amostra) < 2):
            raise ValueError("A amostra deve conter pelo menos duas observações")
        
        self.amostra = amostra
        
        # --- ESTATÍSTICAS DESCRITIVAS BÁSICAS DA AMOSTRA ---
        self.n = len(self.amostra) # Tamanho total da amostra
        self.media_amostral = statistics.mean(amostra) # Média aritmética dos elementos
        
        # Desvio padrão amostral utilizando n - 1 no denominador (Correção de Bessel)
        self.desvio_padrao_amostral = statistics.stdev(self.amostra, self.media_amostral)
        
        # Variância amostral (quadrado do desvio padrão)
        self.variancia_amostral = self.desvio_padrao_amostral ** 2
        
        # Erro padrão da média: quantifica a variabilidade esperada das médias amostrais
        self.erro_padrao = self.desvio_padrao_amostral / math.sqrt(self.n)
    
    def mostrar_valores(self) -> None:
        """
        Imprime os parâmetros resumidos da amostra diretamente no console do sistema.
        """
        print(f"n: {self.n}")
        print(f"Media amostral: {self.media_amostral}")
        print(f"Desvio padrão amostral: {self.desvio_padrao_amostral}")
        print(f"Variancia amostral: {self.variancia_amostral}")
        print(f"Erro padrão: {self.erro_padrao}")
    
    # --- MÉTODOS ESTÁTICOS: VALORES CRÍTICOS Z (DISTRIBUIÇÃO NORMAL PADRÃO) ---
    @staticmethod
    def valor_critico_bilateral(alfa: float) -> float:
        """
        Retorna o escore Z crítico para um teste bilateral, onde a área alfa é dividida igualmente 
        nas duas caudas da curva normal. Utiliza a função inversa da CDF.
        """
        return statistics.NormalDist().inv_cdf(1 - alfa / 2) # Aproximação para varias amostras
    
    @staticmethod
    def valor_critico_unilateral_maior(alfa: float) -> float:
        """
        Retorna o escore Z crítico superior. Deixa uma área à direita na cauda superior 
        exatamente igual ao valor de alfa especificado.
        """
        return statistics.NormalDist().inv_cdf(1 - alfa) # Aproximação para varias amostras
    
    @staticmethod
    def valor_critico_unilateral_menor(alfa: float) -> float:
        """
        Retorna o escore Z crítico inferior. Deixa uma área à esquerda na cauda inferior
        exatamente igual ao valor de alfa especificado (gerando um valor negativo).
        """
        return statistics.NormalDist().inv_cdf(alfa) # Aproximação para varias amostras
    
    def z_escore(self, media_hipotese: float) -> float:
        """
        Calcula a estatística de teste (Z-score), que mede quantos erros padrões 
        a média observada está distante da média teórica estabelecida pela hipótese nula.
        """
        return (self.media_amostral - media_hipotese) / self.erro_padrao
    
    # --- PROCESSAMENTO DOS VALORES-P ---
    def valor_p_bilateral(self, media_hipotese: float) -> float:
        """
        H0 : \mu = media_hipotese
        H1 : \mu != media_hipotese
        Calcula o valor-p para um teste bilateral. Representa a probabilidade de obter um 
        Z-score tão extremo quanto o observado, em módulo, em ambas as direções da curva.
        """
        z_escore = abs(self.z_escore(media_hipotese))
        return 2 * (1 - statistics.NormalDist().cdf(z_escore))
    
    def valor_p_unilateral_maior(self, media_hipotese: float) -> float:
        """
        H0 : \mu = media_hipotese
        H1 : \mu > media_hipotese
        Calcula o valor-p para um teste unilateral à direita. Determina a probabilidade de encontrar 
        uma média amostral maior ou igual à observada sob as condições da hipótese nula.
        """
        z_escore = self.z_escore(media_hipotese)
        return 1 - statistics.NormalDist().cdf(z_escore)
    
    def valor_p_unilateral_menor(self, media_hipotese: float) -> float:
        """
        H0 : \mu = media_hipotese
        H1 : \mu < media_hipotese
        Calcula o valor-p para um teste unilateral à esquerda. Determina a probabilidade de encontrar 
        uma média amostral menor ou igual à observada sob as condições da hipótese nula.
        """
        z_escore = self.z_escore(media_hipotese)
        return statistics.NormalDist().cdf(z_escore)
    
    # --- CÁLCULO DO ERRO TIPO II (BETA) ---
    def beta_unilateral_maior(self, media_hipotese: float, media_alternativa: float, alfa: float, erro_padrao: float) -> float:
        """
        Calcula a probabilidade do Erro Tipo II (Beta) para um cenário unilateral à direita: 
        a probabilidade de não rejeitar H0 quando a hipótese alternativa (media_alternativa) é a verdadeira.
        """
        z_critico = self.valor_critico_unilateral_maior(alfa)
        # Transforma o ponto crítico da variável original de volta em uma unidade Z centrada em H1
        z_beta = (z_critico * erro_padrao - (media_alternativa - media_hipotese)) / erro_padrao
        return statistics.NormalDist().cdf(z_beta)
    

    def beta_unilateral_menor(self, media_hipotese: float, media_alternativa: float, alfa: float, erro_padrao: float) -> float:
        """
        Calcula a probabilidade do Erro Tipo II (Beta) para um cenário unilateral à esquerda:
        a probabilidade de falhar em rejeitar H0 dada uma média alternativa menor que a da hipótese nula.
        """
        z_critico = self.valor_critico_unilateral_menor(alfa) 
        # Calcula a posição da linha crítica sob a nova distribuição centrada na hipótese alternativa
        z_beta = (z_critico * erro_padrao - (media_alternativa - media_hipotese)) / erro_padrao
        return 1 - statistics.NormalDist().cdf(z_beta)
    
    def beta_bilateral(self, media_hipotese: float, media_alternativa: float, alfa: float, erro_padrao: float) -> float:
        """
        Calcula a probabilidade de cometer o Erro Tipo II (Beta) em testes bilaterais.
        Avalia a probabilidade acumulada contida entre os dois limites de aceitação críticos
        projetados e redefinidos sob a curva da média alternativa real.
        """
        # Captura os limites críticos das caudas superior e inferior baseados no alfa dividido por dois
        z_critico_superior = self.valor_critico_unilateral_maior(alfa / 2)
        z_critico_inferior = self.valor_critico_unilateral_menor(alfa / 2)
        
        # Reposiciona estatisticamente as fronteiras em escores Z baseados na distribuição alternativa real
        z_beta_superior = (z_critico_superior * erro_padrao - (media_alternativa - media_hipotese)) / erro_padrao
        z_beta_inferior = (z_critico_inferior * erro_padrao - (media_alternativa - media_hipotese)) / erro_padrao
        
        dist = statistics.NormalDist()
        # Subtrai a área da cauda inferior da área total acumulada até o limite superior para obter a região de aceitação (Beta)
        return dist.cdf(z_beta_superior) - dist.cdf(z_beta_inferior)

    @staticmethod
    def calculos_inferenciais(est_A: Estimador, est_B: Estimador, alpha: float) -> tuple[float,float,float]:
        diferenca = est_A.media_amostral - est_B.media_amostral
        erro_combinado = math.sqrt((est_A.variancia_amostral / est_A.n) + (est_B.variancia_amostral / est_B.n))
        z_calc = (diferenca - 0) / erro_combinado
        
        z_critico = statistics.NormalDist().inv_cdf(1 - alpha / 2)
        p_valor = 2 * (1 - statistics.NormalDist().cdf(abs(z_calc)))

        return p_valor, z_critico, z_calc