# GetPrepInstructionsResult

Result for the get prep instructions operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku_prep_instructions_list** | [**List[SKUPrepInstructions]**](SKUPrepInstructions.md) | A list of SKU labeling requirements and item preparation instructions. | [optional] 
**invalid_sku_list** | [**List[InvalidSKU]**](InvalidSKU.md) | A list of invalid SKU values and the reason they are invalid. | [optional] 
**asin_prep_instructions_list** | [**List[ASINPrepInstructions]**](ASINPrepInstructions.md) | A list of item preparation instructions. | [optional] 
**invalid_asin_list** | [**List[InvalidASIN]**](InvalidASIN.md) | A list of invalid ASIN values and the reasons they are invalid. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_prep_instructions_result import GetPrepInstructionsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetPrepInstructionsResult from a JSON string
get_prep_instructions_result_instance = GetPrepInstructionsResult.from_json(json)
# print the JSON string representation of the object
print(GetPrepInstructionsResult.to_json())

# convert the object into a dict
get_prep_instructions_result_dict = get_prep_instructions_result_instance.to_dict()
# create an instance of GetPrepInstructionsResult from a dict
get_prep_instructions_result_from_dict = GetPrepInstructionsResult.from_dict(get_prep_instructions_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


