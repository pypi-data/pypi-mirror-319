# PrepDetails

The preparation details for a product. This contains the prep category, prep owner, and label owner. Prep instructions are generated based on the specified category.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_owner** | [**LabelOwner**](LabelOwner.md) |  | [optional] 
**prep_category** | **str** | The preparation category for shipping an item to Amazon&#39;s fulfillment network. | [optional] 
**prep_instructions** | [**List[PrepInstruction]**](PrepInstruction.md) | Information that pertains to the preparation of inbound products. This is generated based on the specified category. | [optional] 
**prep_owner** | [**PrepOwner**](PrepOwner.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.prep_details import PrepDetails

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


