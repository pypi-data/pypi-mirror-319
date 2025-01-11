# AssociatedItem

An item that is associated with an order item. For example, a tire installation service that is purchased with tires.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | The order item&#39;s order identifier, in 3-7-7 format. | [optional] 
**order_item_id** | **str** | An Amazon-defined item identifier for the associated item. | [optional] 
**association_type** | [**AssociationType**](AssociationType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.associated_item import AssociatedItem

# TODO update the JSON string below
json = "{}"
# create an instance of AssociatedItem from a JSON string
associated_item_instance = AssociatedItem.from_json(json)
# print the JSON string representation of the object
print(AssociatedItem.to_json())

# convert the object into a dict
associated_item_dict = associated_item_instance.to_dict()
# create an instance of AssociatedItem from a dict
associated_item_from_dict = AssociatedItem.from_dict(associated_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


