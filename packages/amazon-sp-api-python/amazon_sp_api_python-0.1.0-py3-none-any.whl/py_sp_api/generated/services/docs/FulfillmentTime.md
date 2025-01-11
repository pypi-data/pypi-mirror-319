# FulfillmentTime

Input for fulfillment time details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** | The date, time in UTC of the fulfillment start time in ISO 8601 format. | [optional] 
**end_time** | **datetime** | The date, time in UTC of the fulfillment end time in ISO 8601 format. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.fulfillment_time import FulfillmentTime

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentTime from a JSON string
fulfillment_time_instance = FulfillmentTime.from_json(json)
# print the JSON string representation of the object
print(FulfillmentTime.to_json())

# convert the object into a dict
fulfillment_time_dict = fulfillment_time_instance.to_dict()
# create an instance of FulfillmentTime from a dict
fulfillment_time_from_dict = FulfillmentTime.from_dict(fulfillment_time_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


