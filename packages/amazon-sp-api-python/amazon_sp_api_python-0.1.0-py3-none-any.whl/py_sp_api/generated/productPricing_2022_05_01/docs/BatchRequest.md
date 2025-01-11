# BatchRequest

The common properties for individual requests within a batch.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uri** | **str** | The URI associated with an individual request within a batch. For &#x60;FeaturedOfferExpectedPrice&#x60;, this is &#x60;/products/pricing/2022-05-01/offer/featuredOfferExpectedPrice&#x60;. | 
**method** | [**HttpMethod**](HttpMethod.md) |  | 
**body** | **Dict[str, object]** | Additional HTTP body information that is associated with an individual request within a batch. | [optional] 
**headers** | **Dict[str, str]** | A mapping of additional HTTP headers to send or receive for an individual request within a batch. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.batch_request import BatchRequest

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


