# ListTransactionsResponse

The response schema for the `listTransactions` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | The response includes &#x60;nextToken&#x60; when the number of results exceeds the specified &#x60;pageSize&#x60; value. To get the next page of results, call the operation with this token and include the same arguments as the call that produced the token. To get a complete list, call this operation until &#x60;nextToken&#x60; is null. Note that this operation can return empty pages. | [optional] 
**transactions** | [**List[Transaction]**](Transaction.md) | A list of transactions within the specified time period. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.list_transactions_response import ListTransactionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListTransactionsResponse from a JSON string
list_transactions_response_instance = ListTransactionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListTransactionsResponse.to_json())

# convert the object into a dict
list_transactions_response_dict = list_transactions_response_instance.to_dict()
# create an instance of ListTransactionsResponse from a dict
list_transactions_response_from_dict = ListTransactionsResponse.from_dict(list_transactions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


