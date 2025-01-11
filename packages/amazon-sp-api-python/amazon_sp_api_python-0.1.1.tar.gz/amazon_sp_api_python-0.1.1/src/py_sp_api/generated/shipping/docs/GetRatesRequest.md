# GetRatesRequest

The payload schema for the getRates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_to** | [**Address**](Address.md) |  | 
**ship_from** | [**Address**](Address.md) |  | 
**service_types** | [**List[ServiceType]**](ServiceType.md) | A list of service types that can be used to send the shipment. | 
**ship_date** | **datetime** | The start date and time. This defaults to the current date and time. | [optional] 
**container_specifications** | [**List[ContainerSpecification]**](ContainerSpecification.md) | A list of container specifications. | 

## Example

```python
from py_sp_api.generated.shipping.models.get_rates_request import GetRatesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetRatesRequest from a JSON string
get_rates_request_instance = GetRatesRequest.from_json(json)
# print the JSON string representation of the object
print(GetRatesRequest.to_json())

# convert the object into a dict
get_rates_request_dict = get_rates_request_instance.to_dict()
# create an instance of GetRatesRequest from a dict
get_rates_request_from_dict = GetRatesRequest.from_dict(get_rates_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


