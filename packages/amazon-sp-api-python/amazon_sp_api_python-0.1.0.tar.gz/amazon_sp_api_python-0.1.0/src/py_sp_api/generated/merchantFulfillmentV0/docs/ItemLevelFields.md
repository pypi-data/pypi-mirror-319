# ItemLevelFields

A list of item level fields.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | 
**additional_inputs** | [**List[AdditionalInputs]**](AdditionalInputs.md) | A list of additional inputs. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.item_level_fields import ItemLevelFields

# TODO update the JSON string below
json = "{}"
# create an instance of ItemLevelFields from a JSON string
item_level_fields_instance = ItemLevelFields.from_json(json)
# print the JSON string representation of the object
print(ItemLevelFields.to_json())

# convert the object into a dict
item_level_fields_dict = item_level_fields_instance.to_dict()
# create an instance of ItemLevelFields from a dict
item_level_fields_from_dict = ItemLevelFields.from_dict(item_level_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


