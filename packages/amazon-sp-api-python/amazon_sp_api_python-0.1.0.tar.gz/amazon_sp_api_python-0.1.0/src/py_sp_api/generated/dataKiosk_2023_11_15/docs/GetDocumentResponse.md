# GetDocumentResponse

The response for the `getDocument` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **str** | The identifier for the Data Kiosk document. This identifier is unique only in combination with a selling partner account ID. | 
**document_url** | **str** | A presigned URL that can be used to retrieve the Data Kiosk document. This URL expires after 5 minutes. If the Data Kiosk document is compressed, the &#x60;Content-Encoding&#x60; header will indicate the compression algorithm.  **Note:** Most HTTP clients are capable of automatically decompressing downloaded files based on the &#x60;Content-Encoding&#x60; header. | 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.get_document_response import GetDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDocumentResponse from a JSON string
get_document_response_instance = GetDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(GetDocumentResponse.to_json())

# convert the object into a dict
get_document_response_dict = get_document_response_instance.to_dict()
# create an instance of GetDocumentResponse from a dict
get_document_response_from_dict = GetDocumentResponse.from_dict(get_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


