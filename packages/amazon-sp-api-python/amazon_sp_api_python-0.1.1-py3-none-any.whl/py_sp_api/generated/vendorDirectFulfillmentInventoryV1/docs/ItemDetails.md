# ItemDetails

Updated inventory details for an item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer_product_identifier** | **str** | The buyer selected product identification of the item. Either buyerProductIdentifier or vendorProductIdentifier should be submitted. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Either buyerProductIdentifier or vendorProductIdentifier should be submitted. | [optional] 
**available_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**is_obsolete** | **bool** | When true, the item is permanently unavailable. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentInventoryV1.models.item_details import ItemDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ItemDetails from a JSON string
item_details_instance = ItemDetails.from_json(json)
# print the JSON string representation of the object
print(ItemDetails.to_json())

# convert the object into a dict
item_details_dict = item_details_instance.to_dict()
# create an instance of ItemDetails from a dict
item_details_from_dict = ItemDetails.from_dict(item_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


