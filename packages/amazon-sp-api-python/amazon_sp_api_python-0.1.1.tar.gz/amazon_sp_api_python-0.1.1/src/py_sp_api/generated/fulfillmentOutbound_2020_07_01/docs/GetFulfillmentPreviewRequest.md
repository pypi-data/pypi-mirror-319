# GetFulfillmentPreviewRequest

The request body schema for the `getFulfillmentPreview` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The marketplace the fulfillment order is placed against. | [optional] 
**address** | [**Address**](Address.md) |  | 
**items** | [**List[GetFulfillmentPreviewItem]**](GetFulfillmentPreviewItem.md) | An array of fulfillment preview item information. | 
**shipping_speed_categories** | [**List[ShippingSpeedCategory]**](ShippingSpeedCategory.md) | ShippingSpeedCategory List | [optional] 
**include_cod_fulfillment_preview** | **bool** | When true, returns all fulfillment order previews both for COD and not for COD. Otherwise, returns only fulfillment order previews that are not for COD. | [optional] 
**include_delivery_windows** | **bool** | When true, returns the &#x60;ScheduledDeliveryInfo&#x60; response object, which contains the available delivery windows for a Scheduled Delivery. The &#x60;ScheduledDeliveryInfo&#x60; response object can only be returned for fulfillment order previews with &#x60;ShippingSpeedCategories&#x60; &#x3D; &#x60;ScheduledDelivery&#x60;. | [optional] 
**feature_constraints** | [**List[FeatureSettings]**](FeatureSettings.md) | A list of features and their fulfillment policies to apply to the order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_fulfillment_preview_request import GetFulfillmentPreviewRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetFulfillmentPreviewRequest from a JSON string
get_fulfillment_preview_request_instance = GetFulfillmentPreviewRequest.from_json(json)
# print the JSON string representation of the object
print(GetFulfillmentPreviewRequest.to_json())

# convert the object into a dict
get_fulfillment_preview_request_dict = get_fulfillment_preview_request_instance.to_dict()
# create an instance of GetFulfillmentPreviewRequest from a dict
get_fulfillment_preview_request_from_dict = GetFulfillmentPreviewRequest.from_dict(get_fulfillment_preview_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


