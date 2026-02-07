import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('curso pandas/dados_dash.csv')

def apply_demographic_filters(data, sex, race, age, education):
    mask = pd.Series(True, index = data.index)

    for col, val in [
        ('Sexo', sex),
        ('Raça', race),
        ('Faixa etária', age),
        ('Nível de instrução', education)
    ]:
        if val != 'nan':
            mask &= data[col].eq(val)
        else:
            mask &= data[col].isna()
    
    return data.loc[mask]

def format(valor_atual, valor_ant, prefixo = '', sufixo = '', decimal = 1):
        dif = valor_atual - valor_ant
        porc = ((valor_atual/valor_ant)-1)*100

        dif_format = f'{dif:+,.{decimal}f}'.replace(",", "X").replace(".", ",").replace("X", ".")
        porc_format = f'{porc:+,.{decimal}f}'.replace(",", "X").replace(".", ",").replace("X", ".")

        dif_format = f'{prefixo}{dif_format}{sufixo}'
        porc_format = f'{prefixo}{porc_format}{sufixo}'

        return html.Small(f'{dif_format}'), html.Small(f'{porc_format}')

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(external_stylesheets = [dbc.themes.FLATLY, dbc_css])
server = app.server

####################################################CRIAÇÃO DOS CARDS##############################################
card_graph = [
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H6(html.Strong('Indicador:')),
                dcc.Dropdown(
                    id = 'dropdown_indicator_graph',
                    options = {
                        'Taxa de desocupação':'Taxa de desocupação',
                        'Nível da ocupação':'Nível de ocupação',
                        'Participação':'Taxa de participação',
                        'Pessoas em idade ativa':'Pessoas em idade ativa',
                        'Pessoas ocupadas':'Pessoas ocupadas',
                        'Pessoas desocupadas':'Pessoas desocupadas',
                        'Força de trabalho':'Força de trabalho',
                        'Renda habitual principal':'Renda habitual principal',
                        'Renda efetiva principal':'Renda efetiva principal',
                        'Renda habitual total':'Renda habitual total',
                        'Renda efetiva total':'Renda efetiva total'
                    },
                    value = 'Taxa de desocupação'),
                html.Br(),
                html.H6(html.Strong('Período:')),
                dcc.Dropdown(
                    id = 'dropdown_tri_graph',
                    options = {
                        '':'Todos',
                        '01':'1° trimestre',
                        '02':'2° trimestre',
                        '03':'3° trimestre',
                        '04':'4° trimestre'
                    },
                    value = ''
                ),
                html.Br(),
                html.Small('Fonte: IBGE - PNAD Contínua (microdados), Janeiro de 2026. Elaboração: Observatório de Políticas Públicas do Trabalho do Ceará')
            ], width = 2),
            dbc.Col(dcc.Graph(id = 'graph',
                            config={
                                'responsive': True,
                                'displayModeBar': False
                            }), width = 10, 
                    style = {'height': '105%', 'width': '80%', 'margin-top':'0px', 'margin-start':'20px'}
                    )
        ], className="h-100 g-2")
    ], className="h-100 ms-2 me-0 mb-0")
]

card_rate = [
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.Label(html.Strong('Indicador')), width = 4),
            dbc.Col(html.Label(html.Strong('Valor')), width = 3),
            dbc.Col(html.Label(html.Strong('Variação a/a')), width = 5, className = 'text-center')
        ], className = 'mb-2'),
        dbc.Row([
            dbc.Col(html.H6('Taxa de participação:'), width = 4),
            dbc.Col(html.H6(id = 'participation_rate'), width = 3),
            dbc.Col(id = 'participation_rate_dif', width = 3),
            dbc.Col(id = 'participation_rate_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Nível de ocupação:'), width = 4),
            dbc.Col(html.H6(id = 'employment_level'), width = 3),
            dbc.Col(id = 'employment_level_dif', width = 3),
            dbc.Col(id = 'employment_level_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Taxa de desocupação:'), width = 4),
            dbc.Col(html.H6(id = 'unemployment_rate'), width = 3),
            dbc.Col(id = 'unemployment_rate_dif', width = 3),
            dbc.Col(id = 'unemployment_rate_porc', width = 2)
        ])
    ])
]

card_filter = [
    dbc.Row([
            dbc.Col([
                html.H6(html.Strong('Período:')),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id = 'dropdown_tri',
                            options = {
                                '01':'1° trimestre',
                                '02':'2° trimestre',
                                '03':'3° trimestre',
                                '04':'4° trimestre',
                            },
                            value = None,
                            placeholder = 'Trimestre'
                        )
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id = 'dropdown_year',
                            options = 
                                {str(i) : str(i) for i in range(2016, 2026)},
                            value = None,
                            placeholder = 'Ano'
                        )
                    )
                ]),
            ]),
            dbc.Col([
                html.H6(html.Strong('Sexo:')),
                dcc.Dropdown(
                    id = 'dropdown_sex',
                    options = {
                        'nan':'Geral',
                        'Homem':'Homem',
                        'Mulher':'Mulher'
                    },
                    value = 'nan')
            ]),
            dbc.Col([
                html.H6(html.Strong('Faixa etária:')),
                dcc.Dropdown(
                    id = 'dropdown_age',
                    options = {
                        'nan':'Geral',
                        '14 a 17':'14 a 17',
                        '18 a 24':'18 a 24',
                        '15 a 29':'15 a 29',
                        '25 a 39':'25 a 39',
                        '40 a 59':'40 a 59',
                        '60 ou mais':'60 ou mais'
                    },
                    value = 'nan'
                )
            ])
    ], className = 'ms-2 me-2 mt-2 mb-1'),
    dbc.Row([
        dbc.Col([
            html.H6(html.Strong('Local:'),
                        style = {'margin-top':"0px"}),
                    dcc.Dropdown(
                        id = 'dropdown_local',
                        options = {_ : _ for _ in df['Local'].unique()}
                    )
        ]),
        dbc.Col([
            html.H6(html.Strong('Raça:', style = {'margin-top':'2px'})),
                dcc.Dropdown(
                    id = 'dropdown_race',
                    options = {
                        'nan':'Geral',
                        'Negra':'Negro',
                        'Não Negra':'Não Negro'
                    },
                    value = 'nan'
                )
        ]),
        dbc.Col([
            html.H6(html.Strong('Escolaridade:',
                    style = {'margin-top':"2px"})),
                dcc.Dropdown(
                    id = 'dropdown_education',
                    options = {
                        'nan':'Geral',
                        'Sem instrução e menos de 1 ano de estudo':'Sem instrução e menos de 1 ano de estudo',
                        'Fundamental incompleto ou equivalente':'Fundamental incompleto ou equivalente',
                        'Fundamental completo ou equivalente':'Fundamental completo ou equivalente',
                        'Médio incompleto ou equivalente':'Médio incompleto ou equivalente',
                        'Médio completo ou equivalente':'Médio completo ou equivalente',
                        'Superior incompleto ou equivalente':'Superior incompleto ou equivalente',
                        'Superior completo':'Superior completo'
                    },
                    value = 'nan'
                )
        ])
    ], className = 'ms-2 me-2 mt-0 mb-2')            
]

card_logo = [
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src = '/assets/secretaria_do_trabalho_h_1-1024x336.webp',
                        top = True,
                        style = {'height': '100px', 'object-fit':'contain'}
                    ), className = "d-flex justify-content-center align-items-center"
                ),
                dbc.Col(
                    dbc.CardImg(
                        src = '/assets/Logo_Observatorio-768x251.png',
                        top = True,
                        style = {'height': '100px', 'object-fit':'contain'}
                    ), className="d-flex justify-content-center align-items-center"
                )
            ], className = 'h-100'
        ), className="d-flex align-items-center h-100"
    )
]

card_rend = [
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.Label(html.Strong('Rendimento')), width = 4),
            dbc.Col(html.Label(html.Strong('Valor')), width = 3),
            dbc.Col(html.Label(html.Strong('Variação a/a')), width = 5, className = 'text-center')
        ], className = 'mb-2'),
        dbc.Row([
            dbc.Col(html.H6('Habitual principal:'), width = 4),
            dbc.Col(html.H6(id = 'hab_princ'), width = 3),
            dbc.Col(id = 'hab_princ_dif', width = 3),
            dbc.Col(id = 'hab_princ_porc', width = 2
                    )
        ]),
        dbc.Row([
            dbc.Col(html.H6('Efetivo principal:'), width = 4),
            dbc.Col(html.H6(id = 'efet_princ'), width = 3),
            dbc.Col(id = 'efet_princ_dif', width = 3),
            dbc.Col(id = 'efet_princ_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Habitual total:'), width = 4),
            dbc.Col(html.H6(id = 'hab_total'), width = 3),
            dbc.Col(id = 'hab_total_dif', width = 3),
            dbc.Col(id = 'hab_total_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Efetivo total:'), width = 4),
            dbc.Col(html.H6(id = 'efet_total'), width = 3),
            dbc.Col(id = 'efet_total_dif', width = 3),
            dbc.Col(id = 'efet_total_porc', width = 2)
        ]), 
    ])
]

card_pop = [
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.Label(html.Strong('Indicador')), width = 4),
            dbc.Col(html.Label(html.Strong('Valor')), width = 3),
            dbc.Col(html.Label(html.Strong('Variação a/a')), width = 5, className = 'text-center')
        ], className = 'mb-2'),
        dbc.Row([
            dbc.Col(html.H6('PIA:'), width = 4),
            dbc.Col(html.H6(id = 'pia'), width = 3),
            dbc.Col(id = 'pia_dif', width = 3),
            dbc.Col(id = 'pia_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Força de trabalho:'), width = 4),
            dbc.Col(html.H6(id = 'workforce'), width = 3),
            dbc.Col(id = 'workforce_dif', width = 3),
            dbc.Col(id = 'workforce_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Ocupados:'), width = 4),
            dbc.Col(html.H6(id = 'employed'), width = 3),
            dbc.Col(id = 'employed_dif', width = 3),
            dbc.Col(id = 'employed_porc', width = 2)
        ]),
        dbc.Row([
            dbc.Col(html.H6('Desocupados:'), width = 4),
            dbc.Col(html.H6(id = 'unemployed'), width = 3),
            dbc.Col(id = 'unemployed_dif', width = 3),
            dbc.Col(id = 'unemployed_porc', width = 2)
        ]), 
    ])
]

####################################################FORMANDO LAYOUT##############################################
app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        card_logo, color = "success", outline = True,
                        style={'border-width': '2px', 'height': '21vh'}
                        ),
                        width = 4
                ),
                dbc.Col(
                    dbc.Card(
                        card_filter, color = "success", outline = True,
                        style={'border-width': '2px', 'height': '21vh'}
                    ),
                    width = 8
                )
            ], className= 'ms-2 me-2 mt-1 mb-2'),
            dbc.Row([ 
                dbc.Col(
                    dbc.Card(card_pop, color = "success", outline = True, 
                            style = {'height':'25vh', 'border-width':'2px'}), 
                            width = 4
                ),
                dbc.Col(
                    dbc.Card(card_rate, color = "success", outline = True,
                            style = {'height':'25vh', 'border-width':'2px'}),
                            width = 4
                ),
                dbc.Col(
                    dbc.Card(card_rend, color = "success", outline = True,
                            style = {'height':'25vh', 'border-width':'2px'}),
                            width = 4
                )
                 ], className= 'ms-2 me-2 mt-1 mb-1 h-100'),
            dbc.Row([
                dbc.Col(
                    dbc.Card(card_graph, color = "success", outline = True, 
                            style = {'height':'49vh', 'border-width':'2px', "overflow": "hidden"}), 
                            width = 12
                )
            ], className= 'ms-2 me-2 mt-2 mb-2')
        ], fluid = True, className = 'dbc p-1')

####################################################CALLBACKS##############################################
@app.callback(
   [
      Output('unemployment_rate', 'children'),
      Output('employment_level', 'children'),
      Output('participation_rate', 'children'),
      Output('pia', 'children'),
      Output('employed', 'children'),
      Output('workforce', 'children'),
      Output('unemployed', 'children'),
      Output('hab_princ', 'children'),
      Output('efet_princ', 'children'),
      Output('hab_total', 'children'),
      Output('efet_total', 'children'),
      Output('unemployment_rate_dif', 'children'),
      Output('unemployment_rate_porc', 'children'),
      Output('employment_level_dif', 'children'),
      Output('employment_level_porc', 'children'),
      Output('participation_rate_dif', 'children'),
      Output('participation_rate_porc', 'children'),
      Output('pia_dif', 'children'),
      Output('pia_porc', 'children'),
      Output('employed_dif', 'children'),
      Output('employed_porc', 'children'),
      Output('workforce_dif', 'children'),
      Output('workforce_porc', 'children'),
      Output('unemployed_dif', 'children'),
      Output('unemployed_porc', 'children'),
      Output('hab_princ_dif', 'children'),
      Output('hab_princ_porc', 'children'),
      Output('efet_princ_dif', 'children'),
      Output('efet_princ_porc', 'children'),
      Output('hab_total_dif', 'children'),
      Output('hab_total_porc', 'children'),
      Output('efet_total_dif', 'children'),
      Output('efet_total_porc', 'children')
   ],
   [
      Input('dropdown_tri', 'value'),
      Input('dropdown_year', 'value'),
      Input('dropdown_local', 'value'),
      Input('dropdown_sex', 'value'),
      Input('dropdown_race', 'value'),
      Input('dropdown_age', 'value'),
      Input('dropdown_education', 'value')
   ])

def uptade_cards(selectec_tri, selected_year, selected_local, selected_sex, selected_race, selected_age, selected_education):
    if not selectec_tri or not selected_year or not selected_local or not selected_sex or not selected_race or not selected_age or not selected_education:
        return ["-"] * 33
    
    df_copia = df.copy()
    
    df_copia = df_copia[df_copia['Fonte'] == f'PNADC_{selectec_tri}{selected_year}']
    df_copia = df_copia[df_copia['Local'] == selected_local]
    df_copia = apply_demographic_filters(df_copia, selected_sex, selected_race, selected_age, selected_education)

    df_filtrado = df_copia[['Pessoas em idade ativa', 'Pessoas ocupadas', 'Força de trabalho',
                               'Taxa de desocupação', 'Nível da ocupação', 'Participação',
                               'Renda habitual principal', 'Renda efetiva principal',
                               'Renda habitual total', 'Renda efetiva total']]
    
    if df_copia.empty or df_copia['Pessoas em idade ativa'].iloc[0] == 0:
        return ["N/A"] * 33

    taxa_desocupacao = df_filtrado['Taxa de desocupação'].iloc[0] 
    taxa_desocupacao_format = f'{taxa_desocupacao:.1f}%'.replace(".", ",")

    nivel_ocupacao = df_filtrado['Nível da ocupação'].iloc[0]
    nivel_ocupacao_format = f'{nivel_ocupacao:.1f}%'.replace(".", ",")

    taxa_participacao = df_filtrado['Participação'].iloc[0]
    taxa_participacao_format = f'{taxa_participacao:.1f}%'.replace(".", ",")

    pia = df_filtrado['Pessoas em idade ativa'].iloc[0]
    pia_format = f'{pia:,}'.replace(',','.')
    
    ocupados = df_filtrado['Pessoas ocupadas'].iloc[0]
    ocupados_format = f'{ocupados:,}'.replace(',','.')

    forca = df_filtrado['Força de trabalho'].iloc[0]
    forca_format = f'{df_filtrado['Força de trabalho'].iloc[0]:,}'.replace(',','.')

    desocupados = forca - ocupados
    desocupados_format = f'{desocupados:,}'.replace(',','.')

    princ_hab = df_filtrado['Renda habitual principal'].iloc[0]
    princ_hab_format = f'R$ {princ_hab:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

    princ_efet = df_filtrado['Renda efetiva principal'].iloc[0]
    princ_efet_format = f'R$ {princ_efet:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

    total_hab = df_filtrado['Renda habitual total'].iloc[0]
    total_hab_format = f'R$ {total_hab:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

    total_efet = df_filtrado['Renda efetiva total'].iloc[0]
    total_efet_format = f'R$ {total_efet:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

############################################################################################################################
    df_copia_ant = df.copy()

    df_copia_ant = df_copia_ant[df_copia_ant['Fonte'] == f'PNADC_{selectec_tri}{int(selected_year)-1}']
    df_copia_ant = df_copia_ant[df_copia_ant['Local'] == selected_local]
    df_copia_ant = apply_demographic_filters(df_copia_ant, selected_sex, selected_race, selected_age, selected_education)
    df_filtrado_ant = df_copia_ant[['Pessoas em idade ativa', 'Pessoas ocupadas', 'Força de trabalho',
                               'Taxa de desocupação', 'Nível da ocupação', 'Participação',
                               'Renda habitual principal', 'Renda efetiva principal',
                               'Renda habitual total', 'Renda efetiva total']]

    if not df_copia_ant.empty:
        taxa_desocupacao_ant = df_filtrado_ant['Taxa de desocupação'].iloc[0]
        tx_desc_dif = format(taxa_desocupacao, taxa_desocupacao_ant,'',' p.p.',1)[0]
        tx_desc_porc = format(taxa_desocupacao, taxa_desocupacao_ant,'','%',1)[1]

        nivel_ocupacao_ant = df_filtrado_ant['Nível da ocupação'].iloc[0]
        nv_ocup_dif = format(nivel_ocupacao, nivel_ocupacao_ant,'',' p.p.',1)[0]
        nv_ocup_porc = format(nivel_ocupacao, nivel_ocupacao_ant,'','%',1)[1]

        taxa_participacao_ant = df_filtrado_ant['Participação'].iloc[0]
        tx_part_dif = format(taxa_participacao, taxa_participacao_ant,'',' p.p.',1)[0]
        tx_part_porc = format(taxa_participacao, taxa_participacao_ant,'','%',1)[1]

        pia_ant = df_filtrado_ant['Pessoas em idade ativa'].iloc[0]
        pia_dif = format(pia, pia_ant,'','',0)[0]
        pia_porc = format(pia, pia_ant,'','%',1)[1]
        
        ocupados_ant = df_filtrado_ant['Pessoas ocupadas'].iloc[0]
        ocupados_dif = format(ocupados, ocupados_ant,'','',0)[0]
        ocupados_porc = format(ocupados, ocupados_ant,'','%',1)[1]

        forca_ant = df_filtrado_ant['Força de trabalho'].iloc[0]
        forca_dif = format(forca, forca_ant,'','',0)[0]
        forca_porc = format(forca, forca_ant,'','%',1)[1]

        desocupados_ant = forca_ant - ocupados_ant
        desocupados_dif = format(desocupados, desocupados_ant,'','',0)[0]
        desocupados_porc = format(desocupados, desocupados_ant,'','%',1)[1]

        princ_hab_ant = df_filtrado_ant['Renda habitual principal'].iloc[0]
        princ_hab_dif = format(princ_hab, princ_hab_ant,'R$ ','',2)[0]
        princ_hab_porc = format(princ_hab, princ_hab_ant,'','%',1)[1]

        princ_efet_ant = df_filtrado_ant['Renda efetiva principal'].iloc[0]
        princ_efet_dif = format(princ_efet, princ_efet_ant,'R$ ','',2)[0]
        princ_efet_porc = format(princ_efet, princ_efet_ant,'','%',1)[1]

        total_hab_ant = df_filtrado_ant['Renda habitual total'].iloc[0]
        total_hab_dif = format(total_hab, total_hab_ant,'R$ ','',2)[0]
        total_hab_porc = format(total_hab, total_hab_ant,'','%',1)[1]

        total_efet_ant = df_filtrado_ant['Renda efetiva total'].iloc[0]
        total_efet_dif = format(total_efet, total_efet_ant,'R$ ','',2)[0]
        total_efet_porc = format(total_efet, total_efet_ant,'','%',1)[1]
    
    else:
        placeholder = html.Small("-", className="text-muted")

        tx_desc_dif = placeholder
        tx_desc_porc = placeholder
        nv_ocup_dif = placeholder
        nv_ocup_porc = placeholder
        tx_part_dif = placeholder
        tx_part_porc = placeholder
        pia_dif = placeholder
        pia_porc = placeholder
        ocupados_dif = placeholder
        ocupados_porc = placeholder
        forca_dif = placeholder
        forca_porc = placeholder
        desocupados_dif = placeholder
        desocupados_porc = placeholder
        princ_hab_dif = placeholder
        princ_hab_porc = placeholder
        princ_efet_dif = placeholder
        princ_efet_porc = placeholder
        total_hab_dif = placeholder
        total_hab_porc = placeholder
        total_efet_dif = placeholder
        total_efet_porc = placeholder

    return (taxa_desocupacao_format, nivel_ocupacao_format, taxa_participacao_format, 
            pia_format, ocupados_format, forca_format, desocupados_format, 
            princ_hab_format, princ_efet_format, total_hab_format, total_efet_format, 
            tx_desc_dif, tx_desc_porc, nv_ocup_dif, nv_ocup_porc, tx_part_dif, tx_part_porc, 
            pia_dif, pia_porc, ocupados_dif, ocupados_porc, forca_dif, forca_porc, desocupados_dif, desocupados_porc, 
            princ_hab_dif, princ_hab_porc, princ_efet_dif, princ_efet_porc, total_hab_dif, total_hab_porc, total_efet_dif, total_efet_porc)

@app.callback(
   Output('graph', 'figure'),
   [
      Input('dropdown_tri_graph', 'value'),
      Input('dropdown_sex', 'value'),
      Input('dropdown_race', 'value'),
      Input('dropdown_age', 'value'),
      Input('dropdown_education', 'value'),
      Input('dropdown_indicator_graph', 'value')
   ])

def uptade_graph(selectec_tri, selected_sex, selected_race, selected_age, selected_education, selected_indicator):
    
    df_copia_graph = df.copy()
    df_copia_graph['Pessoas desocupadas'] = df_copia_graph['Força de trabalho'] - df_copia_graph['Pessoas ocupadas']
    
    df_copia_graph = df_copia_graph[df_copia_graph['Fonte'].str.contains(f'PNADC_{selectec_tri}')]
    df_copia_graph = apply_demographic_filters(df_copia_graph, selected_sex, selected_race, selected_age, selected_education)

    df_filtrado_graph = df_copia_graph.loc[:, ['Fonte', 'Local', selected_indicator]].copy()
    df_filtrado_graph['Fonte'] = df_filtrado_graph['Fonte'].replace({'PNADC_01':'1° tri. ',
                                                                     'PNADC_02':'2° tri. ',
                                                                     'PNADC_03':'3° tri. ',
                                                                     'PNADC_04':'4° tri. '
                                                                     }, regex = True)

    fig = px.line(
        df_filtrado_graph,
        x = 'Fonte', y = selected_indicator,
        color = 'Local',
        color_discrete_map = {
            'Brasil':'#4688f4',
            'Ceará':'#34a853',
            'Nordeste':'#ff6d01',
            'Minas Gerais':'#f1c232',
            'Município de Fortaleza (CE)':'#073763',
            'Pernambuco':'#a64d79',
            'São Paulo':'#cc0000',
            'Bahia':'#b6e880'
        },
        labels = {'Fonte': 'Período',
                  selected_indicator:selected_indicator,
                  'Local':''}
    )

    fig.update_layout(
        xaxis = dict(
            showgrid = True,
            showline = True,
            linecolor = "rgba(0,0,0,0.1)"
            ),
        xaxis_tickangle = -30,
        xaxis_title = None,
        margin = dict(l=60,
                      r=0,
                      t=0,
                      b=40),
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
        font_color = 'black',
        legend = dict(
        orientation = "h",
        y = -0.25,
        x = 0.5,
        xanchor = "center"
        ),
        uirevision="grafico_regioes"
        )
    
    fig.update_xaxes(showgrid = False)
    
    fig.update_yaxes(
        showgrid = True,
        gridcolor = 'rgba(0,0,0,0.1)'
        )


    return fig

if __name__ == '__main__':
    app.run(debug = False)