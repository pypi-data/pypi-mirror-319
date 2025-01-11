# PartneredEstimate

The estimated shipping cost for a shipment using an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | [**Amount**](Amount.md) |  | 
**confirm_deadline** | **datetime** | Timestamp in ISO 8601 format. | [optional] 
**void_deadline** | **datetime** | Timestamp in ISO 8601 format. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.partnered_estimate import PartneredEstimate

# TODO update the JSON string below
json = "{}"
# create an instance of PartneredEstimate from a JSON string
partnered_estimate_instance = PartneredEstimate.from_json(json)
# print the JSON string representation of the object
print(PartneredEstimate.to_json())

# convert the object into a dict
partnered_estimate_dict = partnered_estimate_instance.to_dict()
# create an instance of PartneredEstimate from a dict
partnered_estimate_from_dict = PartneredEstimate.from_dict(partnered_estimate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


