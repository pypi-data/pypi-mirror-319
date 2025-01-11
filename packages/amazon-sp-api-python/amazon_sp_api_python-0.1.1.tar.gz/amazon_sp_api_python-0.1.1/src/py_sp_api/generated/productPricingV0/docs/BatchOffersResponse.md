# BatchOffersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**HttpResponseHeaders**](HttpResponseHeaders.md) |  | [optional] 
**status** | [**GetOffersHttpStatusLine**](GetOffersHttpStatusLine.md) |  | [optional] 
**body** | [**GetOffersResponse**](GetOffersResponse.md) |  | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.batch_offers_response import BatchOffersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BatchOffersResponse from a JSON string
batch_offers_response_instance = BatchOffersResponse.from_json(json)
# print the JSON string representation of the object
print(BatchOffersResponse.to_json())

# convert the object into a dict
batch_offers_response_dict = batch_offers_response_instance.to_dict()
# create an instance of BatchOffersResponse from a dict
batch_offers_response_from_dict = BatchOffersResponse.from_dict(batch_offers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


