# IneligibleRate

Detailed information for an ineligible shipping service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **str** | An identifier for the shipping service. | 
**service_name** | **str** | The name of the shipping service. | 
**carrier_name** | **str** | The carrier name for the offering. | 
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | 
**ineligibility_reasons** | [**List[IneligibilityReason]**](IneligibilityReason.md) | A list of reasons why a shipping service offering is ineligible. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.ineligible_rate import IneligibleRate

# TODO update the JSON string below
json = "{}"
# create an instance of IneligibleRate from a JSON string
ineligible_rate_instance = IneligibleRate.from_json(json)
# print the JSON string representation of the object
print(IneligibleRate.to_json())

# convert the object into a dict
ineligible_rate_dict = ineligible_rate_instance.to_dict()
# create an instance of IneligibleRate from a dict
ineligible_rate_from_dict = IneligibleRate.from_dict(ineligible_rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


