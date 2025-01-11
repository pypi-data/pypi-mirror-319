# UnlinkCarrierAccountResponse

The Response  for the UnlinkCarrierAccountResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_unlinked** | **bool** | Is Carrier unlinked from Merchant | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.unlink_carrier_account_response import UnlinkCarrierAccountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UnlinkCarrierAccountResponse from a JSON string
unlink_carrier_account_response_instance = UnlinkCarrierAccountResponse.from_json(json)
# print the JSON string representation of the object
print(UnlinkCarrierAccountResponse.to_json())

# convert the object into a dict
unlink_carrier_account_response_dict = unlink_carrier_account_response_instance.to_dict()
# create an instance of UnlinkCarrierAccountResponse from a dict
unlink_carrier_account_response_from_dict = UnlinkCarrierAccountResponse.from_dict(unlink_carrier_account_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


