# AcknowledgementStatusDetails

Details of item quantity ordered

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acknowledgement_date** | **datetime** | The date when the line item was confirmed by vendor. Must be in ISO-8601 date/time format. | [optional] 
**accepted_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**rejected_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.acknowledgement_status_details import AcknowledgementStatusDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AcknowledgementStatusDetails from a JSON string
acknowledgement_status_details_instance = AcknowledgementStatusDetails.from_json(json)
# print the JSON string representation of the object
print(AcknowledgementStatusDetails.to_json())

# convert the object into a dict
acknowledgement_status_details_dict = acknowledgement_status_details_instance.to_dict()
# create an instance of AcknowledgementStatusDetails from a dict
acknowledgement_status_details_from_dict = AcknowledgementStatusDetails.from_dict(acknowledgement_status_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


