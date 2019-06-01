import quandl
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Dark2_5 as palette
from flask import Flask, request, redirect, render_template
import itertools

quandl.ApiConfig.api_key = "xVZPGx3ny-wXEZqULyN8"



app = Flask(__name__)


def plotcreator(df, values, title):
	colors = itertools.cycle(palette) 
	p = figure(x_axis_type = "datetime", title = title, plot_width = 1000, plot_height = 600)
	p.xaxis.axis_label = 'Date'
	plots = [None]*len(values)
	for idx, (color, value) in enumerate(zip(colors,values)):
		plots[idx] = p.line(df['date'], df[value], legend = '%s price'%value, color = color)
	p.legend.location='top_left'
	return p

# @app.route('/home', methods = ['GET', 'POST'])
# def home():
# 	return render_template('main.html')
@app.route('/tables', methods=['GET', 'POST'])
def table():
	render_template('tables.html')

@app.route('/', methods=['POST', 'GET'])
#@app.route('/main', methods=['POST'])
def main_page():
	variables = {}
	if request.method == 'GET':
		return render_template('main.html')
	else:
		variables['Stock'] = request.form['Stock Name']# change the paragraph to a form 
													 			   #	if not succesful
		variables['Values'] = request.form.getlist('Values')
		if len(variables['Values']) == 0:
			return render_template('main_choose.html')

		start_date = request.form.get('Start Date') 
		end_date = request.form.get('End Date')
		StockPrices = quandl.get_table("WIKI/PRICES", 
			qopts = {'columns': variables['Values']+['date', 'ticker']},
			ticker = variables['Stock'], date = {'gte': start_date, 'lte': end_date})
		print(StockPrices)
		if StockPrices.empty:
			return render_template('nodata.html')

		p = plotcreator(StockPrices, variables['Values'], variables['Stock'])
		script, div = components(p)

		return render_template('main.html', script = script, div = div)

if __name__ == '__main__':
    app.run(debug=True)

