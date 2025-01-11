# PackageWeight

Represents the weight of the package with a unit of measurement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit_of_measurement** | [**WeightUnitOfMeasurement**](WeightUnitOfMeasurement.md) |  | 
**weight** | **float** | The package weight value. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.package_weight import PackageWeight

# TODO update the JSON string below
json = "{}"
# create an instance of PackageWeight from a JSON string
package_weight_instance = PackageWeight.from_json(json)
# print the JSON string representation of the object
print(PackageWeight.to_json())

# convert the object into a dict
package_weight_dict = package_weight_instance.to_dict()
# create an instance of PackageWeight from a dict
package_weight_from_dict = PackageWeight.from_dict(package_weight_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


