# FulfillmentShipment

Delivery and item information for a shipment in a fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_shipment_id** | **str** | A shipment identifier assigned by Amazon. | 
**fulfillment_center_id** | **str** | An identifier for the fulfillment center that the shipment will be sent from. | 
**fulfillment_shipment_status** | **str** | The current status of the shipment. | 
**shipping_date** | **datetime** | Date timestamp | [optional] 
**estimated_arrival_date** | **datetime** | Date timestamp | [optional] 
**shipping_notes** | **List[str]** | Provides additional insight into shipment timeline. Primairly used to communicate that actual delivery dates aren&#39;t available. | [optional] 
**fulfillment_shipment_item** | [**List[FulfillmentShipmentItem]**](FulfillmentShipmentItem.md) | An array of fulfillment shipment item information. | 
**fulfillment_shipment_package** | [**List[FulfillmentShipmentPackage]**](FulfillmentShipmentPackage.md) | An array of fulfillment shipment package information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_shipment import FulfillmentShipment

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentShipment from a JSON string
fulfillment_shipment_instance = FulfillmentShipment.from_json(json)
# print the JSON string representation of the object
print(FulfillmentShipment.to_json())

# convert the object into a dict
fulfillment_shipment_dict = fulfillment_shipment_instance.to_dict()
# create an instance of FulfillmentShipment from a dict
fulfillment_shipment_from_dict = FulfillmentShipment.from_dict(fulfillment_shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


