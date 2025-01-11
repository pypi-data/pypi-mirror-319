# ScheduledDeliveryShipment

Dates for the scheduled delivery shipments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scheduled_delivery_service_type** | **str** | Scheduled delivery service type. | [optional] 
**earliest_nominated_delivery_date** | **datetime** | Earliest nominated delivery date for the scheduled delivery. | [optional] 
**latest_nominated_delivery_date** | **datetime** | Latest nominated delivery date for the scheduled delivery. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.scheduled_delivery_shipment import ScheduledDeliveryShipment

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduledDeliveryShipment from a JSON string
scheduled_delivery_shipment_instance = ScheduledDeliveryShipment.from_json(json)
# print the JSON string representation of the object
print(ScheduledDeliveryShipment.to_json())

# convert the object into a dict
scheduled_delivery_shipment_dict = scheduled_delivery_shipment_instance.to_dict()
# create an instance of ScheduledDeliveryShipment from a dict
scheduled_delivery_shipment_from_dict = ScheduledDeliveryShipment.from_dict(scheduled_delivery_shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


