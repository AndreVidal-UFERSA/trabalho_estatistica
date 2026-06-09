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
        """
        β para:
        H0: μ = media_hipotese
        H1: μ > media_hipotese
        """

        z_critico = self.valor_critico_unilateral_maior(alfa)

        ponto_critico = (
            media_hipotese
            + z_critico * self.erro_padrao
        )

        z = (
            ponto_critico - media_alternativa
        ) / self.erro_padrao

        return statistics.NormalDist().cdf(z)


    def beta_unilateral_menor(
        self,
        media_hipotese: float,
        media_alternativa: float,
        alfa: float
    ) -> float:
        """
        β para:
        H0: μ = media_hipotese
        H1: μ < media_hipotese
        """

        z_critico = self.valor_critico_unilateral_menor(alfa)

        ponto_critico = (
            media_hipotese
            + z_critico * self.erro_padrao
        )

        z = (
            ponto_critico - media_alternativa
        ) / self.erro_padrao

        return 1 - statistics.NormalDist().cdf(z)


    def beta_bilateral(
        self,
        media_hipotese: float,
        media_alternativa: float,
        alfa: float
    ) -> float:
        """
        β para:
        H0: μ = media_hipotese
        H1: μ != media_hipotese
        """

        z_critico = self.valor_critico_bilateral(alfa)

        limite_inferior = (
            media_hipotese
            - z_critico * self.erro_padrao
        )

        limite_superior = (
            media_hipotese
            + z_critico * self.erro_padrao
        )

        normal = statistics.NormalDist(
            mu=media_alternativa,
            sigma=self.erro_padrao
        )

        return (
            normal.cdf(limite_superior)
            - normal.cdf(limite_inferior)
        )


    def poder_unilateral_maior(
        self,
        media_hipotese: float,
        media_alternativa: float,
        alfa: float
    ) -> float:
        return 1 - self.beta_unilateral_maior(
            media_hipotese,
            media_alternativa,
            alfa
        )


    def poder_unilateral_menor(
        self,
        media_hipotese: float,
        media_alternativa: float,
        alfa: float
    ) -> float:
        return 1 - self.beta_unilateral_menor(
            media_hipotese,
            media_alternativa,
            alfa
        )


    def poder_bilateral(
        self,
        media_hipotese: float,
        media_alternativa: float,
        alfa: float
    ) -> float:
        return 1 - self.beta_bilateral(
            media_hipotese,
            media_alternativa,
            alfa
        )
