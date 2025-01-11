# FeesEstimateRequest

A product, marketplace, and proposed price used to request estimated fees.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. | 
**is_amazon_fulfilled** | **bool** | When true, the offer is fulfilled by Amazon. | [optional] 
**price_to_estimate_fees** | [**PriceToEstimateFees**](PriceToEstimateFees.md) |  | 
**identifier** | **str** | A unique identifier provided by the caller to track this request. | 
**optional_fulfillment_program** | [**OptionalFulfillmentProgram**](OptionalFulfillmentProgram.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate_request import FeesEstimateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimateRequest from a JSON string
fees_estimate_request_instance = FeesEstimateRequest.from_json(json)
# print the JSON string representation of the object
print(FeesEstimateRequest.to_json())

# convert the object into a dict
fees_estimate_request_dict = fees_estimate_request_instance.to_dict()
# create an instance of FeesEstimateRequest from a dict
fees_estimate_request_from_dict = FeesEstimateRequest.from_dict(fees_estimate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


