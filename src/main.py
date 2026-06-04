from Estimador import Estimador

def main() -> None:
    print("Insira dados distribuidos normalmente separados por virgula")
    amostra = [float(s) for s in input().replace(" ", "").split(",")]
    estimador = Estimador(amostra)
    estimador.mostrar_valores()
    return

if __name__ == "__main__":
    main()
