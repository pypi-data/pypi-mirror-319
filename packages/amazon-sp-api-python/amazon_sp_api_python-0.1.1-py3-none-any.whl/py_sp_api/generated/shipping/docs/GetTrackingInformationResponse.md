# GetTrackingInformationResponse

The response schema for the getTrackingInformation operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TrackingInformation**](TrackingInformation.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.get_tracking_information_response import GetTrackingInformationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetTrackingInformationResponse from a JSON string
get_tracking_information_response_instance = GetTrackingInformationResponse.from_json(json)
# print the JSON string representation of the object
print(GetTrackingInformationResponse.to_json())

# convert the object into a dict
get_tracking_information_response_dict = get_tracking_information_response_instance.to_dict()
# create an instance of GetTrackingInformationResponse from a dict
get_tracking_information_response_from_dict = GetTrackingInformationResponse.from_dict(get_tracking_information_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


