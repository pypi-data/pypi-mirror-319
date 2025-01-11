# ServiceUploadDocument

Input for to be uploaded document.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **str** | The content type of the to-be-uploaded file | 
**content_length** | **float** | The content length of the to-be-uploaded file | 
**content_md5** | **str** | An MD5 hash of the content to be submitted to the upload destination. This value is used to determine if the data has been corrupted or tampered with during transit. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.service_upload_document import ServiceUploadDocument

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceUploadDocument from a JSON string
service_upload_document_instance = ServiceUploadDocument.from_json(json)
# print the JSON string representation of the object
print(ServiceUploadDocument.to_json())

# convert the object into a dict
service_upload_document_dict = service_upload_document_instance.to_dict()
# create an instance of ServiceUploadDocument from a dict
service_upload_document_from_dict = ServiceUploadDocument.from_dict(service_upload_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


