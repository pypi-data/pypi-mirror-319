# ImagingServicesFeeEvent

A fee event related to Amazon Imaging services.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**imaging_request_billing_item_id** | **str** | The identifier for the imaging services request. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item for which the imaging service was requested. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.imaging_services_fee_event import ImagingServicesFeeEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ImagingServicesFeeEvent from a JSON string
imaging_services_fee_event_instance = ImagingServicesFeeEvent.from_json(json)
# print the JSON string representation of the object
print(ImagingServicesFeeEvent.to_json())

# convert the object into a dict
imaging_services_fee_event_dict = imaging_services_fee_event_instance.to_dict()
# create an instance of ImagingServicesFeeEvent from a dict
imaging_services_fee_event_from_dict = ImagingServicesFeeEvent.from_dict(imaging_services_fee_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


