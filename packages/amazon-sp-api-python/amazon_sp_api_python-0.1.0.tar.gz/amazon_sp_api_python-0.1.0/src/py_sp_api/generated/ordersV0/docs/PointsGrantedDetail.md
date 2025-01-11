# PointsGrantedDetail

The number of Amazon Points offered with the purchase of an item, and their monetary value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**points_number** | **int** | The number of Amazon Points granted with the purchase of an item. | [optional] 
**points_monetary_value** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.points_granted_detail import PointsGrantedDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PointsGrantedDetail from a JSON string
points_granted_detail_instance = PointsGrantedDetail.from_json(json)
# print the JSON string representation of the object
print(PointsGrantedDetail.to_json())

# convert the object into a dict
points_granted_detail_dict = points_granted_detail_instance.to_dict()
# create an instance of PointsGrantedDetail from a dict
points_granted_detail_from_dict = PointsGrantedDetail.from_dict(points_granted_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


