# SkuIneligibilityReason

Represents the ineligibility reason for one SKU.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Code for the SKU ineligibility. | 
**description** | **str** | Detailed description of the SKU ineligibility. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.sku_ineligibility_reason import SkuIneligibilityReason

# TODO update the JSON string below
json = "{}"
# create an instance of SkuIneligibilityReason from a JSON string
sku_ineligibility_reason_instance = SkuIneligibilityReason.from_json(json)
# print the JSON string representation of the object
print(SkuIneligibilityReason.to_json())

# convert the object into a dict
sku_ineligibility_reason_dict = sku_ineligibility_reason_instance.to_dict()
# create an instance of SkuIneligibilityReason from a dict
sku_ineligibility_reason_from_dict = SkuIneligibilityReason.from_dict(sku_ineligibility_reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


