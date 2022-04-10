import re
from flask import Flask, flash, redirect, url_for, render_template, request, session
import numpy as np
import pandas as pd



app = Flask(__name__)

# config------------------------------------------------
DATASETS_BASE_FOLDER = 'Dataset\\'
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------


@app.route('/', methods=['POST', 'GET'])
def index(**kwargs):
    
    if request.method=='POST':
        session['sheet_name'] = request.form['submit']
        return redirect(url_for('test'))

    else:
        vocab_file_sheets = pd.read_excel(VOCAB_FILE, None)
        return render_template('index.html', sheets_dict = vocab_file_sheets)
        
