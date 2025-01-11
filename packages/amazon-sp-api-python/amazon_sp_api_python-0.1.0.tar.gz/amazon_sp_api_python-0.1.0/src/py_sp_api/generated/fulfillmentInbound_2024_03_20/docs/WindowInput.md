# WindowInput

Contains only a starting DateTime.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **datetime** | The start date of the window. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with minute precision. Supports patterns &#x60;yyyy-MM-ddTHH:mmZ&#x60;, &#x60;yyyy-MM-ddTHH:mm:ssZ&#x60;, or &#x60;yyyy-MM-ddTHH:mm:ss.sssZ&#x60;. Note that non-zero second and millisecond components are removed. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.window_input import WindowInput

# TODO update the JSON string below
json = "{}"
# create an instance of WindowInput from a JSON string
window_input_instance = WindowInput.from_json(json)
# print the JSON string representation of the object
print(WindowInput.to_json())

# convert the object into a dict
window_input_dict = window_input_instance.to_dict()
# create an instance of WindowInput from a dict
window_input_from_dict = WindowInput.from_dict(window_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


