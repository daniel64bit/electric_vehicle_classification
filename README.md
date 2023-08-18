# Electric Vehicles

![Python version](https://img.shields.io/badge/python-3.10%20-blue.svg)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/daniel64bit/biofuel_brazil_plants/blob/main/LICENSE.md)

## Visão Geral

Fonte de dados: [Electric Vehicle Title and Registration Activity
](https://data.wa.gov/Transportation/Electric-Vehicle-Title-and-Registration-Activity/rpr4-cgyd)

## Funcionalidades Principais



## Regras

- Não remova nenhuma linha do arquivo `.gitignore`
- Certifique-se de que seus resultados possam ser reproduzidos
- Não comite dados ao repositório
- Não comite credenciais ou configurações locais ao repositório. Mantenha todas as suas credenciais e configurações locais em `conf/local/`

## Requisitos

As bibliotecas necessárias para a execução do projeto estão listadas no arquivo `src/requirements.txt`. Para instalá-las, utilize o comando:

```
pip install -r src/requirements.txt
```

Além disso, é necessário ter a última versão do [geckodriver](https://github.com/mozilla/geckodriver/releases/) em um diretório conhecido. 

## Como executar o pipeline

Para executar o projeto, utilize o comando:

```
kedro run
```

Para executar uma pipeline específica, utilize o comando:
```
kedro run --pipeline <nome-da-pipeline>
```

## Autores

- [Daniel Rodrigues](https://www.linkedin.com/in/danielrod147/)
- [João Arthur](https://www.linkedin.com/in/jarthurcs25/)
- [INTEGRANTE](LINK)
- [INTEGRANTE](LINK)
