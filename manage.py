# !/bin/python3
# -*- coding:utf-8 -*-

from project import create_app
import os

app = create_app("test")

if __name__ == "__main__" :
    app.run (host = '0.0.0.0',debug = True)

    
