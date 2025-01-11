# SkuEligibility

Represents eligibility of one SKU.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ineligibility_reasons** | [**List[SkuIneligibilityReason]**](SkuIneligibilityReason.md) | If not eligible, these are list of error codes and descriptions. | [optional] 
**package_quantity** | [**DistributionPackageQuantity**](DistributionPackageQuantity.md) |  | 
**status** | [**InboundEligibilityStatus**](InboundEligibilityStatus.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.sku_eligibility import SkuEligibility

# TODO update the JSON string below
json = "{}"
# create an instance of SkuEligibility from a JSON string
sku_eligibility_instance = SkuEligibility.from_json(json)
# print the JSON string representation of the object
print(SkuEligibility.to_json())

# convert the object into a dict
sku_eligibility_dict = sku_eligibility_instance.to_dict()
# create an instance of SkuEligibility from a dict
sku_eligibility_from_dict = SkuEligibility.from_dict(sku_eligibility_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


