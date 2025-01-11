# NetworkComminglingTransactionEvent

A network commingling transaction event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_type** | **str** | The type of network item swap.  Possible values:  * NetCo - A Fulfillment by Amazon inventory pooling transaction. Available only in the India marketplace.  * ComminglingVAT - A commingling VAT transaction. Available only in the UK, Spain, France, Germany, and Italy marketplaces. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**net_co_transaction_id** | **str** | The identifier for the network item swap. | [optional] 
**swap_reason** | **str** | The reason for the network item swap. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the swapped item. | [optional] 
**marketplace_id** | **str** | The marketplace in which the event took place. | [optional] 
**tax_exclusive_amount** | [**Currency**](Currency.md) |  | [optional] 
**tax_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.network_commingling_transaction_event import NetworkComminglingTransactionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of NetworkComminglingTransactionEvent from a JSON string
network_commingling_transaction_event_instance = NetworkComminglingTransactionEvent.from_json(json)
# print the JSON string representation of the object
print(NetworkComminglingTransactionEvent.to_json())

# convert the object into a dict
network_commingling_transaction_event_dict = network_commingling_transaction_event_instance.to_dict()
# create an instance of NetworkComminglingTransactionEvent from a dict
network_commingling_transaction_event_from_dict = NetworkComminglingTransactionEvent.from_dict(network_commingling_transaction_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


