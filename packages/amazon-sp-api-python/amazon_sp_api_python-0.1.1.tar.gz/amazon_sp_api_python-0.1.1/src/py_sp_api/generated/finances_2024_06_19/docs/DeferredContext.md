# DeferredContext

Additional information related to deferred transactions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deferral_reason** | **str** | Deferral policy applied on the transaction.  **Examples:** &#x60;B2B&#x60;,&#x60;DD7&#x60; | [optional] 
**maturity_date** | **datetime** | A date in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**deferral_status** | **str** | The status of the transaction. For example, &#x60;HOLD&#x60;,&#x60;RELEASE&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.deferred_context import DeferredContext

# TODO update the JSON string below
json = "{}"
# create an instance of DeferredContext from a JSON string
deferred_context_instance = DeferredContext.from_json(json)
# print the JSON string representation of the object
print(DeferredContext.to_json())

# convert the object into a dict
deferred_context_dict = deferred_context_instance.to_dict()
# create an instance of DeferredContext from a dict
deferred_context_from_dict = DeferredContext.from_dict(deferred_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


