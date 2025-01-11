# AssociatedItem

Information about an item associated with the service job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**title** | **str** | The title of the item. | [optional] 
**quantity** | **int** | The total number of items included in the order. | [optional] 
**order_id** | **str** | The Amazon-defined identifier for an order placed by the buyer, in 3-7-7 format. | [optional] 
**item_status** | **str** | The status of the item. | [optional] 
**brand_name** | **str** | The brand name of the item. | [optional] 
**item_delivery** | [**ItemDelivery**](ItemDelivery.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.services.models.associated_item import AssociatedItem

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


