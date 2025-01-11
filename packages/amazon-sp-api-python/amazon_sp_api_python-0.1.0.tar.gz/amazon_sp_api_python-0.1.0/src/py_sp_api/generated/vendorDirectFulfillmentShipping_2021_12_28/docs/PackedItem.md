# PackedItem

An item that has been packed into a container for shipping.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **int** | The sequence number of the item. The number must be the same as the order number of the item. | 
**buyer_product_identifier** | **str** | The buyer&#39;s Amazon Standard Identification Number (ASIN) of an item. Either &#x60;buyerProductIdentifier&#x60; or &#x60;vendorProductIdentifier&#x60; is required. | [optional] 
**piece_number** | **int** | The piece number of the item in this container. This is required when the item is split across different containers. | [optional] 
**vendor_product_identifier** | **str** | An item&#39;s product identifier, which the vendor selects. This identifier should be the same as the identifier, such as a SKU, in the purchase order. | [optional] 
**packed_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.packed_item import PackedItem

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


