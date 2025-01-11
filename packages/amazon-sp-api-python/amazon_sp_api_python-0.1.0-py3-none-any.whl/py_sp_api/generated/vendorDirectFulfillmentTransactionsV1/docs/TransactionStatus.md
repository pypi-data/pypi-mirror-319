# TransactionStatus

The payload for the getTransactionStatus operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_status** | [**Transaction**](Transaction.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentTransactionsV1.models.transaction_status import TransactionStatus

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionStatus from a JSON string
transaction_status_instance = TransactionStatus.from_json(json)
# print the JSON string representation of the object
print(TransactionStatus.to_json())

# convert the object into a dict
transaction_status_dict = transaction_status_instance.to_dict()
# create an instance of TransactionStatus from a dict
transaction_status_from_dict = TransactionStatus.from_dict(transaction_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


