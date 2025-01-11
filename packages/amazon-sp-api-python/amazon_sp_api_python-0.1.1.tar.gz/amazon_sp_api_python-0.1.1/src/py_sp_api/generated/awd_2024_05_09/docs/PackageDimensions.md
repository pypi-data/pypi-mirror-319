# PackageDimensions

Dimensions of the package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **float** | Height of the package. | 
**length** | **float** | Length of the package. | 
**unit_of_measurement** | [**DimensionUnitOfMeasurement**](DimensionUnitOfMeasurement.md) |  | 
**width** | **float** | Width of the package. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.package_dimensions import PackageDimensions

# TODO update the JSON string below
json = "{}"
# create an instance of PackageDimensions from a JSON string
package_dimensions_instance = PackageDimensions.from_json(json)
# print the JSON string representation of the object
print(PackageDimensions.to_json())

# convert the object into a dict
package_dimensions_dict = package_dimensions_instance.to_dict()
# create an instance of PackageDimensions from a dict
package_dimensions_from_dict = PackageDimensions.from_dict(package_dimensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


