# Dimensions

Measurement of a package's dimensions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **float** | The height of a package. | 
**length** | **float** | The length of a package. | 
**unit_of_measurement** | [**UnitOfMeasurement**](UnitOfMeasurement.md) |  | 
**width** | **float** | The width of a package. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.dimensions import Dimensions

# TODO update the JSON string below
json = "{}"
# create an instance of Dimensions from a JSON string
dimensions_instance = Dimensions.from_json(json)
# print the JSON string representation of the object
print(Dimensions.to_json())

# convert the object into a dict
dimensions_dict = dimensions_instance.to_dict()
# create an instance of Dimensions from a dict
dimensions_from_dict = Dimensions.from_dict(dimensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


