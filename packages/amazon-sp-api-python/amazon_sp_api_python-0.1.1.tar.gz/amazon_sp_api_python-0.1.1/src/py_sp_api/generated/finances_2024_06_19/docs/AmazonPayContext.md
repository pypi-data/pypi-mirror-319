# AmazonPayContext

Additional information related to Amazon Pay.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**store_name** | **str** | The name of the store that is related to the transaction. | [optional] 
**order_type** | **str** | The transaction&#39;s order type. | [optional] 
**channel** | **str** | Channel details of related transaction. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.amazon_pay_context import AmazonPayContext

# TODO update the JSON string below
json = "{}"
# create an instance of AmazonPayContext from a JSON string
amazon_pay_context_instance = AmazonPayContext.from_json(json)
# print the JSON string representation of the object
print(AmazonPayContext.to_json())

# convert the object into a dict
amazon_pay_context_dict = amazon_pay_context_instance.to_dict()
# create an instance of AmazonPayContext from a dict
amazon_pay_context_from_dict = AmazonPayContext.from_dict(amazon_pay_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


