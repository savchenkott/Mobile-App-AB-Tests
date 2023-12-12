from yattag import Doc
from dataset_download import p_value

doc, tag, text = Doc().tagtext()

with tag('html'):
    with tag('body'):
        with tag('h1'):
            text(f'P-value: {p_value}')  # Use an f-string to include p_value
            pass

html = doc.getvalue()

with open('output.html', 'w') as f:
    f.write(html)
