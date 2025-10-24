from flask import Flask 
from routes.home import home_route
from routes.admin import admin_route


app = Flask(__name__)
app.register_blueprint(home_route)
app.register_blueprint(admin_route, url_prefix='/admin')

app.secret_key = 'chave-secreta'

app.run(debug=True)