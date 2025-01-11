# ItemDeliveryPromise

Promised delivery information for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | The date and time of the start of the promised delivery window in ISO 8601 format. | [optional] 
**end_time** | **datetime** | The date and time of the end of the promised delivery window in ISO 8601 format. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.item_delivery_promise import ItemDeliveryPromise

# TODO update the JSON string below
json = "{}"
# create an instance of ItemDeliveryPromise from a JSON string
item_delivery_promise_instance = ItemDeliveryPromise.from_json(json)
# print the JSON string representation of the object
print(ItemDeliveryPromise.to_json())

# convert the object into a dict
item_delivery_promise_dict = item_delivery_promise_instance.to_dict()
# create an instance of ItemDeliveryPromise from a dict
item_delivery_promise_from_dict = ItemDeliveryPromise.from_dict(item_delivery_promise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


