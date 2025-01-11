# TransportationSelection

The transportation option selected to confirm.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact_information** | [**ContactInformation**](ContactInformation.md) |  | [optional] 
**shipment_id** | **str** | Shipment ID that the transportation Option is for. | 
**transportation_option_id** | **str** | Transportation option being selected for the provided shipment. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.transportation_selection import TransportationSelection

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationSelection from a JSON string
transportation_selection_instance = TransportationSelection.from_json(json)
# print the JSON string representation of the object
print(TransportationSelection.to_json())

# convert the object into a dict
transportation_selection_dict = transportation_selection_instance.to_dict()
# create an instance of TransportationSelection from a dict
transportation_selection_from_dict = TransportationSelection.from_dict(transportation_selection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


