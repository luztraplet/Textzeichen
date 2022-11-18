from dash import Output, Input, State, callback_context
from dash.exceptions import PreventUpdate

from src.framework.ui import create_table


def add_callback(app):
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
        """callback function"""
        ctx = callback_context
        if ctx.triggered[0]["prop_id"] == "submission-button.n_clicks":
            return get_text_stats(textarea, switches)
        raise PreventUpdate


def get_text_stats(input_text: str, switches: list):
    """main analysis function"""
    all_marks = {'\\': 0, ')': 0, ';': 0, '<': 0, '…': 0, '«': 0, ',': 0, '.': 0, '/': 0, '-': 0, '|': 0, '~': 0,
                 '•': 0, '‚': 0, '»': 0, '*': 0, '=': 0, '·': 0, '´': 0, '#': 0, '„': 0, '>': 0, '@': 0, '(': 0, "'": 0,
                 'Ꞌ': 0, '’': 0, '‹': 0, '[': 0, '‐': 0, '°': 0, '%': 0, '?': 0, '¦': 0, '+': 0, ']': 0, '›': 0, '§': 0,
                 '"': 0, '¨': 0, '^': 0, '–': 0, '}': 0, '!': 0, '_': 0, '{': 0, '\n': 0, ':': 0, '“': 0, '‘': 0,
                 '`': 0, '&': 0, '¬': 0, '”': 0, '⟨': 0, '⟩': 0, '●': 0, '◦': 0, '◘': 0, '—': 0, '⁄': 0, '∕': 0, '⧸': 0,
                 '／': 0, '̸': 0, '̷': 0, '〈': 0, '〉': 0, '《': 0, '》': 0, '「': 0, '」': 0, '『': 0, '』': 0, '【': 0, '】': 0,
                 '〔': 0, '〕': 0, '〖': 0, '〗': 0, '〘': 0, '〙': 0, '〚': 0, '〛': 0, '⋮': 0, '⋯': 0, '⋰': 0, '⋱': 0, 'ּ': 0,
                 '᛫': 0, '‧': 0, '∘': 0, '∙': 0, '⋅': 0, '⦁': 0, '⸰': 0, '⸱': 0, '⸳': 0, '・': 0, 'ꞏ': 0, '･': 0, '𐄁': 0,
                 '🞄': 0, '⏺': 0, '‑': 0, '⚫': 0, '⬤': 0, '¿': 0, '‽': 0, '⁇': 0, '⁈': 0, '⁉': 0, '⸘': 0, 'ʼ': 0, 'ˈ': 0,
                 '′': 0, 'ʻ': 0, '⸮': 0, '¡': 0, '≈': 0}

    sentence_ending_marks = ['.', '!', '?', ':']

    has_hard_line_breaks = "hasHardLineBreaks" in switches
    has_blanks = "hasBlanks" in switches

    all_characters = len(input_text.replace(' ', '').replace('\n', ''))
    num_characters = len(input_text)

    num_words = 0
    for word in input_text.split():
        if any(character.isalpha() for character in word):
            num_words += 1

    num_paragraphs = 0
    for paragraph in input_text.splitlines():
        if any(character.isalpha() for character in paragraph):
            num_paragraphs += 1

    text_out_of_marks = ""
    num_phrases = 0
    for character in input_text:
        if character == '\n':
            if has_hard_line_breaks:
                text_out_of_marks += '\n'

        elif character in all_marks:
            text_out_of_marks += character
            all_marks[character] += 1

            if character in sentence_ending_marks:
                num_phrases += 1

            if has_blanks:
                text_out_of_marks += ' '

    sum_marks = sum(all_marks.values())

    if not all_characters:
        alert_value = "Sie haben noch keinen Text eingefügt!"
        alert_type = "mb-0 alert alert-danger"
    else:
        alert_value = 'Statistiken wurden aktualisiert!'
        alert_type = "mb-0 alert"

    return [
        text_out_of_marks,
        f"Anzahl Zeichen (mit Leerzeichen): {num_characters}",
        f"Anzahl Zeichen (ohne Leerzeichen): {all_characters}",
        f"Anzahl Satzzeichen: {sum_marks}",
        f"Anzahl Wörter: {num_words}",
        f"Anzahl Sätze: {num_phrases}",
        f"Anzahl Paragraphen: {num_paragraphs}",
        create_table(all_marks, num_phrases),
        True,
        alert_value,
        alert_type
    ]
