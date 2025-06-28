"""
gerar_dados_sinteticos.py

Este script gera três tabelas simuladas com dados sobre a produção industrial brasileira:
1. fProducaoIndustrial: fatos com métricas por setor e data
2. dSetores: dimensão com setores e imagens representativas
3. dCalendario: dimensão de datas completa entre 2013 e 2023

As tabelas são salvas em formato CSV na pasta /data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import calendar
import locale
import os

# Caminho base
base_path = "C:\\GitHub\\dashboard-producao-industrial\\data\\"

# ================================
# dSetores (Dimensão de Setores)
# ================================
setores = ['Agroindústria', 'Automotivo', 'Têxtil e Vestuário', 'Outros']
mapeamento_setores = {
    'Agroindústria': 1,
    'Automotivo': 2,
    'Têxtil e Vestuário': 3,
    'Outros': 4
}
imagens_setores = {
    'Agroindústria': 'https://terramagna.com.br/wp-content/uploads/2022/08/maquinas-agricolas-soja-agronegocio-no-Brasil.jpg',
    'Automotivo': 'https://bpoadvogados.com.br/wp-content/uploads/2018/11/img-destaque-1.jpg',
    'Têxtil e Vestuário': 'https://www.kandohub.com.br/files/industriatextil_1615304565997.jpeg',
    'Outros': 'https://www.blsistemas.com.br/wp-content/uploads/2018/03/quais-sao-os-usos-da-industria-industrial-no-brasil.jpg'
}
dSetores = pd.DataFrame(mapeamento_setores.items(), columns=['Setor', 'id_Setor'])
dSetores['Imagem'] = dSetores['Setor'].map(imagens_setores)
dSetores.to_csv(f"{base_path}dSetores.csv", index=False)

# ======================================
# fProducaoIndustrial (Fato principal)
# ======================================
anos = list(range(2013, 2024))
producaoIndustrial = pd.DataFrame(
    [(ano, mes, setor) for ano in anos for mes in range(1, 13) for setor in setores],
    columns=['Ano', 'Mês', 'Setor']
)
producaoIndustrial['id_Setor'] = producaoIndustrial['Setor'].map(mapeamento_setores)
producaoIndustrial['Data'] = pd.to_datetime(
    producaoIndustrial['Ano'].astype(str) + '-' + producaoIndustrial['Mês'].astype(str) + '-01'
).dt.strftime('%d/%m/%Y')

# Geração realista de métricas
np.random.seed(42)
n = len(producaoIndustrial)

# Matéria-Prima
producaoIndustrial['Matéria-Prima (toneladas)'] = np.random.randint(50000, 200000, n)

# Volume de Produção = Matéria-Prima * fator + ruído
fator_producao = 4.5
ruido = np.random.normal(0, 50000, n)
producaoIndustrial['Volume de Produção (toneladas)'] = (
    producaoIndustrial['Matéria-Prima (toneladas)'] * fator_producao + ruido
).astype(int)

# Número de Trabalhadores = produção / fator + ruído
fator_trabalhador = 150
ruido_trab = np.random.normal(0, 500, n)
producaoIndustrial['Número de Trabalhadores'] = (
    producaoIndustrial['Volume de Produção (toneladas)'] / fator_trabalhador + ruido_trab
).astype(int)

# Valor das Exportações = volume * preço médio + ruído
preco_medio = 180
variacao = np.random.normal(0, 10000000, n)
producaoIndustrial['Valor das Exportações (em dólares)'] = (
    producaoIndustrial['Volume de Produção (toneladas)'] * preco_medio + variacao
).astype(int)

# Remover registros futuros
producaoIndustrial = producaoIndustrial[
    producaoIndustrial['Data'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y')) < datetime.now()
]

# Remove colunas auxiliares
producaoIndustrial.drop(columns=['Ano', 'Mês', 'Setor'], inplace=True)
producaoIndustrial.to_csv(f"{base_path}fProducaoIndustrial.csv", index=False)

# ===========================
# dCalendario (Dimensão Data)
# ===========================
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def criar_calendario(start_ano, end_ano):
    base = []
    for ano in range(start_ano, end_ano + 1):
        for mes in range(1, 13):
            nome_mes = calendar.month_name[mes].capitalize()
            for semana in calendar.monthcalendar(ano, mes):
                for dia in semana:
                    if dia != 0:
                        data = f"{dia:02d}/{mes:02d}/{ano}"
                        base.append([data, nome_mes, mes, ano])
    return pd.DataFrame(base, columns=['Data', 'Nome_Mes', 'Mes_Num', 'Ano'])

dCalendario = criar_calendario(2013, 2023)
dCalendario.to_csv(f"{base_path}dCalendario.csv", index=False)

print(" Dados sintéticos gerados com sucesso em /data/")
