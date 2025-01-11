# GetCarrierAccountsRequest

The request schema for the GetCarrierAccounts operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_carrier_accounts_request import GetCarrierAccountsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetCarrierAccountsRequest from a JSON string
get_carrier_accounts_request_instance = GetCarrierAccountsRequest.from_json(json)
# print the JSON string representation of the object
print(GetCarrierAccountsRequest.to_json())

# convert the object into a dict
get_carrier_accounts_request_dict = get_carrier_accounts_request_instance.to_dict()
# create an instance of GetCarrierAccountsRequest from a dict
get_carrier_accounts_request_from_dict = GetCarrierAccountsRequest.from_dict(get_carrier_accounts_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


