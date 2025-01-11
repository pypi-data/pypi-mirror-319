# Granularity

Describes a granularity at which inventory data can be aggregated. For example, if you use Marketplace granularity, the fulfillable quantity will reflect inventory that could be fulfilled in the given marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**granularity_type** | **str** | The granularity type for the inventory aggregation level. | [optional] 
**granularity_id** | **str** | The granularity ID for the specified granularity type. When granularityType is Marketplace, specify the marketplaceId. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.granularity import Granularity

# TODO update the JSON string below
json = "{}"
# create an instance of Granularity from a JSON string
granularity_instance = Granularity.from_json(json)
# print the JSON string representation of the object
print(Granularity.to_json())

# convert the object into a dict
granularity_dict = granularity_instance.to_dict()
# create an instance of Granularity from a dict
granularity_from_dict = Granularity.from_dict(granularity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


