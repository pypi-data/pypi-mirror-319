# CollectOnDelivery

The amount to collect on delivery.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | [**Currency**](Currency.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.collect_on_delivery import CollectOnDelivery

# TODO update the JSON string below
json = "{}"
# create an instance of CollectOnDelivery from a JSON string
collect_on_delivery_instance = CollectOnDelivery.from_json(json)
# print the JSON string representation of the object
print(CollectOnDelivery.to_json())

# convert the object into a dict
collect_on_delivery_dict = collect_on_delivery_instance.to_dict()
# create an instance of CollectOnDelivery from a dict
collect_on_delivery_from_dict = CollectOnDelivery.from_dict(collect_on_delivery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


