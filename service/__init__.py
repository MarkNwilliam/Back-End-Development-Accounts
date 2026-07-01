import os
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)

# CORS policy configuration
CORS(app)

# Security headers with Talisman
talisman = Talisman(
    app,
    content_security_policy=None,
    force_https=False,
    strict_transport_security=True,
    session_cookie_secure=False
)

from service import routes
