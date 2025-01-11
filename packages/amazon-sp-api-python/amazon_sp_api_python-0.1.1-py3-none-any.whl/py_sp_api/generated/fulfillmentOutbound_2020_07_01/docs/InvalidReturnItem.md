# InvalidReturnItem

An item that is invalid for return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_return_item_id** | **str** | An identifier assigned by the seller to the return item. | 
**seller_fulfillment_order_item_id** | **str** | The identifier assigned to the item by the seller when the fulfillment order was created. | 
**invalid_item_reason** | [**InvalidItemReason**](InvalidItemReason.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.invalid_return_item import InvalidReturnItem

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidReturnItem from a JSON string
invalid_return_item_instance = InvalidReturnItem.from_json(json)
# print the JSON string representation of the object
print(InvalidReturnItem.to_json())

# convert the object into a dict
invalid_return_item_dict = invalid_return_item_instance.to_dict()
# create an instance of InvalidReturnItem from a dict
invalid_return_item_from_dict = InvalidReturnItem.from_dict(invalid_return_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


