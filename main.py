from flask import Flask, request
from implement2D import Calc
from numpy import random
from pprint import pprint
import webbrowser
import json

app = Flask(__name__)


@app.route("/")
def root():
  return app.send_static_file('./index.html')


@app.route("/calc", methods=['POST'])
def calc():
  data = json.loads(request.data)
  # print(data)
  ci = list(map(lambda x: float(x), data["ci"]))
  # ci = data["ci"].map(lambda x: int(x))
  c = Calc(int(data["minutes"]), float(data["alpha"]), float(data["l"]), float(data["dx"]),
           float(data["dy"]), float(data["dt"]), ci)

  pprint(vars(c))

  c.calculate()
  c.show()

  return "ok"



# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'
webbrowser.get(chrome_path).open("http://localhost:5000")


app.run(host="0.0.0.0", port=5000, debug=False,
        threaded=False, use_reloader=False)
