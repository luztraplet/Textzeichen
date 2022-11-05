import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=["assets/bootstrap.css"])
server = app.server

marks = ''');<…«,./-|~•‚»*=·´#„\>@('Ꞌ’‹[‐°%?¦+]›§"¨^–}!_{:“‘`&¬”⟨⟩●◦◘—⁄∕⧸／̸̷〈〉《》「」『』【】〔〕〖〗〘〙〚〛⋮⋯⋰⋱ּ᛫‧∘∙⋅⦁⸰⸱⸳・ꞏ･𐄁🞄⏺‑⚫⬤¿‽⁇⁈⁉⸘ʼˈ′ʻ⸮¡≈'''

# <editor-fold desc="Header">
header = html.Header(
    className="page-header pt-4",
    children=[
        html.H1('Textanalyse Tool'),
        html.H4("Analysieren Sie die Satzzeichen Ihres Textes.",
                className="text-muted")
    ]
)
# </editor-fold>

# <editor-fold desc="Text">
text = dcc.Textarea(
    className="form-label",
    placeholder="Kopieren Sie Ihren Text hier hinein und führen Sie das Programm aus.",
    id='textarea',
    value='',
    style={"height": "10rem"})
# </editor-fold>

# <editor-fold desc="Buttons">
buttons = [
    html.Div(
        html.Button('Ausführen',
                    id='submission-button',
                    n_clicks=0,
                    className="btn btn-primary  btn-lg"),
        className="col-auto"),
    html.Div(
        dbc.Checklist(
            options=[
                {"label": "feste Zeilenumbrüche für Darstellung übernehmen", "value": "hasHardLineBreaks"},
                {"label": "Leerzeichen für Darstellung zwischen Satzzeichen einfügen", "value": "hasBlanks"}],
            value=[2],
            id="switches-input",
            switch=True),
        className="col-auto"),
    html.Div(dbc.Alert(
        id="alert",
        className="mb-0 alert",
        is_open=False,
        duration=2000
    ), className="col-auto")]
# </editor-fold>s

# <editor-fold desc="Analysis">
analysis = dbc.Accordion(
    [
        dbc.AccordionItem(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem('Anzahl Zeichen (mit Leerzeichen): ', id="num-all-characters"),
                    dbc.ListGroupItem("Anzahl Zeichen (ohne Leerzeichen): ", id="num-characters"),
                    dbc.ListGroupItem("Anzahl Satzzeichen: ", id="num-marks"),
                    dbc.ListGroupItem("Anzahl Wörter: ", id="num-words"),
                    dbc.ListGroupItem("Anzahl Sätze: ", id="num-phrases"),
                    dbc.ListGroupItem("Anzahl Paragraphen: ", id="num-paragraphs")
                ]
            ), title="Übersicht"
        ),
        dbc.AccordionItem(html.Div(children=[
            html.H6("Dies sind die Satzzeichen in Ihrem Text: ", className="text-muted"),
            html.P(id='mark-text', style={'whiteSpace': 'pre-line'}),
            dcc.Clipboard(
                target_id="mark-text",
                style={
                    "position": "absolute",
                    "top": 0,
                    "right": 0,
                    "fontSize": 20,
                })], style={"position": "relative"}), title="Reihenfolge der Satzzeichen"),
        dbc.AccordionItem(
            html.Div(id="table-container")
            , title="Anzahl pro Typ"
        ),
    ]
)
# </editor-fold>

# <editor-fold desc="Footer">
footer = html.Footer(style={'textAlign': 'center'},
                     children=[
                         html.A("Von Luzian Trapletti | Copyright © 2022 Luzian Trapletti"),
                     ])
# </editor-fold>


app.layout = html.Div(className="container", children=[
    html.Div(header, className="row mb-4"),
    html.Div(text, className="row mb-4"),
    html.Div(buttons, className="row mb-4", style={"min-height": "58px"}),
    html.Div(analysis, className="row mb-4"),
    html.Div(footer, className="row my-5")
])


@app.callback(
    Output('mark-text', 'children'),
    Output('num-all-characters', 'children'),
    Output('num-characters', 'children'),
    Output('num-marks', 'children'),
    Output('num-words', 'children'),
    Output('num-phrases', 'children'),
    Output('num-paragraphs', 'children'),
    Output('table-container', 'children'),
    Output('alert', 'is_open'),
    Output('alert', 'children'),
    Output('alert', 'className'),
    Input('submission-button', 'n_clicks'),
    Input('switches-input', 'value'),
    State('textarea', 'value')
)
def update_output(_, switches, textarea):
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] == "submission-button.n_clicks":
        return getStats(textarea, switches)
    raise PreventUpdate


def getStats(text, switches):
    global marks
    marksDict = {i: 0 for i in marks}
    hasHardLineBreaks = "hasHardLineBreaks" in switches
    hasBlanks = "hasBlanks" in switches
    characters = len(text.replace(' ', '').replace('\n', ''))
    allCharacters = len(text)
    words = 0
    for i in text.split():
        if any(u.isalpha() for u in i):
            words += 1
    phrases = 0
    paragraphs = 0
    for p in text.splitlines():
        if any(u.isalpha() for u in p):
            paragraphs += 1
    markText = ''
    for character in text:
        if character == '\n':
            if hasHardLineBreaks:
                markText += '\n'
        elif character in marks:
            markText += character
            marksDict[character] += 1
            if character in ['.', '!', '?', ':']:
                phrases += 1
            if hasBlanks:
                markText += ' '

    sumMarks = sum(marksDict.values())
    if characters == 0:
        alertValue = 'Sie haben noch keinen Text eingefügt!'
        alertType = "mb-0 alert alert-danger"
    else:
        alertValue = 'Statistiken wurden aktualisiert!'
        alertType = "mb-0 alert"

    return markText, f"Anzahl Zeichen (mit Leerzeichen): {allCharacters}", f"Anzahl Zeichen (ohne Leerzeichen): {characters}", f"Anzahl Satzzeichen: {sumMarks}", f"Anzahl Wörter: {words}", f"Anzahl Sätze: {phrases}", f"Anzahl Paragraphen: {paragraphs}", createDataFrame(
        phrases, marksDict), True, alertValue, alertType


def createDataFrame(phrases, marksDict):
    col1 = []
    col2 = []
    col3 = []
    m = {k: v for k, v in sorted(marksDict.items(), key=lambda item: item[1], reverse=True)}
    for item in m.items():
        if item[1] > 0:
            col1.append(item[0])
            col2.append(item[1])
            col3.append(round(item[1] / phrases, 2))
    return dbc.Table.from_dataframe(pd.DataFrame({'Zeichen': col1, 'Total': col2, 'Pro Satz': col3}), bordered=True)


if __name__ == '__main__':
    app.run_server()
