# PrepDetails

Preparation instructions and who is responsible for the preparation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prep_instruction** | [**PrepInstruction**](PrepInstruction.md) |  | 
**prep_owner** | [**PrepOwner**](PrepOwner.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.prep_details import PrepDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PrepDetails from a JSON string
prep_details_instance = PrepDetails.from_json(json)
# print the JSON string representation of the object
print(PrepDetails.to_json())

# convert the object into a dict
prep_details_dict = prep_details_instance.to_dict()
# create an instance of PrepDetails from a dict
prep_details_from_dict = PrepDetails.from_dict(prep_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


