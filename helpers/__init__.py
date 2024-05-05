from datetime import datetime

def remove_consecutive_line_breaks(text):
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')
    return text

def get_session_id():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
