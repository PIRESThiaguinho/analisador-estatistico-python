# Analisador Estatístico — Engenharia de Software

Trabalho da disciplina **Probabilidade e Estatística**. Aplicação de linha de comando (CLI) em Python para analisar dados numéricos por três métodos: dados não agrupados, distribuição discreta de frequências e distribuição por intervalos de classe.

## Requisitos
- Python 3.10 ou superior.
- Nenhuma dependência externa.
- Na Parte 1, utiliza `statistics.mean`, `statistics.median` e `statistics.mode`.
- Na Parte 3, as fórmulas são implementadas com Python nativo, sem `statistics`, NumPy, Pandas ou SciPy para os cálculos agrupados.

## Como executar
1. Instale o Python 3.
2. Abra um terminal na pasta do projeto.
3. Execute:
   ```bash
   python analisador.py
   ```
4. Escolha `1` para digitar os dados separados por vírgula ou `2` para carregar um CSV.
5. Para testar rapidamente, digite: `2, 3, 3, 4, 5, 6, 7, 7, 8, 9`.

## Formato CSV
O programa aceita números em arquivo `.csv`, inclusive separados por vírgula ou ponto e vírgula. Cabeçalhos textuais simples são ignorados antes do primeiro valor numérico. É recomendado usar uma coluna com valores numéricos, por exemplo:

```csv
valor
12
15
18
20
20
25
```

## Organização
- `analisador.py`: funções de entrada, tabela de frequências e cálculos estatísticos.
- `relatorio_tecnico.pdf`: relatório explicativo do projeto.

## Fórmulas implementadas
- Sturges: `k = ceil(1 + 3,322 log10(n))`.
- Amplitude de classe: `h = (máximo - mínimo) / k`.
- Média agrupada: soma dos pontos médios multiplicados pelas frequências, dividida por `n`.
- Mediana e separatrizes: `L + ((posição - F_anterior) / f_classe) * h`.
- Moda agrupada (Czuber): `L + ((f1 - f0) / ((f1 - f0) + (f1 - f2))) * h`.

## Observações importantes
Resultados agrupados são estimativas por interpolação e podem diferir dos cálculos feitos com os dados individuais. O programa usa limites inferiores inclusivos e superiores exclusivos, exceto o limite superior da última classe, que é inclusivo para garantir que o maior valor seja contado. A escolha do número de classes e a convenção de interpolação podem variar conforme o critério ensinado pelo professor; confirme se a turma adotou exatamente a regra de Sturges e as fórmulas apresentadas aqui.
