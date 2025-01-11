# ShipmentSchedule

Details about the estimated delivery window.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**estimated_delivery_date_time** | **datetime** | Date on which the shipment is expected to reach the customer delivery location. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 
**appt_window_start_date_time** | **datetime** | The date and time at the start of the appointment window when the shipment is expected to be delivered. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 
**appt_window_end_date_time** | **datetime** | The date and time at the end of the appointment window when the shipment is expected to be delivered. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.shipment_schedule import ShipmentSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentSchedule from a JSON string
shipment_schedule_instance = ShipmentSchedule.from_json(json)
# print the JSON string representation of the object
print(ShipmentSchedule.to_json())

# convert the object into a dict
shipment_schedule_dict = shipment_schedule_instance.to_dict()
# create an instance of ShipmentSchedule from a dict
shipment_schedule_from_dict = ShipmentSchedule.from_dict(shipment_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


