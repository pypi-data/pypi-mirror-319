# PackedItems

Details of the item being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **str** | Item sequence number for the item. The first item will be 001, the second 002, and so on. This number is used as a reference to refer to this item from the carton or pallet level. | [optional] 
**buyer_product_identifier** | **str** | Buyer Standard Identification Number (ASIN) of an item. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was sent in the purchase order. | [optional] 
**packed_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**item_details** | [**PackageItemDetails**](PackageItemDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.packed_items import PackedItems

# TODO update the JSON string below
json = "{}"
# create an instance of PackedItems from a JSON string
packed_items_instance = PackedItems.from_json(json)
# print the JSON string representation of the object
print(PackedItems.to_json())

# convert the object into a dict
packed_items_dict = packed_items_instance.to_dict()
# create an instance of PackedItems from a dict
packed_items_from_dict = PackedItems.from_dict(packed_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


