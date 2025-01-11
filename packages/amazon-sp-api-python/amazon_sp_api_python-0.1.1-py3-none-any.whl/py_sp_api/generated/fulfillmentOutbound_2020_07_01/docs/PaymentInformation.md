# PaymentInformation

The attributes related to the payment made from customer to seller for this order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_transaction_id** | **str** | The transaction identifier of this payment. | 
**payment_mode** | **str** | The transaction mode of this payment. | 
**payment_date** | **datetime** | Date timestamp | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.payment_information import PaymentInformation

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentInformation from a JSON string
payment_information_instance = PaymentInformation.from_json(json)
# print the JSON string representation of the object
print(PaymentInformation.to_json())

# convert the object into a dict
payment_information_dict = payment_information_instance.to_dict()
# create an instance of PaymentInformation from a dict
payment_information_from_dict = PaymentInformation.from_dict(payment_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


