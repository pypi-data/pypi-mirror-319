# GetSupplySourcesResponse

The paginated list of supply sources.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_sources** | [**List[SupplySourceListInner]**](SupplySourceListInner.md) | The list of &#x60;SupplySource&#x60;s. | [optional] 
**next_page_token** | **str** | If present, use this pagination token to retrieve the next page of supply sources. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.get_supply_sources_response import GetSupplySourcesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSupplySourcesResponse from a JSON string
get_supply_sources_response_instance = GetSupplySourcesResponse.from_json(json)
# print the JSON string representation of the object
print(GetSupplySourcesResponse.to_json())

# convert the object into a dict
get_supply_sources_response_dict = get_supply_sources_response_instance.to_dict()
# create an instance of GetSupplySourcesResponse from a dict
get_supply_sources_response_from_dict = GetSupplySourcesResponse.from_dict(get_supply_sources_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


