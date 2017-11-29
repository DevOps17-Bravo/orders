######################################################################
# Error Handlers
# Handles all of the HTTP Error Codes as JSON
######################################################################

from flask import jsonify, make_response
from app.server import app
from app.custom_exceptions import DataValidationError


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles all data validation issues from the model """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles requests that have bad or malformed data """
    return make_response(jsonify(status=400, error="Bad Request", message=error.message), 400)

@app.errorhandler(404)
def not_found(error):
    """ Handles Orders that cannot be found """
    return make_response(jsonify(status=404, error="Not Found", message=error.message), 404)

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles bad method calls """
    return make_response(jsonify(status=405, error="Method not Allowed",
                   message="Your request method is not supported." \
                   " Check your HTTP method and try again."), 405)

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles catostrophic errors """
    return make_response(jsonify(status=500, error="Internal Server Error", message=error.message), 500)
