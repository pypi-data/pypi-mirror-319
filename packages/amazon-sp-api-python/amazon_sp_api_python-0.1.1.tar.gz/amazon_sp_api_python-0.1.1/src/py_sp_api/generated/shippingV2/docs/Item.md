# Item

An item in a package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_value** | [**Currency**](Currency.md) |  | [optional] 
**description** | **str** | The product description of the item. | [optional] 
**item_identifier** | **str** | A unique identifier for an item provided by the client. | [optional] 
**quantity** | **int** | The number of units. This value is required. | 
**weight** | [**Weight**](Weight.md) |  | [optional] 
**liquid_volume** | [**LiquidVolume**](LiquidVolume.md) |  | [optional] 
**is_hazmat** | **bool** | When true, the item qualifies as hazardous materials (hazmat). Defaults to false. | [optional] 
**dangerous_goods_details** | [**DangerousGoodsDetails**](DangerousGoodsDetails.md) |  | [optional] 
**product_type** | **str** | The product type of the item. | [optional] 
**invoice_details** | [**InvoiceDetails**](InvoiceDetails.md) |  | [optional] 
**serial_numbers** | **List[str]** | A list of unique serial numbers in an Amazon package that can be used to guarantee non-fraudulent items. The number of serial numbers in the list must be less than or equal to the quantity of items being shipped. Only applicable when channel source is Amazon. | [optional] 
**direct_fulfillment_item_identifiers** | [**DirectFulfillmentItemIdentifiers**](DirectFulfillmentItemIdentifiers.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.item import Item

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


