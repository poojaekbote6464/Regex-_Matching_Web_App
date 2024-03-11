from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        regex_pattern = request.form['regex_pattern']
        text_to_search = request.form['text_to_search']
        try:
            matches = re.findall(regex_pattern, text_to_search)
            return redirect(url_for('results', regex_pattern=regex_pattern, matches=matches, text_to_search=text_to_search))
        except re.error as e:
            error_message = str(e)
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

@app.route('/results')
def results():
    regex_pattern = request.args.get('regex_pattern')
    matches = request.args.getlist('matches')
    text_to_search = request.args.get('text_to_search')

    highlighted_text = highlight_matches(regex_pattern, text_to_search)
    
    return render_template('results.html', regex_pattern=regex_pattern, matches=matches, text_to_search=highlighted_text)


@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form['email']
    is_valid = validate_email_address(email)
    return render_template('email_validation.html', email=email, is_valid=is_valid)

def validate_email_address(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def highlight_matches(regex_pattern, text_to_search):
    highlighted_text = re.sub(regex_pattern, r'<span class="highlight">\g<0></span>', text_to_search)
    return highlighted_text

if __name__ == '__main__':
    app.run(debug=True)
