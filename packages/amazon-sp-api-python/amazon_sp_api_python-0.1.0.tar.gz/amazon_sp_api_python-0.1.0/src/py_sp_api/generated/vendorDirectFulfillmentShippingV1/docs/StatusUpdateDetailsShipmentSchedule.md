# StatusUpdateDetailsShipmentSchedule

Details for the scheduled delivery timeline for a shipment, including the estimated delivery date and time, as well as the start and end times of the appointment window for delivery.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**estimated_delivery_date_time** | **datetime** | Date on which the shipment is expected to reach the customer delivery location. This field is expected to be in ISO-8601 date/time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 
**appt_window_start_date_time** | **datetime** | This field indicates the date and time at the start of the appointment window scheduled to deliver the shipment. This field is expected to be in ISO-8601 date/time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 
**appt_window_end_date_time** | **datetime** | This field indicates the date and time at the end of the appointment window scheduled to deliver the shipment. This field is expected to be in ISO-8601 date/time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.status_update_details_shipment_schedule import StatusUpdateDetailsShipmentSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of StatusUpdateDetailsShipmentSchedule from a JSON string
status_update_details_shipment_schedule_instance = StatusUpdateDetailsShipmentSchedule.from_json(json)
# print the JSON string representation of the object
print(StatusUpdateDetailsShipmentSchedule.to_json())

# convert the object into a dict
status_update_details_shipment_schedule_dict = status_update_details_shipment_schedule_instance.to_dict()
# create an instance of StatusUpdateDetailsShipmentSchedule from a dict
status_update_details_shipment_schedule_from_dict = StatusUpdateDetailsShipmentSchedule.from_dict(status_update_details_shipment_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


