# Incentive

Contains details about cost related modifications to the placement cost.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Description of the incentive. | 
**target** | **str** | Target of the incentive. Possible values: &#39;Placement Services&#39;, &#39;Fulfillment Fee Discount&#39;. | 
**type** | **str** | Type of incentive. Possible values: &#x60;FEE&#x60;, &#x60;DISCOUNT&#x60;. | 
**value** | [**Currency**](Currency.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.incentive import Incentive

# TODO update the JSON string below
json = "{}"
# create an instance of Incentive from a JSON string
incentive_instance = Incentive.from_json(json)
# print the JSON string representation of the object
print(Incentive.to_json())

# convert the object into a dict
incentive_dict = incentive_instance.to_dict()
# create an instance of Incentive from a dict
incentive_from_dict = Incentive.from_dict(incentive_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


