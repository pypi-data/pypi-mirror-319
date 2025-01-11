# CreateServiceDocumentUploadDestination

The response schema for the `createServiceDocumentUploadDestination` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ServiceDocumentUploadDestination**](ServiceDocumentUploadDestination.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.create_service_document_upload_destination import CreateServiceDocumentUploadDestination

# TODO update the JSON string below
json = "{}"
# create an instance of CreateServiceDocumentUploadDestination from a JSON string
create_service_document_upload_destination_instance = CreateServiceDocumentUploadDestination.from_json(json)
# print the JSON string representation of the object
print(CreateServiceDocumentUploadDestination.to_json())

# convert the object into a dict
create_service_document_upload_destination_dict = create_service_document_upload_destination_instance.to_dict()
# create an instance of CreateServiceDocumentUploadDestination from a dict
create_service_document_upload_destination_from_dict = CreateServiceDocumentUploadDestination.from_dict(create_service_document_upload_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


