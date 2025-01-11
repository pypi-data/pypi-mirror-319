# PaymentTerms

Terms of the payment for the invoice. The basis of the payment terms is the invoice date.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The payment term type for the invoice. | [optional] 
**discount_percent** | **str** | A decimal number with no loss of precision. Useful when precision loss is unacceptable, as with currencies. Follows RFC7159 for number representation. &lt;br&gt;**Pattern** : &#x60;^-?(0|([1-9]\\d*))(\\.\\d+)?([eE][+-]?\\d+)?$&#x60;. | [optional] 
**discount_due_days** | **float** | The number of calendar days from the Base date (Invoice date) until the discount is no longer valid. | [optional] 
**net_due_days** | **float** | The number of calendar days from the base date (invoice date) until the total amount on the invoice is due. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.payment_terms import PaymentTerms

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentTerms from a JSON string
payment_terms_instance = PaymentTerms.from_json(json)
# print the JSON string representation of the object
print(PaymentTerms.to_json())

# convert the object into a dict
payment_terms_dict = payment_terms_instance.to_dict()
# create an instance of PaymentTerms from a dict
payment_terms_from_dict = PaymentTerms.from_dict(payment_terms_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


