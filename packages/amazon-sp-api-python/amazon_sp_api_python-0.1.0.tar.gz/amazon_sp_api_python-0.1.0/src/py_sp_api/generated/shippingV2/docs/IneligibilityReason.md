# IneligibilityReason

The reason why a shipping service offering is ineligible.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | [**IneligibilityReasonCode**](IneligibilityReasonCode.md) |  | 
**message** | **str** | The ineligibility reason. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.ineligibility_reason import IneligibilityReason

# TODO update the JSON string below
json = "{}"
# create an instance of IneligibilityReason from a JSON string
ineligibility_reason_instance = IneligibilityReason.from_json(json)
# print the JSON string representation of the object
print(IneligibilityReason.to_json())

# convert the object into a dict
ineligibility_reason_dict = ineligibility_reason_instance.to_dict()
# create an instance of IneligibilityReason from a dict
ineligibility_reason_from_dict = IneligibilityReason.from_dict(ineligibility_reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


