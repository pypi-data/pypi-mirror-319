# PrepInstruction

Information pertaining to the preparation of inbound products.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prep_owner** | [**PrepOwner**](PrepOwner.md) |  | [optional] 
**prep_type** | **str** | The type of preparation to be done. For more information about preparing items, refer to [Prep guidance](https://sellercentral.amazon.com/help/hub/reference/external/GF4G7547KSLDX2KC) on Seller Central. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.prep_instruction import PrepInstruction

# TODO update the JSON string below
json = "{}"
# create an instance of PrepInstruction from a JSON string
prep_instruction_instance = PrepInstruction.from_json(json)
# print the JSON string representation of the object
print(PrepInstruction.to_json())

# convert the object into a dict
prep_instruction_dict = prep_instruction_instance.to_dict()
# create an instance of PrepInstruction from a dict
prep_instruction_from_dict = PrepInstruction.from_dict(prep_instruction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


