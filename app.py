

import dash
from dash import dcc, html, Input, Output, State
import base64
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import dash_bootstrap_components as dbc

api ="Enter your api key here
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = dbc.Container([
    dbc.Row([
        dbc.Card([
            dbc.CardHeader("Financial Report Summarizer by Obaude Ayodeji with Plotly and Dash", style={'fontSize': '27px'}),
            dbc.CardBody([dcc.Markdown(id='dataname', style={'whiteSpace': 'pre-line'})])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Store(id='store2', data=[]),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    , dcc.Store(id='store', data=[])
                ]),
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


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return decoded.decode('utf-8')


def generate_response(data, fallback="No data uploaded"):
    return fallback if 'No data uploaded' in data else data


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

#saving filename
@app.callback(Output('store2', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is None:
        return "No data uploaded"

    try:
        content = filename.split('.')[0]
        return content
    except Exception as e:
        return 'There was an error processing this file.'




#no need
@app.callback(Output('dataname', 'children'),
              Input('store2', 'data'))
def receive_summary(data):
    return generate_response(data)


@app.callback(Output('text', 'children'),
              Input('store', 'data')
              )
def receive_summary(data):
        if 'No data uploaded' not in data:
            prompt = ChatPromptTemplate.from_template("Provide a brief and short summary of the key financial insights and findings from the {foo} earnings report . Highlight total revenue, expenses, profits, significant trends, and future outlook. Tailor the summary for stakeholders, investors, and decision-makers, please make it concise")
            model = ChatOpenAI(openai_api_key=api)
            chain = prompt | model
            result = chain.invoke({'foo': data}).content.replace('\n', '')
            return result
        else:
            return 'No Data uploaded'


@app.callback(Output('text2', 'children'),
              Input('store', 'data'))

def receive_risks_opportunities(contents):
    if 'No data uploaded' not in contents:
        # Process the uploaded data

        prompt = ChatPromptTemplate.from_template("Summarize the identified risks and opportunities from the {foo} earnings report. Provide insights into potential challenges, market risks, and factors that may impact future performance. Additionally, highlight opportunities for growth, strategic initiatives, and areas where the company can capitalize for improvement. , please make it concise")
        model = ChatOpenAI(openai_api_key=api)
        chain = prompt | model
        result = chain.invoke({'foo': contents}).content.replace('\n', '')
        return result
    else:
        return 'No data Uploaded'  # or an empty string or any other value you prefer


## query
@app.callback(Output('text3', 'children'),
              Input('store', 'data'),
              Input('input', 'value')

             )
def query(data, value):

    if  value is not None:
        prompt = ChatPromptTemplate.from_template("{new_query} {foo} earnings report. make it concise")
        model = ChatOpenAI(openai_api_key=api)
        chain = prompt | model
        result = chain.invoke({'foo': data, 'new_query': value}).content.replace('\n', '')
        return result
    else:
        return 'No data uploaded'


if __name__ == '__main__':
    app.run_server(port=770, debug=True)
