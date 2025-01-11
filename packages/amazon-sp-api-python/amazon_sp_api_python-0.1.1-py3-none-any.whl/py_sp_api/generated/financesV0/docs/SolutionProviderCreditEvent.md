# SolutionProviderCreditEvent

A credit given to a solution provider.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider_transaction_type** | **str** | The transaction type. | [optional] 
**seller_order_id** | **str** | A seller-defined identifier for an order. | [optional] 
**marketplace_id** | **str** | The identifier of the marketplace where the order was placed. | [optional] 
**marketplace_country_code** | **str** | The two-letter country code of the country associated with the marketplace where the order was placed. | [optional] 
**seller_id** | **str** | The Amazon-defined identifier of the seller. | [optional] 
**seller_store_name** | **str** | The store name where the payment event occurred. | [optional] 
**provider_id** | **str** | The Amazon-defined identifier of the solution provider. | [optional] 
**provider_store_name** | **str** | The store name where the payment event occurred. | [optional] 
**transaction_amount** | [**Currency**](Currency.md) |  | [optional] 
**transaction_creation_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.solution_provider_credit_event import SolutionProviderCreditEvent

# TODO update the JSON string below
json = "{}"
# create an instance of SolutionProviderCreditEvent from a JSON string
solution_provider_credit_event_instance = SolutionProviderCreditEvent.from_json(json)
# print the JSON string representation of the object
print(SolutionProviderCreditEvent.to_json())

# convert the object into a dict
solution_provider_credit_event_dict = solution_provider_credit_event_instance.to_dict()
# create an instance of SolutionProviderCreditEvent from a dict
solution_provider_credit_event_from_dict = SolutionProviderCreditEvent.from_dict(solution_provider_credit_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


