# ItemDelivery

Delivery information for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**estimated_delivery_date** | **datetime** | The date and time of the latest Estimated Delivery Date (EDD) of all the items with an EDD. In ISO 8601 format. | [optional] 
**item_delivery_promise** | [**ItemDeliveryPromise**](ItemDeliveryPromise.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.services.models.item_delivery import ItemDelivery

# TODO update the JSON string below
json = "{}"
# create an instance of ItemDelivery from a JSON string
item_delivery_instance = ItemDelivery.from_json(json)
# print the JSON string representation of the object
print(ItemDelivery.to_json())

# convert the object into a dict
item_delivery_dict = item_delivery_instance.to_dict()
# create an instance of ItemDelivery from a dict
item_delivery_from_dict = ItemDelivery.from_dict(item_delivery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


