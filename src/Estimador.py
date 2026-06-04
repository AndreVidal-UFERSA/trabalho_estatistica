import math
import statistics

class Estimador:
    def __init__(self, amostra: list[float]):
        self.amostra = amostra
        self.n = len(self.amostra)
        self.media = statistics.mean(amostra)
        self.desvio_padrao = statistics.stdev(self.amostra, self.media)
        self.variancia = self.desvio_padrao ** 2
        self.erro_padrao = self.desvio_padrao / math.sqrt(self.n)
    
    def mostrar_valores(self) -> None:
        print(f"n: {self.n}")
        print(f"Media: {self.media}")
        print(f"Desvio padrão: {self.desvio_padrao}")
        print(f"Variancia: {self.variancia}")
    
    def validar_hipotese_media_bilateral(self, media_hipotese: float, alpha: float = 0.05) -> bool:
        """
        H0 : \mu = media_hipotese
        H1 : \mu != media_hipotese
        """
        z_crit = statistics.NormalDist().inv_cdf(1 - alpha / 2)
        z = (self.media - media_hipotese) / self.erro_padrao
        return abs(z) <= z_crit
    
    def validar_hipotese_media_unilateral_maior(self, media_hipotese: float, alpha: float = 0.05) -> bool:
        """
        H0 : \mu = media_hipotese
        H1 : \mu > media_hipotese
        """
        z_crit = statistics.NormalDist().inv_cdf(1 - alpha)
        z = (self.media - media_hipotese) / self.erro_padrao
        return z <= z_crit
    
    def validar_hipotese_media_unilateral_menor(self, media_hipotese: float, alpha: float = 0.05) -> bool:
        """
        H0 : \\mu = media_hipotese
        H1 : \\mu < media_hipotese
        """
        z_crit = statistics.NormalDist().inv_cdf(alpha)
        z = (self.media - media_hipotese) / self.erro_padrao
        return z >= z_crit
