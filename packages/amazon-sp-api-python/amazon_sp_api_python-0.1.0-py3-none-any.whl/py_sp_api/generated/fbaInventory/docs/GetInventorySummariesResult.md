# GetInventorySummariesResult

The payload schema for the getInventorySummaries operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**granularity** | [**Granularity**](Granularity.md) |  | 
**inventory_summaries** | [**List[InventorySummary]**](InventorySummary.md) | A list of inventory summaries. | 

## Example

```python
from py_sp_api.generated.fbaInventory.models.get_inventory_summaries_result import GetInventorySummariesResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetInventorySummariesResult from a JSON string
get_inventory_summaries_result_instance = GetInventorySummariesResult.from_json(json)
# print the JSON string representation of the object
print(GetInventorySummariesResult.to_json())

# convert the object into a dict
get_inventory_summaries_result_dict = get_inventory_summaries_result_instance.to_dict()
# create an instance of GetInventorySummariesResult from a dict
get_inventory_summaries_result_from_dict = GetInventorySummariesResult.from_dict(get_inventory_summaries_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


