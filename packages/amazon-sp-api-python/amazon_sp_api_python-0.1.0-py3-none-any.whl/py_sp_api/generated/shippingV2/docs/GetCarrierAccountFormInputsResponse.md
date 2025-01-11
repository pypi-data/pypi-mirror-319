# GetCarrierAccountFormInputsResponse

The Response  for the GetCarrierAccountFormInputsResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**linkable_carriers_list** | [**List[LinkableCarrier]**](LinkableCarrier.md) | A list of LinkableCarrier | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_carrier_account_form_inputs_response import GetCarrierAccountFormInputsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCarrierAccountFormInputsResponse from a JSON string
get_carrier_account_form_inputs_response_instance = GetCarrierAccountFormInputsResponse.from_json(json)
# print the JSON string representation of the object
print(GetCarrierAccountFormInputsResponse.to_json())

# convert the object into a dict
get_carrier_account_form_inputs_response_dict = get_carrier_account_form_inputs_response_instance.to_dict()
# create an instance of GetCarrierAccountFormInputsResponse from a dict
get_carrier_account_form_inputs_response_from_dict = GetCarrierAccountFormInputsResponse.from_dict(get_carrier_account_form_inputs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


