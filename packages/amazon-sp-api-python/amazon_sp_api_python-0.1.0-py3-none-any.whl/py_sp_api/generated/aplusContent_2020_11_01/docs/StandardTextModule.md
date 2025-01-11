# StandardTextModule

A standard headline and body text.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headline** | [**TextComponent**](TextComponent.md) |  | [optional] 
**body** | [**ParagraphComponent**](ParagraphComponent.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.standard_text_module import StandardTextModule

# TODO update the JSON string below
json = "{}"
# create an instance of StandardTextModule from a JSON string
standard_text_module_instance = StandardTextModule.from_json(json)
# print the JSON string representation of the object
print(StandardTextModule.to_json())

# convert the object into a dict
standard_text_module_dict = standard_text_module_instance.to_dict()
# create an instance of StandardTextModule from a dict
standard_text_module_from_dict = StandardTextModule.from_dict(standard_text_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


