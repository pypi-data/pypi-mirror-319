# CancelReservationResponse

Response schema for the `cancelReservation` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.cancel_reservation_response import CancelReservationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelReservationResponse from a JSON string
cancel_reservation_response_instance = CancelReservationResponse.from_json(json)
# print the JSON string representation of the object
print(CancelReservationResponse.to_json())

# convert the object into a dict
cancel_reservation_response_dict = cancel_reservation_response_instance.to_dict()
# create an instance of CancelReservationResponse from a dict
cancel_reservation_response_from_dict = CancelReservationResponse.from_dict(cancel_reservation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


