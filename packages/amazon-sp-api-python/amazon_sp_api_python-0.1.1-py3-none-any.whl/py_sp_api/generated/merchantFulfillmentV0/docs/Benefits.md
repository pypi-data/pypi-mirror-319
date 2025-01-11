# Benefits

Benefits that are included and excluded for each shipping offer. Benefits represents services provided by Amazon (for example, `CLAIMS_PROTECTED`) when sellers purchase shipping through Amazon. Benefit details are made available for any shipment placed on or after January 1st 2024 00:00 UTC.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**included_benefits** | **List[str]** | A list of included benefits. | [optional] 
**excluded_benefits** | [**List[ExcludedBenefit]**](ExcludedBenefit.md) | A list of excluded benefits. Refer to the &#x60;ExcludeBenefit&#x60; object for further documentation. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.benefits import Benefits

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


