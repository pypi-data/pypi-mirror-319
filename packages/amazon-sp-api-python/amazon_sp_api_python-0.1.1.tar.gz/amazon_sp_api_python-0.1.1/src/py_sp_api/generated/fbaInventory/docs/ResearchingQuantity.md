# ResearchingQuantity

The number of misplaced or warehouse damaged units that are actively being confirmed at our fulfillment centers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_researching_quantity** | **int** | The total number of units currently being researched in Amazon&#39;s fulfillment network. | [optional] 
**researching_quantity_breakdown** | [**List[ResearchingQuantityEntry]**](ResearchingQuantityEntry.md) | A list of quantity details for items currently being researched. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.researching_quantity import ResearchingQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of ResearchingQuantity from a JSON string
researching_quantity_instance = ResearchingQuantity.from_json(json)
# print the JSON string representation of the object
print(ResearchingQuantity.to_json())

# convert the object into a dict
researching_quantity_dict = researching_quantity_instance.to_dict()
# create an instance of ResearchingQuantity from a dict
researching_quantity_from_dict = ResearchingQuantity.from_dict(researching_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


