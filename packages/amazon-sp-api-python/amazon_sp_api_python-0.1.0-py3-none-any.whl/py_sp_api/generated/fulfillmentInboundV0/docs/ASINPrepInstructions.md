# ASINPrepInstructions

Item preparation instructions to help with item sourcing decisions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**barcode_instruction** | [**BarcodeInstruction**](BarcodeInstruction.md) |  | [optional] 
**prep_guidance** | [**PrepGuidance**](PrepGuidance.md) |  | [optional] 
**prep_instruction_list** | [**List[PrepInstruction]**](PrepInstruction.md) | A list of preparation instructions to help with item sourcing decisions. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.asin_prep_instructions import ASINPrepInstructions

# TODO update the JSON string below
json = "{}"
# create an instance of ASINPrepInstructions from a JSON string
asin_prep_instructions_instance = ASINPrepInstructions.from_json(json)
# print the JSON string representation of the object
print(ASINPrepInstructions.to_json())

# convert the object into a dict
asin_prep_instructions_dict = asin_prep_instructions_instance.to_dict()
# create an instance of ASINPrepInstructions from a dict
asin_prep_instructions_from_dict = ASINPrepInstructions.from_dict(asin_prep_instructions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


