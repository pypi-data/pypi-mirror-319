# UpdateReservationRequest

Request schema for the `updateReservation` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** | Resource (store) identifier. | 
**reservation** | [**Reservation**](Reservation.md) |  | 

## Example

```python
from py_sp_api.generated.services.models.update_reservation_request import UpdateReservationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateReservationRequest from a JSON string
update_reservation_request_instance = UpdateReservationRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateReservationRequest.to_json())

# convert the object into a dict
update_reservation_request_dict = update_reservation_request_instance.to_dict()
# create an instance of UpdateReservationRequest from a dict
update_reservation_request_from_dict = UpdateReservationRequest.from_dict(update_reservation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


