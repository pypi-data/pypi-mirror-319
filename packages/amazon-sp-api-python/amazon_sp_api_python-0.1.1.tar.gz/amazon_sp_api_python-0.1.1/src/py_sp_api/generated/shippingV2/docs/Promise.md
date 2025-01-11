# Promise

The time windows promised for pickup and delivery events.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_window** | [**TimeWindow**](TimeWindow.md) |  | [optional] 
**pickup_window** | [**TimeWindow**](TimeWindow.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.promise import Promise

# TODO update the JSON string below
json = "{}"
# create an instance of Promise from a JSON string
promise_instance = Promise.from_json(json)
# print the JSON string representation of the object
print(Promise.to_json())

# convert the object into a dict
promise_dict = promise_instance.to_dict()
# create an instance of Promise from a dict
promise_from_dict = Promise.from_dict(promise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


