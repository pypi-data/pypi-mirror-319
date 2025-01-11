# TransactionIdentifier

The identifier for a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The transaction identifier name. Use the &#x60;getInvoicesAttributes&#x60; operation to check &#x60;transactionIdentifierName&#x60; options. | [optional] 
**id** | **str** | The transaction identifier. | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.transaction_identifier import TransactionIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionIdentifier from a JSON string
transaction_identifier_instance = TransactionIdentifier.from_json(json)
# print the JSON string representation of the object
print(TransactionIdentifier.to_json())

# convert the object into a dict
transaction_identifier_dict = transaction_identifier_instance.to_dict()
# create an instance of TransactionIdentifier from a dict
transaction_identifier_from_dict = TransactionIdentifier.from_dict(transaction_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


