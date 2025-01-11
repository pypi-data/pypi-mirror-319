# UnfulfillablePreviewItem

Information about unfulfillable items in a fulfillment order preview.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**quantity** | **int** | The item quantity. | 
**seller_fulfillment_order_item_id** | **str** | A fulfillment order item identifier created with a call to the &#x60;getFulfillmentPreview&#x60; operation. | 
**item_unfulfillable_reasons** | **List[str]** | String list | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.unfulfillable_preview_item import UnfulfillablePreviewItem

# TODO update the JSON string below
json = "{}"
# create an instance of UnfulfillablePreviewItem from a JSON string
unfulfillable_preview_item_instance = UnfulfillablePreviewItem.from_json(json)
# print the JSON string representation of the object
print(UnfulfillablePreviewItem.to_json())

# convert the object into a dict
unfulfillable_preview_item_dict = unfulfillable_preview_item_instance.to_dict()
# create an instance of UnfulfillablePreviewItem from a dict
unfulfillable_preview_item_from_dict = UnfulfillablePreviewItem.from_dict(unfulfillable_preview_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


