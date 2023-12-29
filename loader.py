import io
import json


def unescape_messenger(text):
    if text is None:
        return None
    out = io.StringIO()
    sz = len(text)
    unicode = ""
    had_slash = False
    in_unicode = False
    for i in range(sz):
        ch = text[i]
        if in_unicode:
            unicode += ch
            if len(unicode) == 4:
                try:
                    value = int(unicode, 16)
                    out.write(chr(value))
                    unicode = ""
                    in_unicode = False
                    had_slash = False
                except ValueError:
                    pass
            continue
        if had_slash:
            had_slash = False
            if ch == 'u':
                in_unicode = True
            else:
                out.write("\\")
                out.write(ch)
            continue
        elif ch == '\\':
            had_slash = True
            continue
        out.write(ch)
    if had_slash:
        out.write('\\')
    return out.getvalue()


def get_messenger_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        badly_encoded = f.read()
    unescaped = unescape_messenger(badly_encoded)
    bytes_data = unescaped.encode('iso-8859-1')
    fixed = bytes_data.decode('utf-8')
    return json.loads(fixed)
