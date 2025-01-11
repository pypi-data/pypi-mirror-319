# Weight

The weight of the scheduled package

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **float** | The weight of the package. | [optional] 
**unit** | [**UnitOfWeight**](UnitOfWeight.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.weight import Weight

# TODO update the JSON string below
json = "{}"
# create an instance of Weight from a JSON string
weight_instance = Weight.from_json(json)
# print the JSON string representation of the object
print(Weight.to_json())

# convert the object into a dict
weight_dict = weight_instance.to_dict()
# create an instance of Weight from a dict
weight_from_dict = Weight.from_dict(weight_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


