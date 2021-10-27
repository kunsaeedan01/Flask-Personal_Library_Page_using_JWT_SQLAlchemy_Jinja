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
### Usage
There 2 tables for functionality:
1) User table stores user's id, login, password, token
2) Book is a table which stores the items from webpage functionality: adding books that will be stored at main page.
/add route allows you to add one record of a book's title, author and it's rating, your records will be saved on database
/delete for drop the book from list and it will not be shown
/edit allows to update information

### Example 
Authentication realised using JWT.
/unprotected allows to compare token-added and token-free access.
```python
@app.route('/unprotected')
def unprotected():
    return jsonify({"message":"Anyone can view this"})
```
/protected route uses decorator to verify the valid token
```python
@app.route('/protected')
@token_required
def protected():
    return jsonify({"message": "This is only available for people with valid tokens."})
```

