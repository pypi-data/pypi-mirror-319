# ItemEligibilityPreview

The response object which contains the ASIN, marketplaceId if required, eligibility program, the eligibility status (boolean), and a list of ineligibility reason codes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The ASIN for which eligibility was determined. | 
**marketplace_id** | **str** | The marketplace for which eligibility was determined. | [optional] 
**program** | **str** | The program for which eligibility was determined. | 
**is_eligible_for_program** | **bool** | Indicates if the item is eligible for the program. | 
**ineligibility_reason_list** | **List[str]** | Potential Ineligibility Reason Codes. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInbound.models.item_eligibility_preview import ItemEligibilityPreview

# TODO update the JSON string below
json = "{}"
# create an instance of ItemEligibilityPreview from a JSON string
item_eligibility_preview_instance = ItemEligibilityPreview.from_json(json)
# print the JSON string representation of the object
print(ItemEligibilityPreview.to_json())

# convert the object into a dict
item_eligibility_preview_dict = item_eligibility_preview_instance.to_dict()
# create an instance of ItemEligibilityPreview from a dict
item_eligibility_preview_from_dict = ItemEligibilityPreview.from_dict(item_eligibility_preview_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


