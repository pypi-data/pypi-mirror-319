# DirectPayment

A payment made directly to a seller.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**direct_payment_type** | **str** | The type of payment.  Possible values:  * StoredValueCardRevenue - The amount that is deducted from the seller&#39;s account because the seller received money through a stored value card.  * StoredValueCardRefund - The amount that Amazon returns to the seller if the order that is bought using a stored value card is refunded.  * PrivateLabelCreditCardRevenue - The amount that is deducted from the seller&#39;s account because the seller received money through a private label credit card offered by Amazon.  * PrivateLabelCreditCardRefund - The amount that Amazon returns to the seller if the order that is bought using a private label credit card offered by Amazon is refunded.  * CollectOnDeliveryRevenue - The COD amount that the seller collected directly from the buyer.  * CollectOnDeliveryRefund - The amount that Amazon refunds to the buyer if an order paid for by COD is refunded. | [optional] 
**direct_payment_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.direct_payment import DirectPayment

# TODO update the JSON string below
json = "{}"
# create an instance of DirectPayment from a JSON string
direct_payment_instance = DirectPayment.from_json(json)
# print the JSON string representation of the object
print(DirectPayment.to_json())

# convert the object into a dict
direct_payment_dict = direct_payment_instance.to_dict()
# create an instance of DirectPayment from a dict
direct_payment_from_dict = DirectPayment.from_dict(direct_payment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


