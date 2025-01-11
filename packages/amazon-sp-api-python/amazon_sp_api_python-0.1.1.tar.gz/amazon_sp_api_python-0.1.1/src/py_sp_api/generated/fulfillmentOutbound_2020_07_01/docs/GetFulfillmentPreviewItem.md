# GetFulfillmentPreviewItem

Item information for a fulfillment order preview.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**quantity** | **int** | The item quantity. | 
**per_unit_declared_value** | [**Money**](Money.md) |  | [optional] 
**seller_fulfillment_order_item_id** | **str** | A fulfillment order item identifier that the seller creates to track items in the fulfillment preview. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_fulfillment_preview_item import GetFulfillmentPreviewItem

# TODO update the JSON string below
json = "{}"
# create an instance of GetFulfillmentPreviewItem from a JSON string
get_fulfillment_preview_item_instance = GetFulfillmentPreviewItem.from_json(json)
# print the JSON string representation of the object
print(GetFulfillmentPreviewItem.to_json())

# convert the object into a dict
get_fulfillment_preview_item_dict = get_fulfillment_preview_item_instance.to_dict()
# create an instance of GetFulfillmentPreviewItem from a dict
get_fulfillment_preview_item_from_dict = GetFulfillmentPreviewItem.from_dict(get_fulfillment_preview_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


