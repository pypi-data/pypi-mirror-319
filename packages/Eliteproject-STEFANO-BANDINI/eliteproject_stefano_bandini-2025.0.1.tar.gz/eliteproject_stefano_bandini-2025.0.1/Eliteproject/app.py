import os
import io
import webbrowser
import pandas as pd
from dash import Dash, Input, Output, dash_table, dcc, html

from modules.fimport import path_output
find_packages()
# load log file
try:
    file_to_parse = os.path.join(path_output, 'Surgery-Default.log')
    with open(file_to_parse, 'r', encoding='latin1') as file:
        lines = file.readlines()
    data = []
    for line in lines:
        parts = line.split('\t')  # use tab as separator
        if len(parts) >= 6:  # Modify structure of string by splitting timestamp in date and time
            timestamp, level, source, id_info, code, message = parts[:6]
            date, time = timestamp.split('T') if 'T' in timestamp else (timestamp, '')
            data.append({
                'Date': date,
                'Time': time,
                'Level': level,
                'Source': source,
                'ID Info': id_info,
                'Code': code.strip(),
                'Message': message.strip()
            })

    df = pd.DataFrame(data)
    levels = [{'label': lvl, 'value': lvl} for lvl in sorted(df['Level'].dropna().unique())]
    sources = [{'label': src, 'value': src} for src in sorted(df['Source'].dropna().unique())]
    codes = [{'label': code, 'value': code} for code in sorted(df['Code'].dropna().unique())]
    print("DataFrame columns:", df.columns)
    
    if not df.empty:
        url = "http://127.0.0.1:8050"
        webbrowser.open_new(url)
    
    
except Exception as e:
    print(f"Unable to read file: {e}")
    df = pd.DataFrame()
    levels = sources = codes = []
    

# Create app Dash
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Elite Log Viewer"

# Level available (update with real value)
levels = []
for lvl in sorted(df['Level'].dropna().unique()):
    levels.append({'label': lvl, 'value': lvl})

# Layout
app.layout = html.Div([
    html.H1("Elite Log Viewer"),
    html.Div([
        dcc.DatePickerSingle(
            id='filter-date',
            placeholder='date',
            display_format='YYYY-MM-DD',
            style = {
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '10px',
                'verticalAlign': 'middle',
            },
        ),
        html.Div([
            html.Label("Level filter"),
            dcc.Checklist(
                id='filter-level',
                options=levels,
                value=[],  # intial selected values
                inline=False,  # checkbox inline orizontal
            ),
        ]),
        dcc.Dropdown(
            id='filter-source',
            options=sources,
            placeholder='Filtro Source',
            style = {
                'width': 200,
                'height': 25,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '12px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
        dcc.Dropdown(
            id='filter-code',
            options=codes,
            placeholder='Code filter',
            style = {
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '12px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
        dcc.Input(
            id='search-message',
            type='text',
            placeholder='Message filter',
            style = {
                'width': 200,
                'height': 30,
                'border-color': '#DFE6E9',
                'textAlign': 'left',
                'font-size': '14px',
                'verticalAlign': 'middle',
                'margin-top': 10,
            },
        ),
    ], style={'margin-bottom': '20px'}),

    dash_table.DataTable(
        id='log-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=50,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{Level} = "emerg"'},
                'backgroundColor': 'red',
                'color': 'white',  # white text
            },
            {
                'if': {'filter_query': '{Level} = "alert"'},
                'backgroundColor': 'pink',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Level} = "crit"'},
                'backgroundColor': 'lightblue',
                'color': 'black',
            }
        ]
    )
])

    # Callback for updating the table
@app.callback(
    Output('log-table', 'data'),
    [
        Input('filter-date', 'date'),
        Input('filter-level', 'value'),
        Input('filter-source', 'value'),
        Input('filter-code', 'value'),
        Input('search-message', 'value')
    ]
)
def update_table(filter_date, filter_levels, filter_source, filter_code, search_message):
    filtered_df = df

    if filter_date:
        filtered_df = filtered_df[filtered_df['Date'] == filter_date]
    if filter_levels:  # multiple filter from values
        filtered_df = filtered_df[filtered_df['Level'].isin(filter_levels)]
    if filter_source:
        filtered_df = filtered_df[filtered_df['Source'] == filter_source]
    if filter_code:
        filtered_df = filtered_df[filtered_df['Code'] == filter_code]
    if search_message:
        filtered_df = filtered_df[filtered_df['Message'].str.contains(search_message, case=False, na=False)]

    return filtered_df.to_dict('records')


if __name__ == "__main__":
    app.run_server(debug=False)
    
exit()
