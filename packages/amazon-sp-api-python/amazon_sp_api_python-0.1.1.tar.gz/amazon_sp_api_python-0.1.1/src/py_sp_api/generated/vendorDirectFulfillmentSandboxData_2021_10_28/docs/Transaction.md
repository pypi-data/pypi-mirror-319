# Transaction

The transaction details including the status. If the transaction was successful, also includes the requested test order data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | The unique identifier returned in the response to the generateOrderScenarios request. | 
**status** | **str** | The current processing status of the transaction. | 
**test_case_data** | [**TestCaseData**](TestCaseData.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.transaction import Transaction

# TODO update the JSON string below
json = "{}"
# create an instance of Transaction from a JSON string
transaction_instance = Transaction.from_json(json)
# print the JSON string representation of the object
print(Transaction.to_json())

# convert the object into a dict
transaction_dict = transaction_instance.to_dict()
# create an instance of Transaction from a dict
transaction_from_dict = Transaction.from_dict(transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


