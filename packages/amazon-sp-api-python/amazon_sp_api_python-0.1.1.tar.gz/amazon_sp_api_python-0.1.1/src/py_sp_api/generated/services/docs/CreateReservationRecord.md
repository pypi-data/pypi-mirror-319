# CreateReservationRecord

`CreateReservationRecord` entity contains the `Reservation` if there is an error/warning while performing the requested operation on it, otherwise it will contain the new `reservationId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reservation** | [**Reservation**](Reservation.md) |  | [optional] 
**warnings** | [**List[Warning]**](Warning.md) | A list of warnings returned in the sucessful execution response of an API request. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.create_reservation_record import CreateReservationRecord

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReservationRecord from a JSON string
create_reservation_record_instance = CreateReservationRecord.from_json(json)
# print the JSON string representation of the object
print(CreateReservationRecord.to_json())

# convert the object into a dict
create_reservation_record_dict = create_reservation_record_instance.to_dict()
# create an instance of CreateReservationRecord from a dict
create_reservation_record_from_dict = CreateReservationRecord.from_dict(create_reservation_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


