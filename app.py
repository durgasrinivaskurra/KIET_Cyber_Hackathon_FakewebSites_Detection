# Import the required modules
from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import requests

app = Flask(__name__)

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to check the number of redirects for a URL
def get_redirect_count(url):
    try:
        response = requests.get(url, allow_redirects=True)
        redirect_count = len(response.history)
        return redirect_count

    except requests.RequestException:
        return 0



# Function to determine if a link is potentially a phishing link
def is_phishing_link(url):
    redirect_count = get_redirect_count(url)
    return redirect_count > 0

# Flask route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route for checking links
@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    urls = data.get('urls', [])

    results = {}
    
    for url in urls:
        is_valid = is_valid_url(url)
        is_phishing = is_phishing_link(url)

        if is_valid:
            result = 'Real'+'\n' "this a safe link"   
            if is_phishing:
                result += ' (Potentially Phishing)'
        else:
            result = 'Fake'+'\n' "this is not a safe link"
        
        results[url] = result
    
    return jsonify({'results': results})

# Function to test the request
def test_request():
    sample_urls = [
        "http://example.com",
        "https://www.google.com",
        "http://www.phishingsite.com",
        "https://www.github.com"
    ]

    payload = {'urls': sample_urls}
    response = requests.post('http://localhost:5000/check', json=payload)

    print("Response:", response.json())

if __name__ == '__main__':
    app.run(debug=True)
    # Uncomment the line below to test the request
    # test_request()
