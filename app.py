import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
url_mapping = {}

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Upgraded UI with Modern CSS (Tailwind-inspired)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkShrink | Modern URL Shortener</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --accent: #6366f1;
            --text: #f8fafc;
            --secondary: #94a3b8;
        }
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: var(--card);
            padding: 2.5rem;
            border-radius: 1rem;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 450px;
            text-align: center;
            border: 1px solid #334155;
        }
        h1 { font-size: 1.8rem; margin-bottom: 0.5rem; color: var(--accent); }
        p { color: var(--secondary); margin-bottom: 2rem; font-size: 0.9rem; }
        input[type="text"] {
            width: 100%;
            padding: 0.8rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #334155;
            background: #0f172a;
            color: white;
            box-sizing: border-box;
            outline: none;
        }
        input[type="text"]:focus { border-color: var(--accent); }
        button {
            width: 100%;
            padding: 0.8rem;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        .result {
            margin-top: 2rem;
            padding: 1rem;
            background: #0f172a;
            border-radius: 0.5rem;
            border-left: 4px solid var(--accent);
        }
        .result a { color: var(--accent); text-decoration: none; word-break: break-all; }
        footer { margin-top: 2rem; font-size: 0.75rem; color: #475569; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 LinkShrink</h1>
        <p>Shorten your long URLs instantly.</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste your long link here..." required>
            <button type="submit">Shorten URL</button>
        </form>
        
        {% if short_url %}
        <div class="result">
            <span style="display:block; font-size: 0.8rem; margin-bottom: 5px; color: var(--secondary);">Your short link:</span>
            <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
        {% endif %}

        <footer>Developed by Axdrmk99</footer>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('url')
        # Simple input check
        if not long_url.startswith(('http://', 'https://')):
            long_url = 'https://' + long_url
        
        short_id = generate_short_id()
        url_mapping[short_id] = long_url
        short_url = f"{request.host_url}{short_id}"
    
    return render_template_string(HTML_TEMPLATE, short_url=short_url)

@app.route('/<short_id>')
def redirect_to_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
