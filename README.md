## Flask-Personal_Library_Page_using_JWT_SQLAlchemy_Jinja

### Installation 
```
pip install flask
pip install flask_sqlalchemy
```
Inside your file for run, also import:
 ```python
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
 ```
