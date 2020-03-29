import dash
import datetime
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas_datareader.data as web
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import plotly.express as px
import re

#CSS
colors = {
    'background': '#FEFFFC',
    'text': '#0F4D7A',
    'highlight':'#EC6F00',
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight':'bold',
    'backgroundColor':colors['background'],
    'color':colors['text']
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': colors['background'],
    'color': colors['highlight'],
    'fontWeight':'bold',
    'padding': '6px'
}

def getNumbers(str): 
    array = re.findall(r'[0-9]+', str) 
    return array 
def output_update(value):
	return value


#stylesheets
external_stylesheets2 = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = ["https://www.w3schools.com/w3css/4/w3.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets2)

# Importing Covid19 India dataset
df = pd.read_csv("covid_19_india.csv")
df.reset_index(inplace  = True)
df.set_index("Date",inplace = True)
df = df.drop("Sno", axis = 1)


#Importing data from healthcare.Gov.in website
df2 = pd.read_html("https://www.mohfw.gov.in")
covid_df1 = df2[7]
covid_df1.reset_index(inplace = True)
covid_df1.set_index("S. No.", inplace = True, drop = True)
covid_df1 = covid_df1.drop("index", axis = 1)
covid_df = covid_df1.iloc[0:21]

#converting the "Cases" columns to int
covid_df['Total Confirmed cases ( Foreign National )']=covid_df['Total Confirmed cases ( Foreign National )'].astype(int)
covid_df['Total Confirmed cases (Indian National)']=covid_df['Total Confirmed cases (Indian National)'].astype(int)

#adding a new column - TotalCases
covid_df['TotalCases'] = covid_df['Total Confirmed cases ( Foreign National )'] + covid_df['Total Confirmed cases (Indian National)']

#Data for pie chart
df_pie = pd.DataFrame(covid_df['Total Confirmed cases ( Foreign National )'])
df_pie['Total Confirmed cases (Indian National)'] = covid_df['Total Confirmed cases (Indian National)']
data1 = covid_df1.loc['Total number of confirmed cases in India']['Total Confirmed cases (Indian National)']


if type(data1) == np.int64:
    data1_f = int(data1)
else:
    data1_n = getNumbers(data1)
    for i in data1_n:
        data1_f = int(i)


    


#data1 = int(data1_f)
data2 = covid_df1.loc['Total number of confirmed cases in India']['Total Confirmed cases ( Foreign National )']

if type(data2) == np.int64:
    data2_f = int(data2)
else:
    data2_n = getNumbers(data2)
    for i in data2_n:
        data2_f = int(i)





    




#Data for economic trending
stock ='EURINR=X'
stock1 = 'INR=X'
stock2 = 'GBPINR=X'
inter_stock1 = '^GSPC'
inter_stock2 = 'IMOEX.ME'
inter_stock3 = '^STOXX50E'
start = datetime.datetime(2020,1,1)
end = datetime.datetime.now()
data_src = "yahoo"
#INDIAN STOCKS
#Dollar
usd_df = web.DataReader(stock1, data_src, start, end)
usd_df.reset_index(inplace = True)
usd_df.set_index("Date", inplace =True)
usd_df = usd_df.drop("Adj Close", axis = 1)

#Euros
euro_df = web.DataReader(stock,data_src, start, end)
euro_df.reset_index(inplace=True)
euro_df.set_index("Date",inplace=True)
euro_df = euro_df.drop("Adj Close",axis=1)


#INTERNATIONAL STOCKS
#NASDAQ
nasdaq_df = web.DataReader(inter_stock1,data_src, start, end)
nasdaq_df.reset_index(inplace = True)
nasdaq_df.set_index("Date", inplace = True)
nasdaq_df = nasdaq_df.drop("Adj Close", axis = 1)
#FTSE
ftse_df = web.DataReader(inter_stock2,data_src, start, end)
ftse_df.reset_index(inplace = True)
ftse_df.set_index("Date", inplace = True)
ftse_df = ftse_df.drop("Adj Close", axis = 1)
#CAC
cac_df = web.DataReader(inter_stock3,data_src, start, end)
cac_df.reset_index(inplace = True)
cac_df.set_index("Date", inplace = True)
cac_df = cac_df.drop("Adj Close", axis = 1)



#Comparing various epidemics and pandemics
mortality = pd.read_html("https://docs.google.com/spreadsheets/d/1g_YxmDfQx7aOU2DKzNZo9b-NTk62Bju6X3z6OuCa6gw/htmlview#")

pd_mortality = mortality[9]
final_pd = pd_mortality[4:]



final_pd = final_pd.drop(["Unnamed: 0","Unnamed: 2"],axis= 1)
final_pd = final_pd.rename({'A':'Disease','B':'Average Deaths/Day(global)',
                           'E':'Fatality rate','F':'infectiousness',
                            'G':'Total Fatalities','H':'Total cases',
                           'C':'Total news mentions'},axis = 1)

final_pd = final_pd.drop(["D","I","J","K","L","M","N"],axis = 1)
final_pd = final_pd.drop(["O","P","Q"],axis = 1)

final_pd.set_index("Disease",inplace = True, drop=True)
final_pd.at['Pneumonia','Total cases'] = 450000000
final_pd.at['Rotavirus','Total cases'] = 3000000
final_pd.at['SARS','Total cases'] = 8000
final_pd.at['Ebola','Total cases'] = 28000                           

final_pd = final_pd.drop(["Swine Flu H1N1 2009","Norovirus","Pneumonia","Malaria","Shigellosis","Chicken Pox","Hepatitis B","Hepatitis A","Dengue Fever"], axis = 0) 

#Total Coronavirus cases-Worldwide
data10 = pd.read_html("https://www.worldometers.info/coronavirus/")

world_covid = data10[0]


world_covid = world_covid.drop(['NewCases'],axis = 1) 
world_covid = world_covid.drop(['NewDeaths','Tot\xa0Cases/1M pop'],axis = 1) 
world_covid.set_index("Country,Other",inplace = True, drop = True)
world_covid = world_covid.fillna(0)
final_world_covid = world_covid[0:50]






# Trend graph for Covid19-India data
app.layout = html.Div(style={'background-color':colors['background'],'color':'black','font-family':'Verdana', 'padding':'50px'},
    children=[
	#html.H1(children="COVID-19 INDIA", style={'textAlign':'center','color':colors['highlight']}),
	 dcc.Tabs(id="tabs-example", value='tab-1-example', 
	 	children=[
        dcc.Tab(label='INDIA', value='tab-1-example', style = tab_style, selected_style = tab_selected_style),
        dcc.Tab(label='WORLD', value='tab-2-example',style = tab_style, selected_style = tab_selected_style),
    ], colors = {
    	"border":colors['background'],
    	"primary": "orange",
    	"background":colors['background']}
    	),
    html.Div(id='tabs-content-example'),
    
    
    
	
	])
	
   
  


def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
        	html.H2(children="COVID-19 INDIA", style={'textAlign':'center','color':colors['highlight']}),
        	dcc.Dropdown(
        		id= "stock-input",
    options=[
        {'label': 'United States Dollar', 'value': stock},
        {'label': 'Euros', 'value': stock1},
        {'label': 'Pound Sterling', 'value': stock2}
    ],
    value=[stock],
    multi=True
)  ,
        	 html.Div(id='dd-output-container'),
        	dcc.Graph(
		id="economy",
		figure = {
		'data':[
		{"x":usd_df.index,'y':usd_df.Close,'mode':'lines','name':' usd'},
		{'x':euro_df.index,'y':euro_df.Close,'mode':'lines','name':'euro'}
			],
		 'layout': {'title':'CURRENCIES',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }




		),
    #Bar Graph for number of cases in India
	html.Div([
		html.Div([
			dcc.Graph(
        id='example-graph-2',
        style = {
        'height': 500,
        'width': 700
        
                },
        figure={
            'data': [
                {'x': covid_df['Name of State / UT']  , 'y':   covid_df['TotalCases'], 'type': 'bar', 'name': 'Total cases'},
                {'x': covid_df['Name of State / UT']  , 'y':  covid_df['Death'], 'type': 'bar', 'name': u'Death'},
            ],

           'layout': {
              'plot_bgcolor': colors['background'],
	         'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
           }
        }
)
			], className = "seven columns"),

 html.Div([dcc.Graph(
        id="piechart",
        style = {
        'height': 500,
        'width': 400,
        'display':'inline-block'
        },
        figure={
            "data": [
                {
                    "labels": ['Indians','Foreigners'],
                    "values": [data1_f,data2_f],
			"type": "pie",
                   "marker": {"line": {"color": "#111110", "width": 1}},
                  "hoverinfo": ['data1','data2'],
                  #"textinfo": "label",
                  "legend":"lables",
              }
          ],
          "layout": {
              "margin": dict(l=10, r=10, t=10, b=10),
             "showlegend": True,
            "paper_bgcolor": colors['background'],
               "plot_bgcolor": colors['background'],
               "font": colors['text'],
                "autosize": True,
            },
        },
    )
    ],className= "five columns")
   ], className = "row")

#Pie chart for number of Indian nationals and foreign Nationals	
    


])




    elif tab == 'tab-2-example':
        return html.Div([

        	dcc.Graph(
		id="economy",
		figure = {
		'data':[
		{"x":nasdaq_df.index,'y':nasdaq_df.Close,'mode':'lines','name':'S&P 500'},
		{'x':ftse_df.index,'y':ftse_df.Close,'mode':'lines','name':'MOEX Russia'},
		{'x':cac_df.index,'y':cac_df.Close,'mode':'lines','name':'ESTX 50 EUR'}

			],
		 'layout': {'title':'GLOBAL STOCKS INDICES',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }),

        	html.Div([
        		html.Div([
        			dcc.Graph(
    	id = "Disease mortality rate",
    	style = {
    	'height':600,
    	'width':800

   	},
   	figure = {
   	"data":[{'x':final_pd.index,'y':final_pd['Total cases'],'type':'bar','name':'diseases-total cases'}],
   	  'layout': {'title':'MORTALITY RATES OF VARIOUS DISEASES',
               'plot_bgcolor': colors['background'],
              'paper_bgcolor': colors['background'],
               'font': {
                   'color': colors['text']
               }
           }




    	}
    	)

        			], className = "six columns"),

        html.Div([
        	 dcc.Graph(
    	id = "number of worldwise cases",
    	style = {
    	'height':600,
    	'width':700

   	},
   	figure = {
   	"data":[{'x':final_world_covid.index,'y':final_world_covid['TotalCases'],'type':'bar','name':'Covid19 confirmed cases'},
   	{'x':final_world_covid.index,'y':final_world_covid['Serious,Critical'],'type':'bar','name':'Covid19 Critical cases'}],
   	  'layout': {'title':'TOTAL COVID19 CASES - WORLDWIDE',
               'plot_bgcolor': colors['background'],
              'paper_bgcolor': colors['background'],
               'font': {
                   'color': colors['text']
               }
           }

		}
    )
       

            
        ], className = "six columns")
        ], className = "row")
]) 



@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')],
              Output('economy', 'figure'),
    		  [Input('stock-input', 'value')]

              )

def update_fig(input_values):
	data =[]
	trace_close = go.Scatter(x = list(df.index), y=list(df.Close)
		,name = 'Close')
	data.append(trace_close)

	layout = {
			'title':'Stoncks graphs'


	}

	return {
	'data':data,
	'layout':layout

	}



if __name__=="__main__":
	app.run_server(port = 8016, debug = True)