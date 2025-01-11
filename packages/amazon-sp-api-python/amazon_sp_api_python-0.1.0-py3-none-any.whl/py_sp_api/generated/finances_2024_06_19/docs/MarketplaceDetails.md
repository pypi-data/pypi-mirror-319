# MarketplaceDetails

Information about the marketplace where the transaction occurred.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The identifier of the marketplace where the transaction occured. | [optional] 
**marketplace_name** | **str** | The name of the marketplace where the transaction occurred. For example: &#x60;Amazon.com&#x60;,&#x60;Amazon.in&#x60; | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.marketplace_details import MarketplaceDetails

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceDetails from a JSON string
marketplace_details_instance = MarketplaceDetails.from_json(json)
# print the JSON string representation of the object
print(MarketplaceDetails.to_json())

# convert the object into a dict
marketplace_details_dict = marketplace_details_instance.to_dict()
# create an instance of MarketplaceDetails from a dict
marketplace_details_from_dict = MarketplaceDetails.from_dict(marketplace_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


