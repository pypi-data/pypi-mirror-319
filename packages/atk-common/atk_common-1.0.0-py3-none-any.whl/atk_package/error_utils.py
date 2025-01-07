from datetime import datetime
import json
from atk_package.datetime_utils import get_utc_date_time
from atk_package.log_utils import add_log_item
from atk_package.response_utils import create_save_resp

def get_message(error):
    if hasattr(error, 'message'):
        return str(error.message)
    else:
        return str(error)

def get_error_entity(app, error, component, method, error_type):
    data = {}
    created = get_utc_date_time()
    data['exceptionType'] = str(type(error))
    data['errorType'] = error_type
    data['message'] = get_message(error)
    data['component'] = component
    data['method'] = method
    data['timestamp'] = created
    return app.response_class(
        response=json.dumps(data),
        status=500,
        mimetype='application/json'
    )

def handle_error(resp, status):
    if resp.status_code == 500:
        add_log_item(resp.json().get('message'))
        return create_save_resp(status, resp.status_code, resp.json())
    else:
        add_log_item(resp.text)
        return create_save_resp(status, resp.status_code, resp.text)

def get_response_error(resp):
    if resp.status_code == 500:
        return resp.json()
    else:
        return resp.text
