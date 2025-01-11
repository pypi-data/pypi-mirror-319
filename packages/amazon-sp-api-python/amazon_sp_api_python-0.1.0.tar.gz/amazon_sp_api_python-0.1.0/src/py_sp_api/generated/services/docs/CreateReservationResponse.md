# CreateReservationResponse

Response schema for the `createReservation` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateReservationRecord**](CreateReservationRecord.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.create_reservation_response import CreateReservationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReservationResponse from a JSON string
create_reservation_response_instance = CreateReservationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateReservationResponse.to_json())

# convert the object into a dict
create_reservation_response_dict = create_reservation_response_instance.to_dict()
# create an instance of CreateReservationResponse from a dict
create_reservation_response_from_dict = CreateReservationResponse.from_dict(create_reservation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


