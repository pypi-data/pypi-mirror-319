# RetrochargeEvent

A retrocharge or retrocharge reversal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**retrocharge_event_type** | **str** | The type of event.  Possible values:  * Retrocharge  * RetrochargeReversal | [optional] 
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**base_tax** | [**Currency**](Currency.md) |  | [optional] 
**shipping_tax** | [**Currency**](Currency.md) |  | [optional] 
**marketplace_name** | **str** | The name of the marketplace where the retrocharge event occurred. | [optional] 
**retrocharge_tax_withheld_list** | [**List[TaxWithheldComponent]**](TaxWithheldComponent.md) | A list of information about taxes withheld. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.retrocharge_event import RetrochargeEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RetrochargeEvent from a JSON string
retrocharge_event_instance = RetrochargeEvent.from_json(json)
# print the JSON string representation of the object
print(RetrochargeEvent.to_json())

# convert the object into a dict
retrocharge_event_dict = retrocharge_event_instance.to_dict()
# create an instance of RetrochargeEvent from a dict
retrocharge_event_from_dict = RetrochargeEvent.from_dict(retrocharge_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


