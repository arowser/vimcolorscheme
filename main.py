# -*- coding: utf-8 -*-
"""
    vim colorscheme online
    ~~~~~~~~~~~~~~~~~~~~~~~

    A online vim colorscheme show site.

    :copyright: (c) 2013 by Arowser
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from flask import Flask, request,  redirect, url_for, abort, \
     render_template

import os
from os import mkdir, remove
from os.path import exists
import time

DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    sz=time.gmtime()
    dirname = "static/%d%d%d" % (sz.tm_year, sz.tm_mon, sz.tm_mday)
    if not exists(dirname):
        mkdir(dirname)
    return render_template('show_entries.html')


@app.route('/', methods=['POST'])
def color_show():
    sz=time.gmtime()
    dirname = "%d%d%d" % (sz.tm_year, sz.tm_mon, sz.tm_mday)
    text = request.form['text']
    colorscheme = request.form['colorscheme']
    vim = request.form['vim']
    language = request.form['language']

    fileName = '%d.c' % (time.time() * 1000)
    f = open(fileName , 'w')
    f.write(text)
    f.close()
    if vim == 'gvim':
        os.system('vim -f +"set filetype=%s" +"syn on" +"colorscheme %s" +"run! syntax/2htmlg.vim"  +"wq" +"q" %s >>/dev/null' % (language, colorscheme, fileName))
    else:
        os.system('vim  -f +"set filetype=%s" +"syn on" +:"colorscheme %s" +:TOhtml +w +qa %s >>/dev/null' % (language, colorscheme, fileName))
    os.system('mv %s.html static/%s/' % (fileName,dirname ))
    remove(fileName)
 
    return redirect(url_for('static', filename='%s/%s.html' % (dirname, fileName)))

if __name__ == '__main__':
    app.run()
