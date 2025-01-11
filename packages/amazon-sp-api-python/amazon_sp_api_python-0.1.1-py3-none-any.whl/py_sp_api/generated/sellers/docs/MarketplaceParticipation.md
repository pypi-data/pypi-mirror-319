# MarketplaceParticipation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace** | [**Marketplace**](Marketplace.md) |  | 
**participation** | [**Participation**](Participation.md) |  | 
**store_name** | **str** | The name of the seller&#39;s store as displayed in the marketplace. | 

## Example

```python
from py_sp_api.generated.sellers.models.marketplace_participation import MarketplaceParticipation

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceParticipation from a JSON string
marketplace_participation_instance = MarketplaceParticipation.from_json(json)
# print the JSON string representation of the object
print(MarketplaceParticipation.to_json())

# convert the object into a dict
marketplace_participation_dict = marketplace_participation_instance.to_dict()
# create an instance of MarketplaceParticipation from a dict
marketplace_participation_from_dict = MarketplaceParticipation.from_dict(marketplace_participation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


