# ChargeRefundTransaction

The charge refund transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**charge_amount** | [**Currency**](Currency.md) |  | [optional] 
**charge_type** | **str** | The type of charge. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.charge_refund_transaction import ChargeRefundTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ChargeRefundTransaction from a JSON string
charge_refund_transaction_instance = ChargeRefundTransaction.from_json(json)
# print the JSON string representation of the object
print(ChargeRefundTransaction.to_json())

# convert the object into a dict
charge_refund_transaction_dict = charge_refund_transaction_instance.to_dict()
# create an instance of ChargeRefundTransaction from a dict
charge_refund_transaction_from_dict = ChargeRefundTransaction.from_dict(charge_refund_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


