# FulfillmentPreview

Information about a fulfillment order preview, including delivery and fee information based on shipping method.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_speed_category** | [**ShippingSpeedCategory**](ShippingSpeedCategory.md) |  | 
**scheduled_delivery_info** | [**ScheduledDeliveryInfo**](ScheduledDeliveryInfo.md) |  | [optional] 
**is_fulfillable** | **bool** | When true, this fulfillment order preview is fulfillable. | 
**is_cod_capable** | **bool** | When true, this fulfillment order preview is for COD (Cash On Delivery). | 
**estimated_shipping_weight** | [**Weight**](Weight.md) |  | [optional] 
**estimated_fees** | [**List[Fee]**](Fee.md) | An array of fee type and cost pairs. | [optional] 
**fulfillment_preview_shipments** | [**List[FulfillmentPreviewShipment]**](FulfillmentPreviewShipment.md) | An array of fulfillment preview shipment information. | [optional] 
**unfulfillable_preview_items** | [**List[UnfulfillablePreviewItem]**](UnfulfillablePreviewItem.md) | An array of unfulfillable preview item information. | [optional] 
**order_unfulfillable_reasons** | **List[str]** | String list | [optional] 
**marketplace_id** | **str** | The marketplace the fulfillment order is placed against. | 
**feature_constraints** | [**List[FeatureSettings]**](FeatureSettings.md) | A list of features and their fulfillment policies to apply to the order. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_preview import FulfillmentPreview

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentPreview from a JSON string
fulfillment_preview_instance = FulfillmentPreview.from_json(json)
# print the JSON string representation of the object
print(FulfillmentPreview.to_json())

# convert the object into a dict
fulfillment_preview_dict = fulfillment_preview_instance.to_dict()
# create an instance of FulfillmentPreview from a dict
fulfillment_preview_from_dict = FulfillmentPreview.from_dict(fulfillment_preview_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


