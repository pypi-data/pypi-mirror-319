# CreateReservationRequest

Request schema for the `createReservation` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** | Resource (store) identifier. | 
**reservation** | [**Reservation**](Reservation.md) |  | 

## Example

```python
from py_sp_api.generated.services.models.create_reservation_request import CreateReservationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReservationRequest from a JSON string
create_reservation_request_instance = CreateReservationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateReservationRequest.to_json())

# convert the object into a dict
create_reservation_request_dict = create_reservation_request_instance.to_dict()
# create an instance of CreateReservationRequest from a dict
create_reservation_request_from_dict = CreateReservationRequest.from_dict(create_reservation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


