import pandas as pd
import numpy as np

def criar_dcalendario(data_inicio, data_fim):
    """
    Gera uma tabela dCalendário entre as datas especificadas.

    Args:pip 
        data_inicio (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Tabela dCalendário com colunas calculadas.

    Raises:
        ValueError: Se o formato das datas for inválido ou `data_inicio` for maior que `data_fim`.

    Exemplos:
        >>> criar_dcalendario('2024-01-01', '2024-12-31')
    """
    try:
        # Validar formatos e converter para datetime
        data_inicio = pd.to_datetime(data_inicio, format='%Y-%m-%d')
        data_fim = pd.to_datetime(data_fim, format='%Y-%m-%d')
    except Exception as e:
        raise ValueError("As datas devem estar no formato 'YYYY-MM-DD'.") from e
    
    if data_inicio > data_fim:
        raise ValueError("A data inicial deve ser menor ou igual à data final.")

    # Gerar uma lista de datas no intervalo
    listar_datas = pd.date_range(start=data_inicio, end=data_fim)
    
    # Criar o DataFrame dCalendário
    d_calendario = pd.DataFrame({'Data': listar_datas})
    d_calendario['Ano'] = d_calendario['Data'].dt.year
    d_calendario['NomeMes'] = d_calendario['Data'].dt.month_name().str.title()
    d_calendario['MesAbre'] = d_calendario['NomeMes'].str[:3]
    d_calendario['MesAno'] = d_calendario['MesAbre'] + '-' + d_calendario['Ano'].astype(str).str[-2:]
    d_calendario['MesNum'] = d_calendario['Data'].dt.month
    d_calendario['AnoMesINT'] = d_calendario['Ano'] * 100 + d_calendario['MesNum']
    d_calendario['InicioMes'] = d_calendario['Data'].dt.to_period('M').dt.start_time
    d_calendario['Trimestre'] = d_calendario['Data'].dt.quarter
    d_calendario['TrimestreAbreviado'] = d_calendario['Trimestre'].astype(str) + "º Trim"
    d_calendario['Bimestre'] = np.ceil(d_calendario['MesNum'] / 2).astype(int).astype(str) + "º Bim"
    d_calendario['Semestre'] = np.ceil(d_calendario['MesNum'] / 6).astype(int).astype(str) + "º Sem"
    d_calendario['Semana'] = d_calendario['Data'].dt.isocalendar().week
    d_calendario['DiaSemana'] = d_calendario['Data'].dt.weekday + 1  # Segunda = 1, Domingo = 7
    d_calendario['NomeDia'] = d_calendario['Data'].dt.day_name().str.title()
    d_calendario['Passado'] = d_calendario['Data'] <= pd.Timestamp.today()
    d_calendario['AnoAtual'] = np.where(d_calendario['Data'].dt.year == pd.Timestamp.today().year, "Ano Atual", d_calendario['Ano'].astype(str))
    d_calendario['MesAtual'] = np.where(
        (d_calendario['Data'].dt.year == pd.Timestamp.today().year) & (d_calendario['Data'].dt.month == pd.Timestamp.today().month),
        "Mês Atual",
        d_calendario['NomeMes']
    )
    
    return d_calendario

df = criar_dcalendario(data_inicio="2024-10-01", data_fim="2025-01-01")
print(df)