from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Team Awesome HackZürich´s project Hello World"

@app.route('/test_html')
def hello_html():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
