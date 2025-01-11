# GetInventorySummariesResponse

The Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetInventorySummariesResult**](GetInventorySummariesResult.md) |  | [optional] 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.get_inventory_summaries_response import GetInventorySummariesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInventorySummariesResponse from a JSON string
get_inventory_summaries_response_instance = GetInventorySummariesResponse.from_json(json)
# print the JSON string representation of the object
print(GetInventorySummariesResponse.to_json())

# convert the object into a dict
get_inventory_summaries_response_dict = get_inventory_summaries_response_instance.to_dict()
# create an instance of GetInventorySummariesResponse from a dict
get_inventory_summaries_response_from_dict = GetInventorySummariesResponse.from_dict(get_inventory_summaries_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


