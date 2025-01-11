# Window

Contains a start and end DateTime representing a time range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**editable_until** | **datetime** | The timestamp at which this Window can no longer be edited. | [optional] 
**end** | **datetime** | The end timestamp of the window. | 
**start** | **datetime** | The start timestamp of the window. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.window import Window

# TODO update the JSON string below
json = "{}"
# create an instance of Window from a JSON string
window_instance = Window.from_json(json)
# print the JSON string representation of the object
print(Window.to_json())

# convert the object into a dict
window_dict = window_instance.to_dict()
# create an instance of Window from a dict
window_from_dict = Window.from_dict(window_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


