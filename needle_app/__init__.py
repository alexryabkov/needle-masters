from flask import Flask

app = Flask(__name__)

import needle_app.views
import needle_app.app_admin
