# ChargeComponent

The type and amount of a charge applied on a package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | [**Currency**](Currency.md) |  | [optional] 
**charge_type** | **str** | The type of charge. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.charge_component import ChargeComponent

# TODO update the JSON string below
json = "{}"
# create an instance of ChargeComponent from a JSON string
charge_component_instance = ChargeComponent.from_json(json)
# print the JSON string representation of the object
print(ChargeComponent.to_json())

# convert the object into a dict
charge_component_dict = charge_component_instance.to_dict()
# create an instance of ChargeComponent from a dict
charge_component_from_dict = ChargeComponent.from_dict(charge_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


