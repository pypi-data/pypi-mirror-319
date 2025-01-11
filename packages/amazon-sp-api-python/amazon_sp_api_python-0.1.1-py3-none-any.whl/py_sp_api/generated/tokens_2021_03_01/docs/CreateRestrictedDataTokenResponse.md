# CreateRestrictedDataTokenResponse

The response schema for the createRestrictedDataToken operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**restricted_data_token** | **str** | A Restricted Data Token (RDT). This is a short-lived access token that authorizes calls to restricted operations. Pass this value with the x-amz-access-token header when making subsequent calls to these restricted resources. | [optional] 
**expires_in** | **int** | The lifetime of the Restricted Data Token, in seconds. | [optional] 

## Example

```python
from py_sp_api.generated.tokens_2021_03_01.models.create_restricted_data_token_response import CreateRestrictedDataTokenResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateRestrictedDataTokenResponse from a JSON string
create_restricted_data_token_response_instance = CreateRestrictedDataTokenResponse.from_json(json)
# print the JSON string representation of the object
print(CreateRestrictedDataTokenResponse.to_json())

# convert the object into a dict
create_restricted_data_token_response_dict = create_restricted_data_token_response_instance.to_dict()
# create an instance of CreateRestrictedDataTokenResponse from a dict
create_restricted_data_token_response_from_dict = CreateRestrictedDataTokenResponse.from_dict(create_restricted_data_token_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


