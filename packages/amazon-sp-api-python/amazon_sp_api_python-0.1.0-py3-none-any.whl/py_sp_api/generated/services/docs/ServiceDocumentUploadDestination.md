# ServiceDocumentUploadDestination

Information about an upload destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_destination_id** | **str** | The unique identifier to be used by APIs that reference the upload destination. | 
**url** | **str** | The URL to which to upload the file. | 
**encryption_details** | [**EncryptionDetails**](EncryptionDetails.md) |  | 
**headers** | **object** | The headers to include in the upload request. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.service_document_upload_destination import ServiceDocumentUploadDestination

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceDocumentUploadDestination from a JSON string
service_document_upload_destination_instance = ServiceDocumentUploadDestination.from_json(json)
# print the JSON string representation of the object
print(ServiceDocumentUploadDestination.to_json())

# convert the object into a dict
service_document_upload_destination_dict = service_document_upload_destination_instance.to_dict()
# create an instance of ServiceDocumentUploadDestination from a dict
service_document_upload_destination_from_dict = ServiceDocumentUploadDestination.from_dict(service_document_upload_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


