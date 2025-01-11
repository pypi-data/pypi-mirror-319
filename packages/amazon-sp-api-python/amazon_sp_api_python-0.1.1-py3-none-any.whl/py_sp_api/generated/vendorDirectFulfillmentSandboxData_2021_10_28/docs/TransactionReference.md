# TransactionReference

A GUID assigned by Amazon to identify this transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | A GUID (Globally Unique Identifier) assigned by Amazon to uniquely identify the transaction. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.transaction_reference import TransactionReference

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


