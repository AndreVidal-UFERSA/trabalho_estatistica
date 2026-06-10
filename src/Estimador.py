import math
import statistics

class Estimador:
    def __init__(self, amostra: list[float]):
        if (len(amostra) < 2):
            raise ValueError("A amostra deve conter pelo menos duas observações")
        self.amostra = amostra
        self.n = len(self.amostra)
        self.media_amostral = statistics.mean(amostra)
        self.desvio_padrao_amostral = statistics.stdev(self.amostra, self.media_amostral)
        self.variancia_amostral = self.desvio_padrao_amostral ** 2
        self.erro_padrao = self.desvio_padrao_amostral / math.sqrt(self.n)
    
    def mostrar_valores(self) -> None:
        print(f"n: {self.n}")
        print(f"Media amostral: {self.media_amostral}")
        print(f"Desvio padrão amostral: {self.desvio_padrao_amostral}")
        print(f"Variancia amostral: {self.variancia_amostral}")
        print(f"Erro padrão: {self.erro_padrao}")
    
    @staticmethod
    def valor_critico_bilateral(alfa: float) -> float:
        return statistics.NormalDist().inv_cdf(1 - alfa / 2) # Aproximação para varias amostras
    
    @staticmethod
    def valor_critico_unilateral_maior(alfa: float) -> float:
        return statistics.NormalDist().inv_cdf(1 - alfa) # Aproximação para varias amostras
    
    @staticmethod
    def valor_critico_unilateral_menor(alfa: float) -> float:
        return statistics.NormalDist().inv_cdf(alfa) # Aproximação para varias amostras
    
    def z_escore(self, media_hipotese: float) -> float:
        return (self.media_amostral - media_hipotese) / self.erro_padrao
    
    def valor_p_bilateral(self, media_hipotese: float) -> float:
        """
        H0 : \\mu = media_hipotese
        H1 : \\mu != media_hipotese
        """
        z_escore = abs(self.z_escore(media_hipotese))
        return 2 * (1 - statistics.NormalDist().cdf(z_escore))
    
    def valor_p_unilateral_maior(self, media_hipotese: float) -> float:
        """
        H0 : \\mu = media_hipotese
        H1 : \\mu > media_hipotese
        """
        z_escore = self.z_escore(media_hipotese)
        return 1 - statistics.NormalDist().cdf(z_escore)
    
    def valor_p_unilateral_menor(self, media_hipotese: float) -> float:
        """
        H0 : \\mu = media_hipotese
        H1 : \\mu < media_hipotese
        """
        z_escore = self.z_escore(media_hipotese)
        return statistics.NormalDist().cdf(z_escore)
    
    def beta_unilateral_maior(self, media_hipotese: float, media_alternativa: float, alfa: float) -> float:
        z_critico = self.valor_critico_unilateral_maior(alfa)
        z_beta = (z_critico * self.erro_padrao - (media_alternativa - media_hipotese)) / self.erro_padrao
        return statistics.NormalDist().cdf(z_beta)
    

    def beta_unilateral_menor(self, media_hipotese: float, media_alternativa: float, alfa: float) -> float:
        z_critico = self.valor_critico_unilateral_menor(alfa) 
        z_beta = (z_critico * self.erro_padrao - (media_alternativa - media_hipotese)) / self.erro_padrao
        return 1 - statistics.NormalDist().cdf(z_beta)
    
    def beta_bilateral(self, media_hipotese: float, media_alternativa: float, alfa: float) -> float:
        z_critico_superior = self.valor_critico_unilateral_maior(alfa / 2)
        z_critico_inferior = self.valor_critico_unilateral_menor(alfa / 2)
        
        z_beta_superior = (z_critico_superior * self.erro_padrao - (media_alternativa - media_hipotese)) / self.erro_padrao
        z_beta_inferior = (z_critico_inferior * self.erro_padrao - (media_alternativa - media_hipotese)) / self.erro_padrao
        
        dist = statistics.NormalDist()
        return dist.cdf(z_beta_superior) - dist.cdf(z_beta_inferior)
        
