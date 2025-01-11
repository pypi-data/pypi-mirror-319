# Item

Details of the item being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Item sequence number for the item. The first item will be 001, the second 002, and so on. This number is used as a reference to refer to this item from the carton or pallet level. | 
**amazon_product_identifier** | **str** | Buyer Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was sent in the purchase order. | [optional] 
**shipped_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**item_details** | [**ItemDetails**](ItemDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.item import Item

# TODO update the JSON string below
json = "{}"
# create an instance of Item from a JSON string
item_instance = Item.from_json(json)
# print the JSON string representation of the object
print(Item.to_json())

# convert the object into a dict
item_dict = item_instance.to_dict()
# create an instance of Item from a dict
item_from_dict = Item.from_dict(item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


