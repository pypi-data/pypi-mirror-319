# GetMarketplaceParticipationsResponse

The response schema for the `getMarketplaceParticipations` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[MarketplaceParticipation]**](MarketplaceParticipation.md) | List of marketplace participations. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.sellers.models.get_marketplace_participations_response import GetMarketplaceParticipationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetMarketplaceParticipationsResponse from a JSON string
get_marketplace_participations_response_instance = GetMarketplaceParticipationsResponse.from_json(json)
# print the JSON string representation of the object
print(GetMarketplaceParticipationsResponse.to_json())

# convert the object into a dict
get_marketplace_participations_response_dict = get_marketplace_participations_response_instance.to_dict()
# create an instance of GetMarketplaceParticipationsResponse from a dict
get_marketplace_participations_response_from_dict = GetMarketplaceParticipationsResponse.from_dict(get_marketplace_participations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


