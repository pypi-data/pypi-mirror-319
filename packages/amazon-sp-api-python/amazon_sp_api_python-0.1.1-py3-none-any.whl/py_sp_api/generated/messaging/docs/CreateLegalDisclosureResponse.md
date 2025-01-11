# CreateLegalDisclosureResponse

The response schema for the createLegalDisclosure operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_legal_disclosure_response import CreateLegalDisclosureResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateLegalDisclosureResponse from a JSON string
create_legal_disclosure_response_instance = CreateLegalDisclosureResponse.from_json(json)
# print the JSON string representation of the object
print(CreateLegalDisclosureResponse.to_json())

# convert the object into a dict
create_legal_disclosure_response_dict = create_legal_disclosure_response_instance.to_dict()
# create an instance of CreateLegalDisclosureResponse from a dict
create_legal_disclosure_response_from_dict = CreateLegalDisclosureResponse.from_dict(create_legal_disclosure_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


