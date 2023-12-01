# Scatter-Search-MBT

## Parâmetros

Dentro do arquivo scatterSearch.cpp é possível mudar os paramêtros globais do algoritmo, como:

- Tamanho da População Inicial

` int TAMANHO_POPULACAO_INICIAL = 1000; `

- Tamanho do Conjunto de Referência

` int TAMANHO_POPULACAO_INICIAL = 1000; `

## Experimentos

Para selecionar os experimentos a serem realizados, basta manter as seguintes linhas descomentadas:

```
arquivos.push_back("Harari/H10_30");
...
arquivos.push_back("Harari/H9_30");

arquivos.push_back("SmallWorld/SW-100-3-0d1-trial1");
...
arquivos.push_back("SmallWorld/SW-1000-6-0d3-trial3");
```
## Compilção

Acessar o diretório de arquivos:

` Algoritimos > Scatter Search `

Em seguida, compilar o programa da seguinte maneira:

``` 
g++ scatterSearch.cpp -std=c++11 -O3
```

Em seguida, basta executar o executador gerado normalmente, sem nenhuma parâmetro de inicialização

## Resultados

Os resultados serão armazenados na pasta:

` Algoritimos > Resultados `

As soluções serão armazenados na Soluções:

` Algoritimos > Soluções `
