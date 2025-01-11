# ItemContributor

Individual contributor to the creation of an item, such as an author or actor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role** | [**ItemContributorRole**](ItemContributorRole.md) |  | 
**value** | **str** | Name of the contributor, such as Jane Austen. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_contributor import ItemContributor

# TODO update the JSON string below
json = "{}"
# create an instance of ItemContributor from a JSON string
item_contributor_instance = ItemContributor.from_json(json)
# print the JSON string representation of the object
print(ItemContributor.to_json())

# convert the object into a dict
item_contributor_dict = item_contributor_instance.to_dict()
# create an instance of ItemContributor from a dict
item_contributor_from_dict = ItemContributor.from_dict(item_contributor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


