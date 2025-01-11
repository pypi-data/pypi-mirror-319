# BatchRequest

Common properties of batch requests against individual APIs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uri** | **str** | The resource path of the operation you are calling in batch without any query parameters.  If you are calling &#x60;getItemOffersBatch&#x60;, supply the path of &#x60;getItemOffers&#x60;.  **Example:** &#x60;/products/pricing/v0/items/B000P6Q7MY/offers&#x60;  If you are calling &#x60;getListingOffersBatch&#x60;, supply the path of &#x60;getListingOffers&#x60;.  **Example:** &#x60;/products/pricing/v0/listings/B000P6Q7MY/offers&#x60; | 
**method** | [**HttpMethod**](HttpMethod.md) |  | 
**headers** | **Dict[str, str]** | A mapping of additional HTTP headers to send/receive for the individual batch request. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.batch_request import BatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BatchRequest from a JSON string
batch_request_instance = BatchRequest.from_json(json)
# print the JSON string representation of the object
print(BatchRequest.to_json())

# convert the object into a dict
batch_request_dict = batch_request_instance.to_dict()
# create an instance of BatchRequest from a dict
batch_request_from_dict = BatchRequest.from_dict(batch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


