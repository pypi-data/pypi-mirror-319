# MeasurementData

Package weight and dimension.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**PackageDimensions**](PackageDimensions.md) |  | [optional] 
**volume** | [**PackageVolume**](PackageVolume.md) |  | [optional] 
**weight** | [**PackageWeight**](PackageWeight.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.measurement_data import MeasurementData

# TODO update the JSON string below
json = "{}"
# create an instance of MeasurementData from a JSON string
measurement_data_instance = MeasurementData.from_json(json)
# print the JSON string representation of the object
print(MeasurementData.to_json())

# convert the object into a dict
measurement_data_dict = measurement_data_instance.to_dict()
# create an instance of MeasurementData from a dict
measurement_data_from_dict = MeasurementData.from_dict(measurement_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


