# ItemBrowseClassification

Classification (browse node) associated with an Amazon catalog item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | Display name for the classification (browse node). | 
**classification_id** | **str** | Identifier of the classification (browse node identifier). | 
**parent** | [**ItemBrowseClassification**](ItemBrowseClassification.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_browse_classification import ItemBrowseClassification

# TODO update the JSON string below
json = "{}"
# create an instance of ItemBrowseClassification from a JSON string
item_browse_classification_instance = ItemBrowseClassification.from_json(json)
# print the JSON string representation of the object
print(ItemBrowseClassification.to_json())

# convert the object into a dict
item_browse_classification_dict = item_browse_classification_instance.to_dict()
# create an instance of ItemBrowseClassification from a dict
item_browse_classification_from_dict = ItemBrowseClassification.from_dict(item_browse_classification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


