# UnlinkCarrierAccountRequest

The request schema for remove the Carrier Account associated with the provided merchant.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.unlink_carrier_account_request import UnlinkCarrierAccountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UnlinkCarrierAccountRequest from a JSON string
unlink_carrier_account_request_instance = UnlinkCarrierAccountRequest.from_json(json)
# print the JSON string representation of the object
print(UnlinkCarrierAccountRequest.to_json())

# convert the object into a dict
unlink_carrier_account_request_dict = unlink_carrier_account_request_instance.to_dict()
# create an instance of UnlinkCarrierAccountRequest from a dict
unlink_carrier_account_request_from_dict = UnlinkCarrierAccountRequest.from_dict(unlink_carrier_account_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


