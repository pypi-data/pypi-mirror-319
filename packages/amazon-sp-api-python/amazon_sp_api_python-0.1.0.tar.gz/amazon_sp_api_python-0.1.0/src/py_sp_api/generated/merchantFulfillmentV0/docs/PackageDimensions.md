# PackageDimensions

The dimensions of a package contained in a shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**length** | **float** | A number that represents the given package dimension. | [optional] 
**width** | **float** | A number that represents the given package dimension. | [optional] 
**height** | **float** | A number that represents the given package dimension. | [optional] 
**unit** | [**UnitOfLength**](UnitOfLength.md) |  | [optional] 
**predefined_package_dimensions** | [**PredefinedPackageDimensions**](PredefinedPackageDimensions.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.package_dimensions import PackageDimensions

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


