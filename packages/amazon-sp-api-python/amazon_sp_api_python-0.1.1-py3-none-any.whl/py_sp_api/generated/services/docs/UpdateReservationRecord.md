# UpdateReservationRecord

`UpdateReservationRecord` entity contains the `Reservation` if there is an error/warning while performing the requested operation on it, otherwise it will contain the new `reservationId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reservation** | [**Reservation**](Reservation.md) |  | [optional] 
**warnings** | [**List[Warning]**](Warning.md) | A list of warnings returned in the sucessful execution response of an API request. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.update_reservation_record import UpdateReservationRecord

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateReservationRecord from a JSON string
update_reservation_record_instance = UpdateReservationRecord.from_json(json)
# print the JSON string representation of the object
print(UpdateReservationRecord.to_json())

# convert the object into a dict
update_reservation_record_dict = update_reservation_record_instance.to_dict()
# create an instance of UpdateReservationRecord from a dict
update_reservation_record_from_dict = UpdateReservationRecord.from_dict(update_reservation_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


