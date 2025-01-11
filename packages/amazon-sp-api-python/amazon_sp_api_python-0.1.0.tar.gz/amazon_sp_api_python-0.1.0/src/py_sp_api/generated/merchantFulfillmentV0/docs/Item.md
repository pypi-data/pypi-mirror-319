# Item

An Amazon order item identifier and a quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_item_id** | **str** | An Amazon-defined identifier for an individual item in an order. | 
**quantity** | **int** | The number of items. | 
**item_weight** | [**Weight**](Weight.md) |  | [optional] 
**item_description** | **str** | The description of the item. | [optional] 
**transparency_code_list** | **List[str]** | A list of transparency codes. | [optional] 
**item_level_seller_inputs_list** | [**List[AdditionalSellerInputs]**](AdditionalSellerInputs.md) | A list of additional seller input pairs required to purchase shipping. | [optional] 
**liquid_volume** | [**LiquidVolume**](LiquidVolume.md) |  | [optional] 
**is_hazmat** | **bool** | When true, the item qualifies as hazardous materials (hazmat). Defaults to false. | [optional] 
**dangerous_goods_details** | [**DangerousGoodsDetails**](DangerousGoodsDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.item import Item

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


