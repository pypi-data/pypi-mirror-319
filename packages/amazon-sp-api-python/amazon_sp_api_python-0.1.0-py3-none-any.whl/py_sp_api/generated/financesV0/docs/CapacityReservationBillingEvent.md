# CapacityReservationBillingEvent

An event related to a capacity reservation billing charge.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_type** | **str** | Indicates the type of transaction. For example, FBA Inventory Fee | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**description** | **str** | A short description of the capacity reservation billing event. | [optional] 
**transaction_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.capacity_reservation_billing_event import CapacityReservationBillingEvent

# TODO update the JSON string below
json = "{}"
# create an instance of CapacityReservationBillingEvent from a JSON string
capacity_reservation_billing_event_instance = CapacityReservationBillingEvent.from_json(json)
# print the JSON string representation of the object
print(CapacityReservationBillingEvent.to_json())

# convert the object into a dict
capacity_reservation_billing_event_dict = capacity_reservation_billing_event_instance.to_dict()
# create an instance of CapacityReservationBillingEvent from a dict
capacity_reservation_billing_event_from_dict = CapacityReservationBillingEvent.from_dict(capacity_reservation_billing_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


