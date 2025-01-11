# InboundEligibility

Represents the eligibility status of the inbound packages.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ineligibility_reasons** | [**List[OrderIneligibilityReason]**](OrderIneligibilityReason.md) | If there are order level eligibility issues, then this list will contain those error codes and descriptions. | [optional] 
**packages_to_inbound** | [**List[SkuEligibility]**](SkuEligibility.md) | Details on SKU eligibility for each inbound package. | 
**previewed_at** | **datetime** | Timestamp when the eligibility check is performed. | 
**status** | [**InboundEligibilityStatus**](InboundEligibilityStatus.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_eligibility import InboundEligibility

# TODO update the JSON string below
json = "{}"
# create an instance of InboundEligibility from a JSON string
inbound_eligibility_instance = InboundEligibility.from_json(json)
# print the JSON string representation of the object
print(InboundEligibility.to_json())

# convert the object into a dict
inbound_eligibility_dict = inbound_eligibility_instance.to_dict()
# create an instance of InboundEligibility from a dict
inbound_eligibility_from_dict = InboundEligibility.from_dict(inbound_eligibility_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


