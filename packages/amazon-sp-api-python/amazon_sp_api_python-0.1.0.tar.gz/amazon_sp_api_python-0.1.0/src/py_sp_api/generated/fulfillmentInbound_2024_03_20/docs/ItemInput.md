# ItemInput

Defines an item's input parameters.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expiration** | **str** | The expiration date of the MSKU. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;YYYY-MM-DD&#x60;. Items with the same MSKU but different expiration dates cannot go into the same box. | [optional] 
**label_owner** | [**LabelOwner**](LabelOwner.md) |  | 
**manufacturing_lot_code** | **str** | The manufacturing lot code. | [optional] 
**msku** | **str** | The merchant SKU, a merchant-supplied identifier of a specific SKU. | 
**prep_owner** | [**PrepOwner**](PrepOwner.md) |  | 
**quantity** | **int** | The number of units of the specified MSKU that will be shipped. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.item_input import ItemInput

# TODO update the JSON string below
json = "{}"
# create an instance of ItemInput from a JSON string
item_input_instance = ItemInput.from_json(json)
# print the JSON string representation of the object
print(ItemInput.to_json())

# convert the object into a dict
item_input_dict = item_input_instance.to_dict()
# create an instance of ItemInput from a dict
item_input_from_dict = ItemInput.from_dict(item_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


