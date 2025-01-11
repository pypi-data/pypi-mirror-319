# DistributionPackage

Represents an AWD distribution package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contents** | [**DistributionPackageContents**](DistributionPackageContents.md) |  | 
**measurements** | [**MeasurementData**](MeasurementData.md) |  | 
**type** | [**DistributionPackageType**](DistributionPackageType.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.distribution_package import DistributionPackage

# TODO update the JSON string below
json = "{}"
# create an instance of DistributionPackage from a JSON string
distribution_package_instance = DistributionPackage.from_json(json)
# print the JSON string representation of the object
print(DistributionPackage.to_json())

# convert the object into a dict
distribution_package_dict = distribution_package_instance.to_dict()
# create an instance of DistributionPackage from a dict
distribution_package_from_dict = DistributionPackage.from_dict(distribution_package_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


