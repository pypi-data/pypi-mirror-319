# DistributionPackageQuantity

Represents a distribution package with its respective quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of cases or pallets with the same package configuration. | 
**distribution_package** | [**DistributionPackage**](DistributionPackage.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.distribution_package_quantity import DistributionPackageQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of DistributionPackageQuantity from a JSON string
distribution_package_quantity_instance = DistributionPackageQuantity.from_json(json)
# print the JSON string representation of the object
print(DistributionPackageQuantity.to_json())

# convert the object into a dict
distribution_package_quantity_dict = distribution_package_quantity_instance.to_dict()
# create an instance of DistributionPackageQuantity from a dict
distribution_package_quantity_from_dict = DistributionPackageQuantity.from_dict(distribution_package_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


