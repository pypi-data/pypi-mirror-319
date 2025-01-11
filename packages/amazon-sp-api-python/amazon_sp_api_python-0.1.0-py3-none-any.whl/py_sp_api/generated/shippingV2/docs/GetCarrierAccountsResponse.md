# GetCarrierAccountsResponse

The Response  for the GetCarrierAccountsResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_accounts** | [**List[ActiveAccount]**](ActiveAccount.md) | A list of ActiveAccount | 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_carrier_accounts_response import GetCarrierAccountsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCarrierAccountsResponse from a JSON string
get_carrier_accounts_response_instance = GetCarrierAccountsResponse.from_json(json)
# print the JSON string representation of the object
print(GetCarrierAccountsResponse.to_json())

# convert the object into a dict
get_carrier_accounts_response_dict = get_carrier_accounts_response_instance.to_dict()
# create an instance of GetCarrierAccountsResponse from a dict
get_carrier_accounts_response_from_dict = GetCarrierAccountsResponse.from_dict(get_carrier_accounts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


