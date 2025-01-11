# SKUPrepInstructions

Labeling requirements and item preparation instructions to help you prepare items for shipment to Amazon's fulfillment network.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**barcode_instruction** | [**BarcodeInstruction**](BarcodeInstruction.md) |  | [optional] 
**prep_guidance** | [**PrepGuidance**](PrepGuidance.md) |  | [optional] 
**prep_instruction_list** | [**List[PrepInstruction]**](PrepInstruction.md) | A list of preparation instructions to help with item sourcing decisions. | [optional] 
**amazon_prep_fees_details_list** | [**List[AmazonPrepFeesDetails]**](AmazonPrepFeesDetails.md) | A list of preparation instructions and fees for Amazon to prep goods for shipment. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.sku_prep_instructions import SKUPrepInstructions

# TODO update the JSON string below
json = "{}"
# create an instance of SKUPrepInstructions from a JSON string
sku_prep_instructions_instance = SKUPrepInstructions.from_json(json)
# print the JSON string representation of the object
print(SKUPrepInstructions.to_json())

# convert the object into a dict
sku_prep_instructions_dict = sku_prep_instructions_instance.to_dict()
# create an instance of SKUPrepInstructions from a dict
sku_prep_instructions_from_dict = SKUPrepInstructions.from_dict(sku_prep_instructions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


