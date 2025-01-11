# AmazonPrepFeesDetails

The fees for Amazon to prep goods for shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prep_instruction** | [**PrepInstruction**](PrepInstruction.md) |  | [optional] 
**fee_per_unit** | [**Amount**](Amount.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.amazon_prep_fees_details import AmazonPrepFeesDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AmazonPrepFeesDetails from a JSON string
amazon_prep_fees_details_instance = AmazonPrepFeesDetails.from_json(json)
# print the JSON string representation of the object
print(AmazonPrepFeesDetails.to_json())

# convert the object into a dict
amazon_prep_fees_details_dict = amazon_prep_fees_details_instance.to_dict()
# create an instance of AmazonPrepFeesDetails from a dict
amazon_prep_fees_details_from_dict = AmazonPrepFeesDetails.from_dict(amazon_prep_fees_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


