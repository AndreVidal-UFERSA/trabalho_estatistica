from Estimador import Estimador

def main() -> None:
    print("Insira dados distribuidos normalmente separados por virgula")
    amostra = [float(s) for s in input().replace(" ", "").split(",")]
    estimador = Estimador(amostra)
    estimador.mostrar_valores()
    media_hipotese = float(input("Insira uma media hipotetica: "))
    valor_p = estimador.valor_p_bilateral(media_hipotese)
    print(f"Valor-p da hipótese H0 : \\mu = {media_hipotese} => {valor_p}")
    alfa = float(input("Insira o valor de alfa: "))
    if valor_p < alfa:
        print("Rejeitada")
    else:
        print("Aceita")
    return

if __name__ == "__main__":
    main()
