# MarketplaceFilter

An event filter to customize your subscription to send notifications for only the specified `marketplaceId`s.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_ids** | **List[str]** | A list of marketplace identifiers to subscribe to (for example: ATVPDKIKX0DER). To receive notifications in every marketplace, do not provide this list. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.marketplace_filter import MarketplaceFilter

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceFilter from a JSON string
marketplace_filter_instance = MarketplaceFilter.from_json(json)
# print the JSON string representation of the object
print(MarketplaceFilter.to_json())

# convert the object into a dict
marketplace_filter_dict = marketplace_filter_instance.to_dict()
# create an instance of MarketplaceFilter from a dict
marketplace_filter_from_dict = MarketplaceFilter.from_dict(marketplace_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


