# TransactionId

Response containing the transaction ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | GUID to identify this transaction. This value can be used with the Transaction Status API to return the status of this transaction. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.transaction_id import TransactionId

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionId from a JSON string
transaction_id_instance = TransactionId.from_json(json)
# print the JSON string representation of the object
print(TransactionId.to_json())

# convert the object into a dict
transaction_id_dict = transaction_id_instance.to_dict()
# create an instance of TransactionId from a dict
transaction_id_from_dict = TransactionId.from_dict(transaction_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


