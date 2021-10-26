from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')


@app.route('/btcgold')
def btcgold():
    return render_template('btc_gold.html')

@app.route('/learning')
def learning():
    return render_template('tickerlearning.html')


if __name__ == "__main__":
	app.run(debug = True, passthrough_errors=True) 