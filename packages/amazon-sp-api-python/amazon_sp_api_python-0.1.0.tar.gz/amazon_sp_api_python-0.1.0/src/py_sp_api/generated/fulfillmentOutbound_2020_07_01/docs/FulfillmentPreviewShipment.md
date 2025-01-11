# FulfillmentPreviewShipment

Delivery and item information for a shipment in a fulfillment order preview.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**earliest_ship_date** | **datetime** | Date timestamp | [optional] 
**latest_ship_date** | **datetime** | Date timestamp | [optional] 
**earliest_arrival_date** | **datetime** | Date timestamp | [optional] 
**latest_arrival_date** | **datetime** | Date timestamp | [optional] 
**shipping_notes** | **List[str]** | Provides additional insight into the shipment timeline when exact delivery dates are not able to be precomputed. | [optional] 
**fulfillment_preview_items** | [**List[FulfillmentPreviewItem]**](FulfillmentPreviewItem.md) | An array of fulfillment preview item information. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_preview_shipment import FulfillmentPreviewShipment

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentPreviewShipment from a JSON string
fulfillment_preview_shipment_instance = FulfillmentPreviewShipment.from_json(json)
# print the JSON string representation of the object
print(FulfillmentPreviewShipment.to_json())

# convert the object into a dict
fulfillment_preview_shipment_dict = fulfillment_preview_shipment_instance.to_dict()
# create an instance of FulfillmentPreviewShipment from a dict
fulfillment_preview_shipment_from_dict = FulfillmentPreviewShipment.from_dict(fulfillment_preview_shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


