# Benefits

Representing the included/excluded benefits that we offer for each ShippingOffering/Rate. Benefits being services provided by Amazon when sellers purchase shipping through Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**included_benefits** | **List[str]** | A list of included benefits. | 
**excluded_benefits** | [**List[ExcludedBenefit]**](ExcludedBenefit.md) | A list of excluded benefit. Refer to the ExcludeBenefit object for further documentation | 

## Example

```python
from py_sp_api.generated.shippingV2.models.benefits import Benefits

# TODO update the JSON string below
json = "{}"
# create an instance of Benefits from a JSON string
benefits_instance = Benefits.from_json(json)
# print the JSON string representation of the object
print(Benefits.to_json())

# convert the object into a dict
benefits_dict = benefits_instance.to_dict()
# create an instance of Benefits from a dict
benefits_from_dict = Benefits.from_dict(benefits_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


