# PaymentMethodDetails

The details of a payment method.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_holder_name** | **str** | The name of the account holder who is registered for the payment method. | [optional] 
**payment_method_id** | **str** | The payment method identifier. | [optional] 
**tail** | **str** | The last three or four digits of the payment method. | [optional] 
**expiry_date** | [**ExpiryDate**](ExpiryDate.md) |  | [optional] 
**country_code** | **str** | The two-letter country code in ISO 3166-1 alpha-2 format. For payment methods in the &#x60;card&#x60; category, the code is for the country where the card was issued. For payment methods in the &#x60;bank account&#x60; category, the code is for the country where the account is located. | [optional] 
**payment_method_type** | [**PaymentMethodType**](PaymentMethodType.md) |  | [optional] 
**assignment_type** | [**AssignmentType**](AssignmentType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.transfers_2024_06_01.models.payment_method_details import PaymentMethodDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodDetails from a JSON string
payment_method_details_instance = PaymentMethodDetails.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodDetails.to_json())

# convert the object into a dict
payment_method_details_dict = payment_method_details_instance.to_dict()
# create an instance of PaymentMethodDetails from a dict
payment_method_details_from_dict = PaymentMethodDetails.from_dict(payment_method_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


