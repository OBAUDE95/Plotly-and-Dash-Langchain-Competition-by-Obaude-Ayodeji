import dash
from dash import dcc, html, Input, Output, State
import base64
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
import dash_bootstrap_components as dbc


##define  app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server 
app.layout = dbc.Container([dbc.Row([
    dbc.Col([dbc.Card([
                dbc.CardHeader("Financial Report Summarizer by Obaude Ayodeji with Plotly and Dash", style={'fontSize': '27px'}),
        
            ])])
    
]),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ,dcc.Store(id='store', data=[])]),
                multiple=False,
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '20px 0'
                }
            ),
            dbc.Card([
                dbc.CardHeader("Earnings Report Summary"),
                dbc.CardBody([dcc.Markdown(id='text', style={'whiteSpace': 'pre-line'})])
            ]),
            dbc.Card([
                dbc.CardHeader("Risks and Opportunities"),
                dbc.CardBody([dcc.Markdown(id='text2', style={'whiteSpace': 'pre-line'})])
            ]),
            dbc.Card([
                dbc.CardHeader("Ask a Question Concerning the uploaded file"),
                dbc.CardBody([dcc.Input(id='input', debounce=True)])
            ]),
            dbc.Card([
                dbc.CardHeader("Response"),
                dbc.CardBody([dcc.Markdown(id='text3', style={'whiteSpace': 'pre-line'})])
            ]),
        ], width=8),
    ], className="mt-4"),
])


###storing data into dcc.store
def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    return decoded.decode('utf-8')
@app.callback(Output('store', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is None:
        return "No data uploaded"

    try:
        content = parse_contents(contents)
        return content

    except Exception as e:
        return 'There was an error processing this file.'

    
    
@app.callback(Output('text', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def receive_summary(data,filename):
        if len(data)!= 0:
            prompt = ChatPromptTemplate.from_template("Provide a brief and short summary of the key financial insights and findings from the {foo} earnings report . Highlight total revenue, expenses, profits, significant trends, and future outlook. Tailor the summary for stakeholders, investors, and decision-makers, please make it concise")
            model = ChatOpenAI(openai_api_key=Enter_Api_key)
            chain = prompt | model
            result = chain.invoke({'foo': data}).content.replace('\n', '')
            return result
        else:
            return None

@app.callback(Output('text2', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def receive_risks_opportunities(contents, filename):
    if contents is not None:
        # Process the uploaded data
        data = parse_contents(contents)
        
        prompt = ChatPromptTemplate.from_template("Summarize the identified risks and opportunities from the {foo} earnings report. Provide insights into potential challenges, market risks, and factors that may impact future performance. Additionally, highlight opportunities for growth, strategic initiatives, and areas where the company can capitalize for improvement. , please make it concise")
        model = ChatOpenAI(openai_api_key=Enter_Api_key)
        chain = prompt | model
        result = chain.invoke({'foo': data}).content.replace('\n', '')
        return result
    else:
        return None  # or an empty string or any other value you prefer


## query 
@app.callback(Output('text3', 'children'),
              Input('store', 'data'),
              Input('input', 'value'),
             State('upload-data', 'filename'),
             prevent_initial_call=True)
def query(data, value,filename):
    
    if value is not None:
        prompt = ChatPromptTemplate.from_template("{new_query} {foo} earnings report. make it concise")
        model = ChatOpenAI(openai_api_key=Enter_Api_key)
        chain = prompt | model
        result = chain.invoke({'foo': data, 'new_query': value}).content.replace('\n', '')
        return result
    else:
        return None
       

if __name__ == '__main__':
    app.run_server(port=770, debug=True)
