# UpdateReservationResponse

Response schema for the `updateReservation` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**UpdateReservationRecord**](UpdateReservationRecord.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.update_reservation_response import UpdateReservationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateReservationResponse from a JSON string
update_reservation_response_instance = UpdateReservationResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateReservationResponse.to_json())

# convert the object into a dict
update_reservation_response_dict = update_reservation_response_instance.to_dict()
# create an instance of UpdateReservationResponse from a dict
update_reservation_response_from_dict = UpdateReservationResponse.from_dict(update_reservation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


