# DistributionPackageContents

Represents the contents inside a package, which can be products or a nested package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packages** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | This is required only when &#x60;DistributionPackageType&#x3D;PALLET&#x60;. | [optional] 
**products** | [**List[ProductQuantity]**](ProductQuantity.md) | This is required only when &#x60;DistributionPackageType&#x3D;CASE&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.distribution_package_contents import DistributionPackageContents

# TODO update the JSON string below
json = "{}"
# create an instance of DistributionPackageContents from a JSON string
distribution_package_contents_instance = DistributionPackageContents.from_json(json)
# print the JSON string representation of the object
print(DistributionPackageContents.to_json())

# convert the object into a dict
distribution_package_contents_dict = distribution_package_contents_instance.to_dict()
# create an instance of DistributionPackageContents from a dict
distribution_package_contents_from_dict = DistributionPackageContents.from_dict(distribution_package_contents_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


