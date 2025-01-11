# PostContentDocumentApprovalSubmissionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_approval_submission_response import PostContentDocumentApprovalSubmissionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentApprovalSubmissionResponse from a JSON string
post_content_document_approval_submission_response_instance = PostContentDocumentApprovalSubmissionResponse.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentApprovalSubmissionResponse.to_json())

# convert the object into a dict
post_content_document_approval_submission_response_dict = post_content_document_approval_submission_response_instance.to_dict()
# create an instance of PostContentDocumentApprovalSubmissionResponse from a dict
post_content_document_approval_submission_response_from_dict = PostContentDocumentApprovalSubmissionResponse.from_dict(post_content_document_approval_submission_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


