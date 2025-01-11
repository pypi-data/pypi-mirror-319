# UpdateItemComplianceDetailsRequest

The `updateItemComplianceDetails` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**msku** | **str** | The merchant SKU, a merchant-supplied identifier for a specific SKU. | 
**tax_details** | [**TaxDetails**](TaxDetails.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_item_compliance_details_request import UpdateItemComplianceDetailsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateItemComplianceDetailsRequest from a JSON string
update_item_compliance_details_request_instance = UpdateItemComplianceDetailsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateItemComplianceDetailsRequest.to_json())

# convert the object into a dict
update_item_compliance_details_request_dict = update_item_compliance_details_request_instance.to_dict()
# create an instance of UpdateItemComplianceDetailsRequest from a dict
update_item_compliance_details_request_from_dict = UpdateItemComplianceDetailsRequest.from_dict(update_item_compliance_details_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


