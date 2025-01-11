# FeeComponent

A fee associated with the event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fee_type** | **str** | The type of fee. For more information about Selling on Amazon fees, see [Selling on Amazon Fee Schedule](https://sellercentral.amazon.com/gp/help/200336920) on Seller Central. For more information about Fulfillment by Amazon fees, see [FBA features, services and fees](https://sellercentral.amazon.com/gp/help/201074400) on Seller Central. | [optional] 
**fee_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.fee_component import FeeComponent

# TODO update the JSON string below
json = "{}"
# create an instance of FeeComponent from a JSON string
fee_component_instance = FeeComponent.from_json(json)
# print the JSON string representation of the object
print(FeeComponent.to_json())

# convert the object into a dict
fee_component_dict = fee_component_instance.to_dict()
# create an instance of FeeComponent from a dict
fee_component_from_dict = FeeComponent.from_dict(fee_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


