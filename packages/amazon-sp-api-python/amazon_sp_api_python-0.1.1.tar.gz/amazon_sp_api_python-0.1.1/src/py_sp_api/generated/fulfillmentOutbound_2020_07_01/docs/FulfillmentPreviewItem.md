# FulfillmentPreviewItem

Item information for a shipment in a fulfillment order preview.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**quantity** | **int** | The item quantity. | 
**seller_fulfillment_order_item_id** | **str** | A fulfillment order item identifier that the seller created with a call to the &#x60;createFulfillmentOrder&#x60; operation. | 
**estimated_shipping_weight** | [**Weight**](Weight.md) |  | [optional] 
**shipping_weight_calculation_method** | **str** | The method used to calculate the estimated shipping weight. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_preview_item import FulfillmentPreviewItem

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentPreviewItem from a JSON string
fulfillment_preview_item_instance = FulfillmentPreviewItem.from_json(json)
# print the JSON string representation of the object
print(FulfillmentPreviewItem.to_json())

# convert the object into a dict
fulfillment_preview_item_dict = fulfillment_preview_item_instance.to_dict()
# create an instance of FulfillmentPreviewItem from a dict
fulfillment_preview_item_from_dict = FulfillmentPreviewItem.from_dict(fulfillment_preview_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


