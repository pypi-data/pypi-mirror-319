# ItemContributorRole

Role of an individual contributor in the creation of an item, such as author or actor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | Display name of the role in the requested locale, such as Author or Actor. | [optional] 
**value** | **str** | Role value for the Amazon catalog item, such as author or actor. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_contributor_role import ItemContributorRole

# TODO update the JSON string below
json = "{}"
# create an instance of ItemContributorRole from a JSON string
item_contributor_role_instance = ItemContributorRole.from_json(json)
# print the JSON string representation of the object
print(ItemContributorRole.to_json())

# convert the object into a dict
item_contributor_role_dict = item_contributor_role_instance.to_dict()
# create an instance of ItemContributorRole from a dict
item_contributor_role_from_dict = ItemContributorRole.from_dict(item_contributor_role_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


