# ItemOffersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**HttpResponseHeaders**](HttpResponseHeaders.md) |  | [optional] 
**status** | [**GetOffersHttpStatusLine**](GetOffersHttpStatusLine.md) |  | [optional] 
**body** | [**GetOffersResponse**](GetOffersResponse.md) |  | 
**request** | [**ItemOffersRequestParams**](ItemOffersRequestParams.md) |  | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.item_offers_response import ItemOffersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ItemOffersResponse from a JSON string
item_offers_response_instance = ItemOffersResponse.from_json(json)
# print the JSON string representation of the object
print(ItemOffersResponse.to_json())

# convert the object into a dict
item_offers_response_dict = item_offers_response_instance.to_dict()
# create an instance of ItemOffersResponse from a dict
item_offers_response_from_dict = ItemOffersResponse.from_dict(item_offers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


