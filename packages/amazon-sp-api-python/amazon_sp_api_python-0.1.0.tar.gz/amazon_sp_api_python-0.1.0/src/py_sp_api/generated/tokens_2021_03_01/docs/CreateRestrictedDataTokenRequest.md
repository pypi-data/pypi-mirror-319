# CreateRestrictedDataTokenRequest

The request schema for the createRestrictedDataToken operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_application** | **str** | The application ID for the target application to which access is being delegated. | [optional] 
**restricted_resources** | [**List[RestrictedResource]**](RestrictedResource.md) | A list of restricted resources. Maximum: 50 | 

## Example

```python
from py_sp_api.generated.tokens_2021_03_01.models.create_restricted_data_token_request import CreateRestrictedDataTokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateRestrictedDataTokenRequest from a JSON string
create_restricted_data_token_request_instance = CreateRestrictedDataTokenRequest.from_json(json)
# print the JSON string representation of the object
print(CreateRestrictedDataTokenRequest.to_json())

# convert the object into a dict
create_restricted_data_token_request_dict = create_restricted_data_token_request_instance.to_dict()
# create an instance of CreateRestrictedDataTokenRequest from a dict
create_restricted_data_token_request_from_dict = CreateRestrictedDataTokenRequest.from_dict(create_restricted_data_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


