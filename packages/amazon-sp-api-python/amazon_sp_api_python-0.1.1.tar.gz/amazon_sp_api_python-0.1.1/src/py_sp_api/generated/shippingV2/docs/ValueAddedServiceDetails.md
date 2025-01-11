# ValueAddedServiceDetails

A collection of supported value-added services.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collect_on_delivery** | [**CollectOnDelivery**](CollectOnDelivery.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.value_added_service_details import ValueAddedServiceDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ValueAddedServiceDetails from a JSON string
value_added_service_details_instance = ValueAddedServiceDetails.from_json(json)
# print the JSON string representation of the object
print(ValueAddedServiceDetails.to_json())

# convert the object into a dict
value_added_service_details_dict = value_added_service_details_instance.to_dict()
# create an instance of ValueAddedServiceDetails from a dict
value_added_service_details_from_dict = ValueAddedServiceDetails.from_dict(value_added_service_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


