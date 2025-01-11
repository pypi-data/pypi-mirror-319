# PostContentDocumentSuspendSubmissionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_suspend_submission_response import PostContentDocumentSuspendSubmissionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentSuspendSubmissionResponse from a JSON string
post_content_document_suspend_submission_response_instance = PostContentDocumentSuspendSubmissionResponse.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentSuspendSubmissionResponse.to_json())

# convert the object into a dict
post_content_document_suspend_submission_response_dict = post_content_document_suspend_submission_response_instance.to_dict()
# create an instance of PostContentDocumentSuspendSubmissionResponse from a dict
post_content_document_suspend_submission_response_from_dict = PostContentDocumentSuspendSubmissionResponse.from_dict(post_content_document_suspend_submission_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


