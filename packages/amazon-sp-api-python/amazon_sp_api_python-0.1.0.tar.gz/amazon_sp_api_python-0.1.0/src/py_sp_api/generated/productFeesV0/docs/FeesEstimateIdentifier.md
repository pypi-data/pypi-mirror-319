# FeesEstimateIdentifier

An item identifier, marketplace, time of request, and other details that identify an estimate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. | [optional] 
**seller_id** | **str** | The seller identifier. | [optional] 
**id_type** | [**IdType**](IdType.md) |  | [optional] 
**id_value** | **str** | The item identifier. | [optional] 
**is_amazon_fulfilled** | **bool** | When true, the offer is fulfilled by Amazon. | [optional] 
**price_to_estimate_fees** | [**PriceToEstimateFees**](PriceToEstimateFees.md) |  | [optional] 
**seller_input_identifier** | **str** | A unique identifier provided by the caller to track this request. | [optional] 
**optional_fulfillment_program** | [**OptionalFulfillmentProgram**](OptionalFulfillmentProgram.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate_identifier import FeesEstimateIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimateIdentifier from a JSON string
fees_estimate_identifier_instance = FeesEstimateIdentifier.from_json(json)
# print the JSON string representation of the object
print(FeesEstimateIdentifier.to_json())

# convert the object into a dict
fees_estimate_identifier_dict = fees_estimate_identifier_instance.to_dict()
# create an instance of FeesEstimateIdentifier from a dict
fees_estimate_identifier_from_dict = FeesEstimateIdentifier.from_dict(fees_estimate_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


