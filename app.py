from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.io import show
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

def create_plot(company):
  tick=company.upper()
  apiKey='DsfYw6GwZRN_j6Pq_cSW'
  startD='20170519'
  endD='20170618'
  getURL="https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json" %tick
  para="&api_key=%s&start_date=%s&end_date%s" % (apiKey,startD,endD)
  r=requests.get(getURL,para)
  r1=r.json()
  rdf=pd.DataFrame(r1['dataset_data']['data'],columns=r1['dataset_data']['column_names'])
  rdf['Date'] = pd.to_datetime(rdf['Date'])
  p = figure(title="Closing price for each day of the past month for :%s" %tick, x_axis_type="datetime", plot_height=300, plot_width=600)
  r = p.line(rdf['Date'], rdf['Close'], color="#2222aa", line_width=3)
  return p


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  current_ticker=request.form.get("ticker")
  if current_ticker == None:
    current_ticker='GOOG'
  #if request.method == 'POST':
  plot = create_plot(current_ticker)
  #else:
  #  plot = create_plot('GOOG')		
  # Embed plot into HTML via Flask Render
  script, div = components(plot)
  return render_template("index.html", script=script, div=div, current_ticker=current_ticker)

if __name__ == '__main__':
  app.run(port=33507)
