# AcknowledgementStatus

Status of acknowledgement.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Acknowledgement code is a unique two digit value which indicates the status of the acknowledgement. For a list of acknowledgement codes that Amazon supports, see the Vendor Direct Fulfillment APIs Use Case Guide. | [optional] 
**description** | **str** | Reason for the acknowledgement code. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.acknowledgement_status import AcknowledgementStatus

# TODO update the JSON string below
json = "{}"
# create an instance of AcknowledgementStatus from a JSON string
acknowledgement_status_instance = AcknowledgementStatus.from_json(json)
# print the JSON string representation of the object
print(AcknowledgementStatus.to_json())

# convert the object into a dict
acknowledgement_status_dict = acknowledgement_status_instance.to_dict()
# create an instance of AcknowledgementStatus from a dict
acknowledgement_status_from_dict = AcknowledgementStatus.from_dict(acknowledgement_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


