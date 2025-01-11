# LinkCarrierAccountRequest

The request schema for verify and add the merchant's account with a certain carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 
**carrier_account_type** | **str** | CarrierAccountType  associated with account. | 
**carrier_account_attributes** | [**List[CarrierAccountAttribute]**](CarrierAccountAttribute.md) | A list of all attributes required by the carrier in order to successfully link the merchant&#39;s account | 
**encrypted_carrier_account_attributes** | [**List[CarrierAccountAttribute]**](CarrierAccountAttribute.md) | A list of all attributes required by the carrier in order to successfully link the merchant&#39;s account | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.link_carrier_account_request import LinkCarrierAccountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LinkCarrierAccountRequest from a JSON string
link_carrier_account_request_instance = LinkCarrierAccountRequest.from_json(json)
# print the JSON string representation of the object
print(LinkCarrierAccountRequest.to_json())

# convert the object into a dict
link_carrier_account_request_dict = link_carrier_account_request_instance.to_dict()
# create an instance of LinkCarrierAccountRequest from a dict
link_carrier_account_request_from_dict = LinkCarrierAccountRequest.from_dict(link_carrier_account_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


