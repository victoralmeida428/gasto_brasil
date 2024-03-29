import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

@st.cache_data
def get_data():
    df = pd.read_csv("https://bit.ly/3amlUZK")
    df["Valor total da compra"] = df["Valor total da compra"].str.replace("R\$ |,", "", regex=True).astype(float)
    df['Data de reconhecimento da compra sem licitação'] = pd.to_datetime(df['Data de reconhecimento da compra sem licitação'], format='%d/%m/%Y')
    return df.sort_values('Data de reconhecimento da compra sem licitação')

@st.cache_data
def get_chart_monthly(df: pd.DataFrame):
    df['mes/ano'] = df['Data de reconhecimento da compra sem licitação'].apply(lambda x: x.strftime('%b/%Y'))
    group_data = df.groupby(['mes/ano', 'Orgão']).agg({
        'Valor total da compra': 'sum'
    }).reset_index()
    group_data['x'] = group_data['mes/ano'].apply(lambda x: dt.datetime.strptime(x, '%b/%Y'))
    fig = px.line(
        group_data.sort_values('x'), 
        x='mes/ano', 
        y='Valor total da compra', 
        title='Gasto mensal', 
        color='Orgão',
        )
    fig.update_layout(title_x=0.5, legend_orientation='h', legend_itemclick='toggleothers', legend_itemdoubleclick='toggle')
    fig.update_xaxes(title=None)
    fig.update_yaxes(title='Gasto<br>R$')
    return fig

@st.cache_data
def get_uasg_chart(df):
    fig = px.bar(df_filter.groupby('UASG').agg({'Valor total da compra': 'sum'})\
              .sort_values('Valor total da compra', ascending=False).head()\
                .sort_values('Valor total da compra'), 
                x='Valor total da compra',
                color_discrete_sequence=['green'],
                title='Maiores gastos por orgão',
                text_auto=True)
    fig.update_layout(title_x=0.5)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title='Gasto R$')
    return fig

col1, col2 = st.columns(2)
with col2:
    st.title('Gastos Públicos')
with col1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil.svg', width=100)
df = get_data()
df_filter = df.copy()
date_min = df_filter['Data de reconhecimento da compra sem licitação'].min()
date_max = df_filter['Data de reconhecimento da compra sem licitação'].max()
with st.sidebar:
    orgao = st.multiselect('Orgão', options=list(df_filter['Orgão'].unique()), placeholder='Escolha o orgão...')
    if orgao:
        df_filter = df_filter.query('Orgão == @orgao')
    indice = st.multiselect('Código da modalidade da compra', options=list(df_filter['Código da modalidade da compra'].unique()), placeholder='Escolha a modalidade')
    if indice:
        df_filter = df_filter.query('`Código da modalidade da compra` == @indice')
    uasg = st.multiselect('UASG', options=list(df_filter['UASG'].unique()), placeholder='Escolha o UASG...')
    if uasg:
        df_filter = df_filter.query('UASG == @uasg')
    col1, col2 = st.columns(2)
    with col1:
        
        start = st.date_input('Início', min_value=date_min, max_value=date_max, value=date_min)
    with col2:
        end = st.date_input('Final', min_value=date_min, max_value=date_max, value=date_max)

df_filter = df_filter.query('(`Data de reconhecimento da compra sem licitação` >= @start) & (`Data de reconhecimento da compra sem licitação` <= @end)')







chart = st.selectbox("Índice", options=['Gasto mensal', 'Gastos por UASG'])
if chart == 'Gasto mensal':
    st.write(get_chart_monthly(df_filter))
if chart == 'Gastos por UASG':
    st.write(get_uasg_chart(df_filter))


