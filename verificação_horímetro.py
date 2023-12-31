# -*- coding: utf-8 -*-
"""Verificação horímetro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wdeJ6Mzd7066N1L2jlfzIDWzshLk8cFI

Autor: Luiz Felipe Souza
"""

import pandas as pd
import warnings
warnings.simplefilter("ignore")

#Entrada da base
Dados1 = pd.read_excel('/content/Abastecimentos.xlsx')
Dados1['KM'] = Dados1['KM'].fillna(0)
Dados1['QTD'] = Dados1['QTD'].fillna(0)
Dados = Dados1
y = 0
z = 0

#Pré-processamento (Filtro 'HR' | Conversão coluna KM e Unidade)
Dados = Dados.replace({',': '.'}, regex=True)
Dados['KM'] = Dados['KM'].astype('float64')
Dados['QTD'] = Dados['QTD'].astype('float64')
Dados['TIPO_RODADO'] = Dados['TIPO_RODADO'].astype('string')

#Filtrar equipamentos HR
Dados = Dados[Dados['TIPO_RODADO']=='HR']

#Tratamento da coluna data
lista_data1 = []
for k in Dados['HR_OPERACAO']:
  k = str(k)
  convert = k.split()
  parameter = 'j'
  if int(len(convert))<2:
    lista_data1.append((str(convert[0]))+"  00:00:00")
    parameter = 'i'
  if int(len(convert))>=2 and parameter=='j':
    lista_data1.append(" ".join(str(k).split()))

Dados['HR_OPERACAO'] = lista_data1
Dados['HR_OPERACAO']  = pd.to_datetime(Dados['HR_OPERACAO'], format='%Y/%m/%d %H:%M:%S')

#Cálculo quantidade de dias para cálculo
Dados['Dias'] = (Dados['HR_OPERACAO'].max()-Dados['HR_OPERACAO'].min())
Dados['Dias'] = (round((Dados['Dias'].dt.days),0).astype('int64'))-3
Dias_menos_3 = int(Dados['Dias'].iloc[0])+1

#Primeira verificação KM/dia maior ou igual a 22
Verificação = Dados.groupby('FROTA')['KM'].sum().reset_index()
Verificação['Verificação'] = Verificação['KM']/Dias_menos_3 #AQUI VEM O Dias_menos_5
Verificação = Verificação[Verificação['Verificação']>=22]

#Filtrando as frotas da primeira verificação na base total
Lista_frotas_erros = list(Verificação['FROTA'])
Result = Dados.loc[Dados['FROTA'].isin(Lista_frotas_erros)]

#Ordenando os valores por FROTA e Horímetro
Result = Result.sort_values(['FROTA', 'HR_OPERACAO']).reset_index(drop=True)

#Encontrando a diferença entre horímetro anterior e posterior
D_1 = list(Result['NO_HOR_ODOM'])
if len(D_1)>0:
  del D_1[0]
  D_1.append('0')
  Result['NO_HOR_ODOM_D1'] = D_1
  Result['NO_HOR_ODOM'] = Result['NO_HOR_ODOM'].astype('float64')
  Result['NO_HOR_ODOM_D1'] = Result['NO_HOR_ODOM_D1'].astype('float64')
  Result['Erro1'] = Result['NO_HOR_ODOM_D1']-Result['NO_HOR_ODOM']
  y = 1

#Segunda verificação de acordo com a média de KM
Result['MEAN'] = Result['QTD']/Result['KM']
Mean = Result[Result['MEAN']<=100]
Media_equipamento_HR = Mean.groupby(['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER'])['MEAN'].mean().reset_index()
Result = Result.merge(Media_equipamento_HR.set_index(['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER']), on=['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER'], how='left').reset_index(drop=True)
Result['Erro2'] = (Result['MEAN_y']*1.3)-Result['MEAN_x']

#Exbindo resultados para verificação
Result['Observação'] = '-'
if y == 1:
  Result.loc[((Result['Erro1'])<=0) & (Result['Observação']=='-'), 'Observação'] = "Erro 1: Horímetro apontado fora da margem sequencial"
  y=0
# Result.loc[((Result['Erro2'])<0) & (Result['Observação']=='-'), 'Observação'] = "Erro 2: Média acima de 30% da média de consumo para o veículo"

#Tabela final tratada
Result_HR = Result[['INSTANCIA', 'PONTO', 'BOLETIM', 'FROTA', 'MARCA', 'MODELO', 'CATEGORIA', 'MATRICULA', 'OPERADOR', 'CARGO', 'HR_OPERACAO', 'MES', 'ANO', 'CD_MATERIAL', 'COMBUSTIVEL', 'OPER', 'OPERACAO', 'TIPO_RODADO', 'QTD', 'NO_HOR_ODOM', 'KM', 'Observação']]

# ############################################################## || ############################################################

#Entrada da base
Dados2 = Dados1

#Pré-processamento (Filtro 'HR' | Conversão coluna KM e Unidade)
Dados2 = Dados2.replace({',': '.'}, regex=True)
Dados2['KM'] = Dados2['KM'].astype('float64')
Dados2['QTD'] = Dados2['QTD'].astype('float64')
Dados2['TIPO_RODADO'] = Dados2['TIPO_RODADO'].astype('string')

#Filtrar equipamentos KM
Dados2 = Dados2[Dados2['TIPO_RODADO']=='KM']

#Tratamento da coluna data
lista_data = []
for i in Dados2['HR_OPERACAO']:
  i = str(i)
  convert = i.split()
  parameter = 'j'
  if int(len(convert))<2:
    lista_data.append(str(str(convert[0])+"  00:00:00"))
    parameter = 'i'
  if int(len(convert))>=2 and parameter=='j':
    lista_data.append(" ".join(str(i).split()))

Dados2['HR_OPERACAO'] = lista_data
Dados2['HR_OPERACAO']  = pd.to_datetime(Dados2['HR_OPERACAO'], format='%Y/%m/%d %H:%M:%S')

#Cálculo quantidade de dias para cálculo
Dados2['Dias'] = (Dados2['HR_OPERACAO'].max()-Dados2['HR_OPERACAO'].min())
Dados2['Dias'] = round((Dados2['Dias'].dt.days),0).astype('int64')-3
Dias_menos_3 = (int(Dados2['Dias'].iloc[0]))+1

#Primeira verificação KM/dia maior ou igual a 22
Verificação2 = Dados2.groupby('FROTA')['KM'].sum().reset_index()
Verificação2['Verificação'] = Verificação2['KM']/Dias_menos_3 #AQUI VEM O Dias_menos_3
Verificação2 = Verificação2[Verificação2['Verificação']>=1000]

#Filtrando as frotas da primeira verificação na base total
Lista_frotas_erros2 = list(Verificação2['FROTA'])
Result2 = Dados2.loc[Dados2['FROTA'].isin(Lista_frotas_erros2)]

#Ordenando os valores por FROTA e Horímetro
Result2 = Result2.sort_values(['FROTA', 'HR_OPERACAO']).reset_index(drop=True)

#Encontrando a diferença entre horímetro anterior e posterior
D_2 = list(Result2['NO_HOR_ODOM'])
if len(D_2)>0:
  del D_2[0]
  D_2.append('0')
  Result2['NO_HOR_ODOM_D1'] = D_2
  Result2['NO_HOR_ODOM'] = Result2['NO_HOR_ODOM'].astype('float64')
  Result2['NO_HOR_ODOM_D1'] = Result2['NO_HOR_ODOM_D1'].astype('float64')
  Result2['Erro1'] = Result2['NO_HOR_ODOM_D1']-Result2['NO_HOR_ODOM']
  x = 1

#Segunda verificação de acordo com a média de KM
Result2['MEAN'] = Result2['KM']/Result2['QTD']
Mean = Result2[Result2['MEAN']<=30]
Media_equipamento_KM = Mean.groupby(['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER'])['MEAN'].mean().reset_index()
Result2 = Result2.merge(Media_equipamento_KM.set_index(['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER']), on=['INSTANCIA', 'MODELO', 'FROTA', 'CD_MATERIAL', 'OPER'], how='left').reset_index(drop=True)
Result2['Erro2'] = Result2['MEAN_x'] - (Result2['MEAN_y']*1.3)

#Exbindo Resultados para verificação
Result2['Observação'] = '-'
if x==1:
  Result2.loc[((Result2['Erro1'])<=0) & (Result2['Observação']=='-'), 'Observação'] = "Erro 1: Horímetro apontado fora da margem sequencial"
  x=0
# Result2.loc[((Result2['Erro2'])<0) & (Result2['Observação']=='-'), 'Observação'] = "Erro 2: Média abaixo de 30% da média de consumo para o veículo"

#Tabela final tratada
Result_KM = Result2[['INSTANCIA', 'PONTO', 'BOLETIM', 'FROTA', 'MARCA', 'MODELO', 'CATEGORIA', 'MATRICULA', 'OPERADOR', 'CARGO', 'HR_OPERACAO', 'MES', 'ANO', 'CD_MATERIAL', 'COMBUSTIVEL', 'OPER', 'OPERACAO', 'TIPO_RODADO', 'QTD', 'NO_HOR_ODOM', 'KM', 'Observação']]

#Unindo os dois dataframes resultantes
frames = [Result_HR, Result_KM]
result = pd.concat(frames)

#Ordenando os valores por FROTA e Horímetro
result = result.sort_values(['FROTA', 'HR_OPERACAO']).reset_index(drop=True)

#Removendo frotas avulsas
values=['LOCACAO AVULSA (KM)', 'LOCACAO AVULSA (HR)']
result = result[~result.CATEGORIA.isin(values)]
result['HR_OPERACAO'] = result['HR_OPERACAO'].dt.strftime('%d/%m/%Y %H:%M:%S')

#Salvar planilha Result
result.to_excel('/content/Correção de horímetros.xlsx', index = False)