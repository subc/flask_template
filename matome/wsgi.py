# -*- coding: utf-8 -*-
from app import create_app
# app = create_app(config='')
app = create_app(config='./config/production.py')

if __name__ == "__main__":
     app.run(debug=True)
