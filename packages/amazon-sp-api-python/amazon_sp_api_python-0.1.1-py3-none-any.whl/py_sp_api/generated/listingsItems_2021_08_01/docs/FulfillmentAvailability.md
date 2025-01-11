# FulfillmentAvailability

The fulfillment availability details for the listings item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_channel_code** | **str** | The code of the fulfillment network that will be used. | 
**quantity** | **int** | The quantity of the item you are making available for sale. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.fulfillment_availability import FulfillmentAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentAvailability from a JSON string
fulfillment_availability_instance = FulfillmentAvailability.from_json(json)
# print the JSON string representation of the object
print(FulfillmentAvailability.to_json())

# convert the object into a dict
fulfillment_availability_dict = fulfillment_availability_instance.to_dict()
# create an instance of FulfillmentAvailability from a dict
fulfillment_availability_from_dict = FulfillmentAvailability.from_dict(fulfillment_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


