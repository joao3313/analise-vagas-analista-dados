import pandas as pd
from pathlib import Path

# Pasta onde está o main.py -> funciona de qualquer terminal
PASTA = Path(__file__).parent

# vagas = pd.read_csv(PASTA / 'vagas.csv', header=1)  # 1ª linha do CSV é vazia (COMENTADO)
candidatura = pd.read_csv(PASTA / 'vagas_aplicadas.csv')

# Limpa nomes das colunas: tira espaços extras e padroniza acentos
candidatura.columns = candidatura.columns.str.normalize('NFC').str.strip()

# ============ VAGAS EBAC (BLOCO COMENTADO POIS vagas.csv NÃO ESTÁ NO REPO) ============
# filtro = (vagas['Curso 1'].str.contains('Analista de Dados', na=False)) | \
#          (vagas['Curso 2'].str.contains('Analista de Dados', na=False)) | \
#          (vagas['Curso 3'].str.contains('Analista de Dados', na=False))
#
# vagas_filtradas = vagas[filtro]
# df_dados = vagas_filtradas[['Nome da Vaga', 'Complexidade', 'Regime', 'Estado', 'Carimbo de data/hora']].copy()
#
# df_dados['Regime'] = df_dados['Regime'].replace('Híbrido', 'Híbrida')
#
# df_dados['Carimbo de data/hora'] = pd.to_datetime(
#     df_dados['Carimbo de data/hora'].str[:10],
#     format='%d/%m/%Y',
#     errors='coerce'
# )
#
# print("Número de vagas filtradas:", vagas_filtradas.shape[0])
# print("Carimbos que falharam na conversão:", df_dados['Carimbo de data/hora'].isna().sum())
#
# contagem_complexidade = df_dados['Complexidade'].value_counts()
# print("\nVagas por complexidade:", contagem_complexidade.to_dict())
#
# qtd_valores_nulos = df_dados['Complexidade'].isna().sum()
# print(f"\nQuantidade de valores nulos em 'Complexidade': {qtd_valores_nulos}")
#
# df_elegiveis = df_dados[df_dados['Complexidade'] == 'Baixa'].copy()
# print("Vagas elegíveis:", df_elegiveis.shape[0])
#
# print("\nDistribuição de regimes nas vagas elegíveis:")
# print(df_elegiveis['Regime'].value_counts(normalize=True))
#
# print("\nDistribuição por estado nas vagas elegíveis:")
# print(df_elegiveis['Estado'].value_counts(normalize=True))
#
# concentracao = pd.crosstab(df_elegiveis['Estado'], df_elegiveis['Regime'])
# print("\nRegime das vagas sem estado ('Não se aplica'):")
# print(concentracao.loc['Não se aplica'])

# ============ MINHAS CANDIDATURAS ============

candidatura = candidatura.rename(columns={'w': 'Nome da Vaga', 'portal': 'Canal de origem'})
candidatura['Nome da Vaga'] = candidatura['Nome da Vaga'].str.strip()
candidatura['status do processo'] = 'Negada'

# Corrige erros de digitação nas datas
candidatura['Data'] = candidatura['Data'].replace({
    '31/09/2026': '30/09/2026',
    '8/7/2026': '7/8/2026'
})

# Converte a data; o que não encaixar vira vazio (NaT) em vez de dar erro
candidatura['Data'] = pd.to_datetime(candidatura['Data'], format='%d/%m/%Y', errors='coerce')
print("\nDatas de candidatura que falharam:", candidatura['Data'].isna().sum())

print("\n", candidatura['status do processo'].value_counts())
print("\n", candidatura['etapa'].value_counts())
print("\n", candidatura['Canal de origem'].value_counts())
print("\n", candidatura['indicação EBAC'].value_counts())

print("\nPeríodo das candidaturas:", candidatura['Data'].min(), "até", candidatura['Data'].max())

candidatura['Mes'] = candidatura['Data'].dt.to_period('M')

print("\nCandidaturas por mês:")
print(candidatura['Mes'].value_counts().sort_index())

print("\nCanal de origem x Indicação EBAC:")
print(pd.crosstab(candidatura['Canal de origem'], candidatura['indicação EBAC']))

print("\nCanal de origem x Indicação EBAC (%):")
print((pd.crosstab(candidatura['Canal de origem'], candidatura['indicação EBAC'], normalize='index') * 100).round(1))

# ============ EXPORTAÇÃO PARA O POWER BI ============

# df_dados.to_csv(PASTA / 'vagas_limpas.csv', index=False, encoding='utf-8-sig')  # COMENTADO PARA NÃO SOBRESCREVER O EXISTENTE
candidatura.to_csv(PASTA / 'candidaturas_limpas.csv', index=False, encoding='utf-8-sig')

print("\nArquivos exportados para:", PASTA)