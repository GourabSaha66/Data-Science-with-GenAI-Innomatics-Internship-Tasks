from flask import Flask, render_template, request
import re
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    test_string = ""
    regex_pattern = ""
    error = None
    exec_time = 0

    if request.method == 'POST':
        test_string = request.form.get('test_string', '')
        regex_pattern = request.form.get('regex_pattern', '')

        if regex_pattern:
            try:
                start_time = time.time()
                matches = list(re.finditer(regex_pattern, test_string))
                
                for i, match in enumerate(matches, 1):
                    results.append({
                        'id': i,
                        'text': match.group(),
                        'start': match.start(),
                        'end': match.end()
                    })
                
                exec_time = round((time.time() - start_time) * 1000, 3)
            except re.error as e:
                error = str(e)

    return render_template('index.html', 
                           results=results, 
                           test_string=test_string, 
                           regex_pattern=regex_pattern, 
                           error=error,
                           exec_time=exec_time)

if __name__ == '__main__':
    app.run(debug=True)