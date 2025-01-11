# CreateLegalDisclosureRequest

The request schema for the createLegalDisclosure operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attachments** | [**List[Attachment]**](Attachment.md) | Attachments to include in the message to the buyer. If any text is included in the attachment, the text must be written in the buyer&#39;s language of preference, which can be retrieved from the GetAttributes operation. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_legal_disclosure_request import CreateLegalDisclosureRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateLegalDisclosureRequest from a JSON string
create_legal_disclosure_request_instance = CreateLegalDisclosureRequest.from_json(json)
# print the JSON string representation of the object
print(CreateLegalDisclosureRequest.to_json())

# convert the object into a dict
create_legal_disclosure_request_dict = create_legal_disclosure_request_instance.to_dict()
# create an instance of CreateLegalDisclosureRequest from a dict
create_legal_disclosure_request_from_dict = CreateLegalDisclosureRequest.from_dict(create_legal_disclosure_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


