# 📆 dcalendario
**dcalendario** é uma biblioteca Python que cria uma tabela de calendário detalhada para análises de dados, incluindo informações úteis como ano, mês, trimestre, semana, entre outras. Essa tabela pode ser usada em projetos de ciência de dados, business intelligence (BI), e aplicações que necessitam de cálculos baseados em datas.

## ✨ Instalação
Instale a biblioteca diretamente do PyPI usando o pip:
```
pip install dcalendario
```

## 🚀 Funcionalidade
A biblioteca gera um DataFrame pandas com uma tabela de calendário detalhada, baseada em um intervalo de datas fornecido pelo usuário.

### Principais Recursos:
- Geração automática de datas entre o início e o fim do intervalo.
- Adiciona colunas com informações úteis:
- Ano, mês, nome do mês, trimestre, semestre, semana, entre outras.
- Identifica se a data pertence ao ano/mês atual.
- Indica se a data é no passado (comparando com a maior data do intervalo).
- Suporte a múltiplas localizações para nomes de meses e dias.

## 🧰 Funções Disponíveis
> criar_dcalendario(data_inicio: str, data_fim: str, locale: str = "en_US") -> pandas.DataFrame
Gera a tabela de calendário.

### Parâmetros:
start_date (str): Data de início do intervalo no formato YYYY-MM-DD.
end_date (str): Data de término do intervalo no formato YYYY-MM-DD.
locale (str): Localização para formatar os nomes dos meses e dias (ex.: pt_BR, en_US).
### Retorno:
**pandas.DataFrame:** Uma tabela de calendário com as colunas detalhadas abaixo.

## 🗂️ Colunas da Tabela

🗂️ Colunas da Tabela

| Coluna                | Tipo  | Descrição                                                                                      |
|-----------------------|-------|------------------------------------------------------------------------------------------------|
| Data                  | date  | A data correspondente ao dia.                                                                  |
| Ano                   | int   | O ano da data.                                                                                 |
| NomeMes               | str   | Nome completo do mês (ex.: Janeiro).                                                           |
| MesAbre               | str   | Abreviação do mês (ex.: Jan).                                                                  |
| MesAno                | str   | Mês e ano combinados no formato MMM-YY (ex.: Jan-24).                                          |
| MesNum                | int   | Número do mês (1 a 12).                                                                        |
| AnoMesINT             | int   | Ano e mês no formato YYYYMM (ex.: 202401).                                                     |
| InicioMes             | date  | Primeiro dia do mês.                                                                           |
| Trimestre             | int   | Trimestre da data (1 a 4).                                                                     |
| TrimestreAbreviado    | str   | Abreviação do trimestre (ex.: 1º Trim).                                                        |
| Bimestre              | str   | Bimestre da data (ex.: 1º Bim).                                                                |
| Semestre              | str   | Semestre da data (ex.: 1º Sem).                                                                |
| Semana                | int   | Número da semana dentro do mês.                                                                |
| DiaSemana             | int   | Número do dia na semana (0 = domingo, 6 = sábado).                                             |
| NomeDia               | str   | Nome completo do dia da semana (ex.: Segunda-feira).                                           |
| Passado               | bool  | True se a data for menor ou igual à maior data no intervalo; caso contrário, False.            |
| AnoAtual              | str   | Ano Atual se for o ano corrente, ou o ano específico da data.                                  |
| MesAtual              | str   | Mês Atual se for o mês corrente; caso contrário, o nome completo do mês.                       |

## 📚 Exemplos de Uso
### Importação e geração de calendário
```
from dcalendario import criar_dcalendario

# Gerar calendário para 2024
calendario = criar_dcalendario('2024-01-01', '2024-12-31', locale='pt_BR')
```

### Saída (exemplo):

```
         Data   Ano   NomeMes MesAbre  MesAno  MesNum  AnoMesINT  ...  Semana  DiaSemana NomeDia Passado     AnoAtual     MesAtual
0  2024-01-01  2024  Janeiro     Jan  Jan-24       1    202401  ...       1          1   Segunda    True    Ano Atual   Mês Atual
1  2024-01-02  2024  Janeiro     Jan  Jan-24       1    202401  ...       1          2   Terça      True    Ano Atual   Janeiro
2  2024-01-03  2024  Janeiro     Jan  Jan-24       1    202401  ...       1          3   Quarta     True    Ano Atual   Janeiro
...
```

### Filtrar datas do ano atual

```
# Datas do ano corrente
datas_ano_corrente = calendario[calendario['AnoAtual'] == 'Ano Atual']
print(datas_ano_corrente.head())
```

### 🛠️ Testes
Para executar os testes unitários, rode o seguinte comando na raiz do projeto:
```
python -m unittest discover tests
```

## 🛡️ Contribuições
Contribuições são bem-vindas! Siga os passos abaixo para colaborar:
1. Faça um fork do repositório.
2. Crie uma branch para a sua feature/bugfix.
3. Envie um Pull Request.

## 🔗 Links Úteis
- Repositório no GitHub: [dcalendario](https://github.com/CarlosEX/dCalendario) c
- Reporte de Issues: [GitHub Issues](https://github.com/CarlosEX/dCalendario/issues)

## 📝 Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.


