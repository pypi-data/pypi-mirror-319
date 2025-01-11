# GetPaymentMethodsResponse

The response schema for the `getPaymentMethods` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_methods** | [**List[PaymentMethodDetails]**](PaymentMethodDetails.md) | The list of payment methods with payment method details. | [optional] 

## Example

```python
from py_sp_api.generated.transfers_2024_06_01.models.get_payment_methods_response import GetPaymentMethodsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPaymentMethodsResponse from a JSON string
get_payment_methods_response_instance = GetPaymentMethodsResponse.from_json(json)
# print the JSON string representation of the object
print(GetPaymentMethodsResponse.to_json())

# convert the object into a dict
get_payment_methods_response_dict = get_payment_methods_response_instance.to_dict()
# create an instance of GetPaymentMethodsResponse from a dict
get_payment_methods_response_from_dict = GetPaymentMethodsResponse.from_dict(get_payment_methods_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


