# Item

Details of the item being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_sequence_number** | **int** | The sequence number of the item. The number must be the same as the order number of the item. | 
**buyer_product_identifier** | **str** | The buyer&#39;s Amazon Standard Identification Number (ASIN) of an item. Either &#x60;buyerProductIdentifier&#x60; or &#x60;vendorProductIdentifier&#x60; is required. | [optional] 
**vendor_product_identifier** | **str** | An item&#39;s product identifier, which the vendor selects. This identifier should be the same as the identifier, such as a SKU, in the purchase order. | [optional] 
**shipped_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.item import Item

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


