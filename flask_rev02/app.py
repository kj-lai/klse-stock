from flask import *
from app_func import show_tables, plot_tables
import io
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def mainpage():
	return render_template('mainpage.html')

@app.route('/', methods=['POST'])
def display():
	input_code = request.form['code']
	val1_1, val1_2, val2, graph1, graph2, graph3 = show_tables(input_code.zfill(4))

	if type(val1_1) == str:
		return render_template('stock-not-found.html')
	else:
		title1     = 'Stock Details for '+str(input_code).zfill(4)+': '+val1_1.name.values[0]
		title2     = 'Past 10 Years Financials'
		save_file1 = './static/images/graph_'+str(input_code)+'_01.png'
		save_file2 = './static/images/graph_'+str(input_code)+'_02.png'
		save_file3 = './static/images/graph_'+str(input_code)+'_03.png'

		graph1.savefig(save_file1, bbox_inches='tight', pad_inches=0.1)
		graph2.savefig(save_file2, bbox_inches='tight', pad_inches=0.1)
		graph3.savefig(save_file3, bbox_inches='tight', pad_inches=0.1)

		return render_template('dashboard.html',
							   tables=[val1_1.to_html(table_id='table1', index=False),
									   val1_2.iloc[:, :25].to_html(table_id='table2', index=False), 
									   val1_2.iloc[:, 25:].to_html(table_id='table3', index=False),
									   val2.to_html(table_id='table4', index=False)],
							   titles = [title1, title2],
							   images = [save_file1, save_file2, save_file3])

if __name__ == '__main__':
	app.run(debug=True)
