# ShippingPromiseSet

The promised delivery time and pickup time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_window** | [**TimeRange**](TimeRange.md) |  | [optional] 
**receive_window** | [**TimeRange**](TimeRange.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.shipping_promise_set import ShippingPromiseSet

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingPromiseSet from a JSON string
shipping_promise_set_instance = ShippingPromiseSet.from_json(json)
# print the JSON string representation of the object
print(ShippingPromiseSet.to_json())

# convert the object into a dict
shipping_promise_set_dict = shipping_promise_set_instance.to_dict()
# create an instance of ShippingPromiseSet from a dict
shipping_promise_set_from_dict = ShippingPromiseSet.from_dict(shipping_promise_set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


