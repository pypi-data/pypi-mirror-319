# ValidateContentDocumentAsinRelationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.validate_content_document_asin_relations_response import ValidateContentDocumentAsinRelationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateContentDocumentAsinRelationsResponse from a JSON string
validate_content_document_asin_relations_response_instance = ValidateContentDocumentAsinRelationsResponse.from_json(json)
# print the JSON string representation of the object
print(ValidateContentDocumentAsinRelationsResponse.to_json())

# convert the object into a dict
validate_content_document_asin_relations_response_dict = validate_content_document_asin_relations_response_instance.to_dict()
# create an instance of ValidateContentDocumentAsinRelationsResponse from a dict
validate_content_document_asin_relations_response_from_dict = ValidateContentDocumentAsinRelationsResponse.from_dict(validate_content_document_asin_relations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


