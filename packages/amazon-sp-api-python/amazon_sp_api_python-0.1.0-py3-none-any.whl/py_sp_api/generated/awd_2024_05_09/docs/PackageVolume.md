# PackageVolume

Represents the volume of the package with a unit of measurement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit_of_measurement** | [**VolumeUnitOfMeasurement**](VolumeUnitOfMeasurement.md) |  | 
**volume** | **float** | The package volume value. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.package_volume import PackageVolume

# TODO update the JSON string below
json = "{}"
# create an instance of PackageVolume from a JSON string
package_volume_instance = PackageVolume.from_json(json)
# print the JSON string representation of the object
print(PackageVolume.to_json())

# convert the object into a dict
package_volume_dict = package_volume_instance.to_dict()
# create an instance of PackageVolume from a dict
package_volume_from_dict = PackageVolume.from_dict(package_volume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


