import dash_bootstrap_components as dbc
from dash import html, dcc


def create_header():
    """header section"""
    return html.Header(
        [
            html.H1('Textanalyse Tool'),
            html.H4(
                "Analysieren Sie die Satzzeichen Ihres Textes.",
                className="text-muted"
            )
        ],
        className="page-header pt-4",
    )


def create_text_area():
    """text area section"""
    return dcc.Textarea(
        className="form-label height-10rem",
        placeholder="Kopieren Sie Ihren Text hier hinein und führen Sie das Programm aus.",
        id="textarea",
        value="",
    )


def create_interface():
    """interface section (buttons and switches)"""
    return [
        html.Div(
            html.Button(
                'Ausführen',
                id='submission-button',
                n_clicks=0,
                className="btn btn-primary  btn-lg"
            ),
            className="col-auto"
        ),
        html.Div(
            dbc.Checklist(
                options=[
                    {"label": "feste Zeilenumbrüche für Darstellung übernehmen", "value": "hasHardLineBreaks"},
                    {"label": "Leerzeichen für Darstellung zwischen Satzzeichen einfügen", "value": "hasBlanks"}
                ],
                value=[2],
                id="switches-input",
                switch=True
            ),
            className="col-auto"
        ),
        html.Div(
            dbc.Alert(
                id="alert",
                className="mb-0 alert",
                is_open=False,
                duration=2000
            ),
            className="col-auto"
        )
    ]


def create_table(all_marks, num_phrases):
    """accordion item table"""
    table_header = html.Thead(html.Tr([html.Th("Zeichen"), html.Th("Total"), html.Th("Pro Satz")]))

    marks = []
    total = []
    per_phrase = []
    sorted_marks = dict(sorted(all_marks.items(), key=lambda item: item[1], reverse=True))
    for mark, num in sorted_marks.items():
        if num > 0:
            marks.append(mark)
            total.append(num)
            per_phrase.append(round(num / num_phrases, 2))

    table_body = html.Tbody(
        [
            html.Tr(
                [html.Td(marks[row]), html.Td(total[row]), html.Td(per_phrase[row])]
            )
            for row in range(len(marks))
        ]
    )

    return dbc.Table([table_header, table_body], bordered=True)


def create_analysis():
    """analysis section"""
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem('Anzahl Zeichen (mit Leerzeichen): ', id="num-all-characters"),
                        dbc.ListGroupItem("Anzahl Zeichen (ohne Leerzeichen): ", id="num-characters"),
                        dbc.ListGroupItem("Anzahl Satzzeichen: ", id="num-marks"),
                        dbc.ListGroupItem("Anzahl Wörter: ", id="num-words"),
                        dbc.ListGroupItem("Anzahl Sätze: ", id="num-phrases"),
                        dbc.ListGroupItem("Anzahl Paragraphen: ", id="num-paragraphs"),
                    ]
                ),
                title="Übersicht"
            ),
            dbc.AccordionItem(
                html.Div(
                    [
                        html.H6("Dies sind die Satzzeichen in Ihrem Text: ", className="text-muted"),
                        html.P(id='mark-text', className="white-space"),
                        dcc.Clipboard(target_id="mark-text", className="spacing")
                    ],
                    className="form-floating"
                ),
                title="Reihenfolge der Satzzeichen"
            ),
            dbc.AccordionItem(
                html.Div(create_table({}, 0), id="table-container"),
                title="Anzahl pro Typ"
            ),
        ]
    )


def create_footer():
    """footer section"""
    return html.Footer(
        [
            html.A("Von Luzian Trapletti | Copyright © 2022 Luzian Trapletti"),
        ],
        className="text-center"
    )


def create_layout(app):
    """main layout"""
    app.layout = html.Div(
        [
            html.Div(create_header(), className="row mb-4"),
            html.Div(create_text_area(), className="row mb-4"),
            html.Div(create_interface(), className="row mb-4 min-height-58px"),
            html.Div(create_analysis(), className="row mb-4"),
            html.Div(create_footer(), className="row mb-4")
        ],
        className="container"
    )
