# ValueAddedServiceChargeEvent

An event related to a value added service charge.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_type** | **str** | Indicates the type of transaction.  Example: &#39;Other Support Service fees&#39; | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**description** | **str** | A short description of the service charge event. | [optional] 
**transaction_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.value_added_service_charge_event import ValueAddedServiceChargeEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ValueAddedServiceChargeEvent from a JSON string
value_added_service_charge_event_instance = ValueAddedServiceChargeEvent.from_json(json)
# print the JSON string representation of the object
print(ValueAddedServiceChargeEvent.to_json())

# convert the object into a dict
value_added_service_charge_event_dict = value_added_service_charge_event_instance.to_dict()
# create an instance of ValueAddedServiceChargeEvent from a dict
value_added_service_charge_event_from_dict = ValueAddedServiceChargeEvent.from_dict(value_added_service_charge_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


