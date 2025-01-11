# ResearchingQuantityEntry

The misplaced or warehouse damaged inventory that is actively being confirmed at our fulfillment centers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The duration of the research. | 
**quantity** | **int** | The number of units. | 

## Example

```python
from py_sp_api.generated.fbaInventory.models.researching_quantity_entry import ResearchingQuantityEntry

# TODO update the JSON string below
json = "{}"
# create an instance of ResearchingQuantityEntry from a JSON string
researching_quantity_entry_instance = ResearchingQuantityEntry.from_json(json)
# print the JSON string representation of the object
print(ResearchingQuantityEntry.to_json())

# convert the object into a dict
researching_quantity_entry_dict = researching_quantity_entry_instance.to_dict()
# create an instance of ResearchingQuantityEntry from a dict
researching_quantity_entry_from_dict = ResearchingQuantityEntry.from_dict(researching_quantity_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


