# Points

The number of Amazon Points that are offered with the purchase of an item and the monetary value of these points.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**points_number** | **int** | The number of Amazon Points. | [optional] 
**points_monetary_value** | [**MoneyType**](MoneyType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.points import Points

# TODO update the JSON string below
json = "{}"
# create an instance of Points from a JSON string
points_instance = Points.from_json(json)
# print the JSON string representation of the object
print(Points.to_json())

# convert the object into a dict
points_dict = points_instance.to_dict()
# create an instance of Points from a dict
points_from_dict = Points.from_dict(points_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


