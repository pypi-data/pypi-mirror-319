# Decorator

A decorator applied to a content string value in order to create rich text.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**DecoratorType**](DecoratorType.md) |  | [optional] 
**offset** | **int** | The starting character of this decorator within the content string. Use zero for the first character. | [optional] 
**length** | **int** | The number of content characters to alter with this decorator. Decorators such as line breaks can have zero length and fit between characters. | [optional] 
**depth** | **int** | The relative intensity or variation of this decorator. Decorators such as bullet-points, for example, can have multiple indentation depths. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.decorator import Decorator

# TODO update the JSON string below
json = "{}"
# create an instance of Decorator from a JSON string
decorator_instance = Decorator.from_json(json)
# print the JSON string representation of the object
print(Decorator.to_json())

# convert the object into a dict
decorator_dict = decorator_instance.to_dict()
# create an instance of Decorator from a dict
decorator_from_dict = Decorator.from_dict(decorator_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


