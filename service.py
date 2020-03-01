import os
import json
import uuid
import subprocess
from flask import Flask, make_response, jsonify, request, send_from_directory, send_file
from werkzeug.routing import Rule


app = Flask(__name__, static_url_path='')

# get prefix from environment variable
APP_ROOT = os.getenv("APP_ROOT")

if APP_ROOT is None:
    pass
else:
    # define custom_rule class
    class Custom_Rule(Rule):
        def __init__(self, string, *args, **kwargs):
            # check endswith '/'
            if APP_ROOT.endswith('/'):
                prefix_without_end_slash = APP_ROOT.rstrip('/')
            else:
                prefix_without_end_slash = APP_ROOT
            # check startswith '/'
            if APP_ROOT.startswith('/'):
                prefix = prefix_without_end_slash
            else:
                prefix = '/' + prefix_without_end_slash
            super(Custom_Rule, self).__init__(prefix + string, *args, **kwargs)

    # set url_rule_class
    app.url_rule_class = Custom_Rule


@app.route('/')
def home():
    return json.dumps({
        "response": "online"
    })


@app.route('/pdf', methods=['POST'])
def pdf():
    data = request.get_json()

    temp_name = uuid.uuid4()
    temp_path = '/app/temp/{}.pdf'.format(temp_name)
    pdf_generated = subprocess.call(
        ['wkhtmltopdf', '--username', data['username'],  '--password',  data['pass'], '--javascript-delay', data['delay'], '--page-size', data['page'], '--orientation', data['orientation'], '--header-right', '( [page] / [toPage] )', '--header-font-size', '10',  data['url'], temp_path])

    if(pdf_generated == 0):
        if APP_ROOT is None:
            resp = {
                "file": "/temp/{}.pdf".format(temp_name)
            }
        else:
            resp = {
                "file": "{}/temp/{}.pdf".format(APP_ROOT, temp_name)
            }
        return (json.dumps(resp), 200, {"Content-Type": "application/json"})
    else:
        return json.dumps({"error": "pdf generation failed"})


@app.route('/png', methods=['POST'])
def png():
    data = request.get_json()

    temp_name = uuid.uuid4()
    temp_path = '/app/temp/{}.png'.format(temp_name)
    png_generated = subprocess.call(
        ['wkhtmltoimage', data['option1'], data['option2'], data['url'], temp_path])

    if(png_generated == 0):
        if APP_ROOT is None:
            resp = {
                "file": "/temp/{}.png".format(temp_name)
            }
        else:
            resp = {
                "file": "{}/temp/{}.png".format(APP_ROOT, temp_name)
            }
        return (json.dumps(resp), 200, {"Content-Type": "application/json"})
    else:
        return json.dumps({"error": "png generation failed"})


@app.route('/jpg', methods=['POST'])
def jpg():
    data = request.get_json()

    temp_name = uuid.uuid4()
    temp_path = '/app/temp/{}.jpg'.format(temp_name)
    jpg_generated = subprocess.call(
        ['wkhtmltoimage', data['option1'], data['option2'], data['url'], temp_path])

    if(jpg_generated == 0):
        if APP_ROOT is None:
            resp = {
                "file": "/temp/{}.jpg".format(temp_name)
            }
        else:
            resp = {
                "file": "{}/temp/{}.jpg".format(APP_ROOT, temp_name)
            }
        return (json.dumps(resp), 200, {"Content-Type": "application/json"})
    else:
        return json.dumps({"error": "jpg generation failed"})


@app.route('/temp/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('temp', path)


# main
if __name__ == "__main__":
    # 利用しているurl_rule_classを表示
    print(app.url_rule_class)
    # Flaskのマッピング情報を表示
    print(app.url_map)
    app.run(host='localhost', port=80)
