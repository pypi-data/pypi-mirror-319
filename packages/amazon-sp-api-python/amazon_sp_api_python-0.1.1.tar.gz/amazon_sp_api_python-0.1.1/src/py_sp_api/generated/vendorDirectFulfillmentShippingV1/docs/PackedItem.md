# PackedItem

Represents an item that has been packed into a container for shipping.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **int** | Item Sequence Number for the item. This must be the same value as sent in the order for a given item. | 
**buyer_product_identifier** | **str** | Buyer&#39;s Standard Identification Number (ASIN) of an item. Either buyerProductIdentifier or vendorProductIdentifier is required. | [optional] 
**vendor_product_identifier** | **str** | The vendor selected product identification of the item. Should be the same as was sent in the Purchase Order, like SKU Number. | [optional] 
**packed_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.packed_item import PackedItem

# TODO update the JSON string below
json = "{}"
# create an instance of PackedItem from a JSON string
packed_item_instance = PackedItem.from_json(json)
# print the JSON string representation of the object
print(PackedItem.to_json())

# convert the object into a dict
packed_item_dict = packed_item_instance.to_dict()
# create an instance of PackedItem from a dict
packed_item_from_dict = PackedItem.from_dict(packed_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


