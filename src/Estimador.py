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
