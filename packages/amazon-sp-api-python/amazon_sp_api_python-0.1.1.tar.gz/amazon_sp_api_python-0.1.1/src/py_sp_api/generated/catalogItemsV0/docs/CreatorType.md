# CreatorType

The creator type attribute of an item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The value of the attribute. | [optional] 
**role** | **str** | The role of the value. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.creator_type import CreatorType

# TODO update the JSON string below
json = "{}"
# create an instance of CreatorType from a JSON string
creator_type_instance = CreatorType.from_json(json)
# print the JSON string representation of the object
print(CreatorType.to_json())

# convert the object into a dict
creator_type_dict = creator_type_instance.to_dict()
# create an instance of CreatorType from a dict
creator_type_from_dict = CreatorType.from_dict(creator_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


