"""
Analisador Estatístico - Engenharia de Software
Trabalho de Probabilidade e Estatística
Python 3.10+
"""

import csv
import math
import statistics
from collections import Counter


def ler_dados_terminal():
    """Lê números separados por vírgula digitados pelo usuário."""
    while True:
        entrada = input("Digite os dados separados por vírgula: ").strip()
        try:
            dados = [float(item.strip().replace(",", ".")) for item in entrada.split(";")] if ";" in entrada else [
                float(item.strip().replace(",", ".")) for item in entrada.split(",")
            ]
            if not dados:
                raise ValueError
            return dados
        except ValueError:
            print("Entrada inválida. Digite somente números separados por vírgula.")


def ler_csv():
    """Lê um CSV com uma coluna numérica ou vários valores numéricos."""
    caminho = input("Caminho do arquivo CSV: ").strip().strip('"')
    dados = []
    try:
        with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
            amostra = arquivo.read(4096)
            arquivo.seek(0)
            try:
                dialect = csv.Sniffer().sniff(amostra, delimiters=",;\\t")
            except csv.Error:
                dialect = csv.excel
            leitor = csv.reader(arquivo, dialect)
            for linha in leitor:
                for celula in linha:
                    valor = celula.strip().replace(",", ".")
                    if not valor:
                        continue
                    try:
                        dados.append(float(valor))
                    except ValueError:
                        # Permite cabeçalho textual, mas rejeita texto misturado a dados.
                        if not dados:
                            continue
                        raise ValueError(f"Valor não numérico encontrado no CSV: {celula}")
        if not dados:
            raise ValueError("O arquivo não contém números.")
        return dados
    except (OSError, UnicodeError, csv.Error, ValueError) as erro:
        print(f"Não foi possível carregar o arquivo: {erro}")
        return None


def formatar(x):
    return f"{x:.4f}"


def parte1(dados):
    """Tendência central com a biblioteca nativa statistics, conforme exigido."""
    print("\n" + "-" * 62)
    print("PARTE 1: DADOS NÃO AGRUPADOS (MÓDULO STATISTICS)")
    print("-" * 62)
    try:
        moda = statistics.mode(dados)
        print(f"Média:   {formatar(statistics.mean(dados))}")
        print(f"Mediana:  {formatar(statistics.median(dados))}")
        print(f"Moda:    {formatar(moda)}")
    except statistics.StatisticsError as erro:
        print(f"Não foi possível calcular: {erro}")


def construir_frequencias(dados):
    contagem = Counter(dados)
    valores = sorted(contagem)
    tabela = []
    acumulada = 0
    for valor in valores:
        fi = contagem[valor]
        acumulada += fi
        tabela.append((valor, fi, acumulada))
    return tabela


def mediana_por_frequencia(tabela, n):
    """Obtém a mediana usando as posições representadas pelas frequências."""
    posicoes = []
    for valor, fi, _ in tabela:
        posicoes.extend([valor] * fi)
    if n % 2:
        return posicoes[n // 2]
    return (posicoes[n // 2 - 1] + posicoes[n // 2]) / 2


def parte2(dados):
    """Estatísticas calculadas a partir da distribuição discreta de frequências."""
    print("\n" + "-" * 62)
    print("PARTE 2: DISTRIBUIÇÃO DE FREQUÊNCIA (SEM INTERVALO)")
    print("-" * 62)
    tabela = construir_frequencias(dados)
    print(f"{'Valor (xi)':>14} | {'Freq. Absoluta (fi)':>20} | {'Freq. Acumulada (Fi)':>21}")
    print("-" * 62)
    for xi, fi, Fi in tabela:
        print(f"{xi:14.4f} | {fi:20d} | {Fi:21d}")

    n = len(dados)
    soma_ponderada = sum(xi * fi for xi, fi, _ in tabela)
    media = soma_ponderada / n
    mediana = mediana_por_frequencia(tabela, n)
    maior_fi = max(fi for _, fi, _ in tabela)
    modas = [xi for xi, fi, _ in tabela if fi == maior_fi]
    moda = modas[0] if len(modas) == 1 else modas
    print("\nCalculados via tabela de frequências:")
    print(f"Média: {formatar(media)}")
    print(f"Mediana: {formatar(mediana)}")
    print(f"Moda(s): {moda}")
    return tabela


def sturges(n):
    """Número de classes pela regra de Sturges, arredondado para cima."""
    return max(1, math.ceil(1 + 3.322 * math.log10(n)))


def construir_classes(dados):
    minimo, maximo = min(dados), max(dados)
    k = sturges(len(dados))
    amplitude_total = maximo - minimo
    largura = amplitude_total / k if amplitude_total > 0 else 1.0
    classes = []
    for i in range(k):
        inferior = minimo + i * largura
        superior = minimo + (i + 1) * largura
        if i == k - 1:
            fi = sum(1 for x in dados if inferior <= x <= superior)
        else:
            fi = sum(1 for x in dados if inferior <= x < superior)
        classes.append({"li": inferior, "ls": superior, "fi": fi, "Fi": 0})
    acumulada = 0
    for classe in classes:
        acumulada += classe["fi"]
        classe["Fi"] = acumulada
    return classes, k, largura


def ponto_medio(classe):
    return (classe["li"] + classe["ls"]) / 2


def localizar_classe(classes, posicao):
    for i, classe in enumerate(classes):
        if classe["Fi"] >= posicao:
            return i
    return len(classes) - 1


def quantil_agrupado(classes, n, fracao):
    """Interpolação para quantis: L + ((posição - F anterior)/fi) * h."""
    posicao = fracao * n
    idx = localizar_classe(classes, posicao)
    classe = classes[idx]
    anterior = classes[idx - 1]["Fi"] if idx > 0 else 0
    if classe["fi"] == 0:
        return classe["li"]
    return classe["li"] + ((posicao - anterior) / classe["fi"]) * (classe["ls"] - classe["li"])


def media_agrupada(classes, n):
    return sum(ponto_medio(c) * c["fi"] for c in classes) / n


def mediana_agrupada(classes, n):
    return quantil_agrupado(classes, n, 0.5)


def moda_agrupada(classes):
    """Moda agrupada pelo método de Czuber."""
    idx = max(range(len(classes)), key=lambda i: classes[i]["fi"])
    classe = classes[idx]
    f1 = classe["fi"]
    f0 = classes[idx - 1]["fi"] if idx > 0 else 0
    f2 = classes[idx + 1]["fi"] if idx < len(classes) - 1 else 0
    h = classe["ls"] - classe["li"]
    denominador = (f1 - f0) + (f1 - f2)
    if denominador == 0:
        return ponto_medio(classe)
    return classe["li"] + ((f1 - f0) / denominador) * h


def parte3(dados):
    """Distribuição intervalar e fórmulas clássicas sem bibliotecas estatísticas."""
    print("\n" + "-" * 62)
    print("PARTE 3: DISTRIBUIÇÃO DE FREQUÊNCIA (COM INTERVALO)")
    print("-" * 62)
    classes, k, largura = construir_classes(dados)
    n = len(dados)
    print(f"n = {n} | mínimo = {min(dados):.4f} | máximo = {max(dados):.4f}")
    print(f"Regra de Sturges: k = ceil(1 + 3,322 log10(n)) = {k}")
    print(f"Amplitude total = {max(dados) - min(dados):.4f} | largura de classe = {largura:.4f}\n")
    print(f"{'Intervalo de Classe':>29} | {'fi':>6} | {'Fi':>6}")
    print("-" * 48)
    for i, c in enumerate(classes):
        fecha = "]" if i == len(classes) - 1 else ")"
        print(f"[{c['li']:.4f} - {c['ls']:.4f}{fecha:1} | {c['fi']:6d} | {c['Fi']:6d}")

    print("\nCalculados por fórmulas de dados agrupados:")
    print(f"Média:   {formatar(media_agrupada(classes, n))}")
    print(f"Mediana: {formatar(mediana_agrupada(classes, n))}")
    print(f"Moda (Czuber): {formatar(moda_agrupada(classes))}")
    print(f"Quartis: Q1 = {formatar(quantil_agrupado(classes, n, 0.25))} | "
          f"Q3 = {formatar(quantil_agrupado(classes, n, 0.75))}")
    print(f"Decis:   D2 = {formatar(quantil_agrupado(classes, n, 0.20))} | "
          f"D7 = {formatar(quantil_agrupado(classes, n, 0.70))}")
    print(f"Percentis: P15 = {formatar(quantil_agrupado(classes, n, 0.15))} | "
          f"P22 = {formatar(quantil_agrupado(classes, n, 0.22))} | "
          f"P63 = {formatar(quantil_agrupado(classes, n, 0.63))} | "
          f"P70 = {formatar(quantil_agrupado(classes, n, 0.70))}")


def main():
    print("=" * 62)
    print("ANALISADOR ESTATÍSTICO - ENGENHARIA DE SOFTWARE")
    print("=" * 62)
    print("[1] Inserir dados via terminal (separados por vírgula)")
    print("[2] Carregar arquivo .csv")
    opcao = input("Escolha a opção: ").strip()

    if opcao == "1":
        try:
            dados = ler_dados_terminal()
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
            return
    elif opcao == "2":
        dados = ler_csv()
        if dados is None:
            return
    else:
        print("Opção inválida.")
        return

    if len(dados) < 1:
        print("É necessário informar ao menos um número.")
        return

    parte1(dados)
    parte2(dados)
    parte3(dados)


if __name__ == "__main__":
    main()
