# UpdateItemComplianceDetailsResponse

The `updateItemComplianceDetails` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_item_compliance_details_response import UpdateItemComplianceDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateItemComplianceDetailsResponse from a JSON string
update_item_compliance_details_response_instance = UpdateItemComplianceDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateItemComplianceDetailsResponse.to_json())

# convert the object into a dict
update_item_compliance_details_response_dict = update_item_compliance_details_response_instance.to_dict()
# create an instance of UpdateItemComplianceDetailsResponse from a dict
update_item_compliance_details_response_from_dict = UpdateItemComplianceDetailsResponse.from_dict(update_item_compliance_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


