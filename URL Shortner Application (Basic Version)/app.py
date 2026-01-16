from flask import Flask, render_template, request, redirect, flash
from models import db, URLModel
import validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original_url = request.form.get('url')
        
        if validators.url(original_url):
            new_url = URLModel(original_url=original_url)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + new_url.short_code
        else:
            flash('Invalid URL! Please enter a full link (including http:// or https://)', 'danger')
            
    return render_template('index.html', short_url=short_url)

@app.route('/history')
def history():
    urls = URLModel.query.all()
    return render_template('history.html', urls=urls)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = URLModel.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url_entry.original_url)

if __name__ == '__main__':
    app.run(debug=True)