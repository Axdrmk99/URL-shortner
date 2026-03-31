import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Dictionary to store our URL mappings
url_mapping = {}

def generate_short_id(length=6):
    """Generates a random string of letters and digits"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Simple HTML template as a string for one-file portability
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>URL Shortener</title></head>
<body>
    <h2>Simple URL Shortener</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter long URL" required>
        <button type="submit">Shorten</button>
    </form>
    {% if short_url %}
        <p>Shortened URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('url')
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
    app.run(debug=True)
