# GetContentDocumentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**content_record** | [**ContentRecord**](ContentRecord.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.get_content_document_response import GetContentDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetContentDocumentResponse from a JSON string
get_content_document_response_instance = GetContentDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(GetContentDocumentResponse.to_json())

# convert the object into a dict
get_content_document_response_dict = get_content_document_response_instance.to_dict()
# create an instance of GetContentDocumentResponse from a dict
get_content_document_response_from_dict = GetContentDocumentResponse.from_dict(get_content_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


