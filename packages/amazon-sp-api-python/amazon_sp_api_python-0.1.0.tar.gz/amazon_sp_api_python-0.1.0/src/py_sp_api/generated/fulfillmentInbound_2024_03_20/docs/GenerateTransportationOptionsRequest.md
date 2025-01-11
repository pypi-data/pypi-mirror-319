# GenerateTransportationOptionsRequest

The `generateTransportationOptions` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**placement_option_id** | **str** | The placement option to generate transportation options for. | 
**shipment_transportation_configurations** | [**List[ShipmentTransportationConfiguration]**](ShipmentTransportationConfiguration.md) | List of shipment transportation configurations. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_transportation_options_request import GenerateTransportationOptionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateTransportationOptionsRequest from a JSON string
generate_transportation_options_request_instance = GenerateTransportationOptionsRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateTransportationOptionsRequest.to_json())

# convert the object into a dict
generate_transportation_options_request_dict = generate_transportation_options_request_instance.to_dict()
# create an instance of GenerateTransportationOptionsRequest from a dict
generate_transportation_options_request_from_dict = GenerateTransportationOptionsRequest.from_dict(generate_transportation_options_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


