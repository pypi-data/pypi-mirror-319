# ListItemComplianceDetailsResponse

The `listItemComplianceDetails` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**compliance_details** | [**List[ComplianceDetail]**](ComplianceDetail.md) | List of compliance details. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_item_compliance_details_response import ListItemComplianceDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListItemComplianceDetailsResponse from a JSON string
list_item_compliance_details_response_instance = ListItemComplianceDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(ListItemComplianceDetailsResponse.to_json())

# convert the object into a dict
list_item_compliance_details_response_dict = list_item_compliance_details_response_instance.to_dict()
# create an instance of ListItemComplianceDetailsResponse from a dict
list_item_compliance_details_response_from_dict = ListItemComplianceDetailsResponse.from_dict(list_item_compliance_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


