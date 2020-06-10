from flask import Flask, request

from descriptors import StringField, DeviceField, PositiveIntegerField
from request import BaseRequest

app = Flask(__name__)


class SampleRequest(BaseRequest):
    name = StringField(length=15)
    device = DeviceField()
    age = PositiveIntegerField()


@app.route('/example', methods=["POST"])
def hello_world():
    sample_request = SampleRequest(request.json)

    result = {
        'name': sample_request.name,
        'device': sample_request.device,
        'age': sample_request.age
    }
    return result, 201


if __name__ == '__main__':
    app.run()
