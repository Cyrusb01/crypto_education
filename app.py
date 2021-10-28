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

# @app.route('/h')
# def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 1000):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	
# 	xAxis = {"categories": [1, 2, 3]}
# 	yAxis = {"title": {"text": 'yAxis Label'}}
# 	return render_template('highchart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/h')
def high():
    title = {"text": 'My Title'}
    chartID = "chart_ID"
    return render_template('highchart.html', title = title, chartID=chartID)

if __name__ == "__main__":

    
	app.run(debug = True, passthrough_errors=True) 