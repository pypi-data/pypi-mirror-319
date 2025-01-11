# LinkCarrierAccountResponse

The Response  for the LinkCarrierAccount operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**registration_status** | [**AccountStatus**](AccountStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.link_carrier_account_response import LinkCarrierAccountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LinkCarrierAccountResponse from a JSON string
link_carrier_account_response_instance = LinkCarrierAccountResponse.from_json(json)
# print the JSON string representation of the object
print(LinkCarrierAccountResponse.to_json())

# convert the object into a dict
link_carrier_account_response_dict = link_carrier_account_response_instance.to_dict()
# create an instance of LinkCarrierAccountResponse from a dict
link_carrier_account_response_from_dict = LinkCarrierAccountResponse.from_dict(link_carrier_account_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


