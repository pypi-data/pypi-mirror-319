# Context

Additional Information about the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**store_name** | **str** | The name of the store that is related to the transaction. | [optional] 
**order_type** | **str** | The transaction&#39;s order type. | [optional] 
**channel** | **str** | Channel details of related transaction. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**sku** | **str** | The Stock Keeping Unit (SKU) of the item. | [optional] 
**quantity_shipped** | **int** | The quantity of the item shipped. | [optional] 
**fulfillment_network** | **str** | The fulfillment network of the item. | [optional] 
**payment_type** | **str** | The type of payment. | [optional] 
**payment_method** | **str** | The method of payment. | [optional] 
**payment_reference** | **str** | The reference number of the payment. | [optional] 
**payment_date** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**deferral_reason** | **str** | Deferral policy applied on the transaction.  **Examples:** &#x60;B2B&#x60;,&#x60;DD7&#x60; | [optional] 
**maturity_date** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**deferral_status** | **str** | The status of the transaction. For example, &#x60;HOLD&#x60;,&#x60;RELEASE&#x60;. | [optional] 
**start_time** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**end_time** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**context_type** | **str** |  | 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.context import Context

# TODO update the JSON string below
json = "{}"
# create an instance of Context from a JSON string
context_instance = Context.from_json(json)
# print the JSON string representation of the object
print(Context.to_json())

# convert the object into a dict
context_dict = context_instance.to_dict()
# create an instance of Context from a dict
context_from_dict = Context.from_dict(context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


