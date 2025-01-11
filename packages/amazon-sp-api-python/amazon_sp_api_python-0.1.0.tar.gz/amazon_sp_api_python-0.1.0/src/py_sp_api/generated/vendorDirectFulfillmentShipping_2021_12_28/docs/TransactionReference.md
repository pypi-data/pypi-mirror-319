# TransactionReference

Response containing the transaction ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | GUID to identify this transaction. This value can be used with the Transaction Status API to return the status of this transaction. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.transaction_reference import TransactionReference

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionReference from a JSON string
transaction_reference_instance = TransactionReference.from_json(json)
# print the JSON string representation of the object
print(TransactionReference.to_json())

# convert the object into a dict
transaction_reference_dict = transaction_reference_instance.to_dict()
# create an instance of TransactionReference from a dict
transaction_reference_from_dict = TransactionReference.from_dict(transaction_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


