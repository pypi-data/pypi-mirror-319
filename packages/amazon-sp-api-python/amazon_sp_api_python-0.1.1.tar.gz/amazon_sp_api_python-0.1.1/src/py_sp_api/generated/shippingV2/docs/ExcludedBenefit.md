# ExcludedBenefit

Object representing an excluded benefit that is excluded for an ShippingOffering/Rate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**benefit** | **str** |  | 
**reason_code** | **str** |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.excluded_benefit import ExcludedBenefit

# TODO update the JSON string below
json = "{}"
# create an instance of ExcludedBenefit from a JSON string
excluded_benefit_instance = ExcludedBenefit.from_json(json)
# print the JSON string representation of the object
print(ExcludedBenefit.to_json())

# convert the object into a dict
excluded_benefit_dict = excluded_benefit_instance.to_dict()
# create an instance of ExcludedBenefit from a dict
excluded_benefit_from_dict = ExcludedBenefit.from_dict(excluded_benefit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


