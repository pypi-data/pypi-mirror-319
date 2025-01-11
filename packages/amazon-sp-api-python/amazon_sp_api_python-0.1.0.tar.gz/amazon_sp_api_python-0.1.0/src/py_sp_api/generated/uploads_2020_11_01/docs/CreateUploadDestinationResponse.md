# CreateUploadDestinationResponse

The response schema for the createUploadDestination operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**UploadDestination**](UploadDestination.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.uploads_2020_11_01.models.create_upload_destination_response import CreateUploadDestinationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUploadDestinationResponse from a JSON string
create_upload_destination_response_instance = CreateUploadDestinationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateUploadDestinationResponse.to_json())

# convert the object into a dict
create_upload_destination_response_dict = create_upload_destination_response_instance.to_dict()
# create an instance of CreateUploadDestinationResponse from a dict
create_upload_destination_response_from_dict = CreateUploadDestinationResponse.from_dict(create_upload_destination_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


