# DescriptorSample
[![Language](https://img.shields.io/badge/language-Python%203.7-orange.svg?style=flat)](https://swift.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/kokonak/SlidingPuzzleView/blob/master/LICENSE)

## About
Python descriptor를 활용해 간단한 request parameter를 validation하는 예제입니다.

1. Validation할 field의 class(BaseField를 상속받는 class)를 만듭니다.  
    ```python
    class IntegerField(BaseField):
        def _value_check(self, value):
            if type(value) == str and not value.isnumeric():
                raise BaseException(f'`{value}` is not an integer')
    
            if value:
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    raise BaseException(f'`{value}` is an invalid parameter')
    
            return value
    ```

2. API별 parameter가 정의되어 있는 class(BaseRequest를 상속받는 class)를 만듭니다.
    ```python
    class SampleRequest(BaseRequest):
        name = StringField(length=15)
        device = DeviceField()
        age = PositiveIntegerField()
    ```

3. Request parameter를 validation합니다.
    ```python
    @app.route('/example', methods=["POST"])
    def hello_world():
        sample_request = SampleRequest(request.json)
    
        result = {
            'name': sample_request.name,
            'device': sample_request.device,
            'age': sample_request.age
        }
        return result
    ```

## Author
kokonak, <a src="mailto:kokonak7@gmail.com">kokonak7@gmail.com</a>
