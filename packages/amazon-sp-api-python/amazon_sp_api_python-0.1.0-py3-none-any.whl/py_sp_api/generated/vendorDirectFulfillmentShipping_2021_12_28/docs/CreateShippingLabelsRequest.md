# CreateShippingLabelsRequest

The request body for the createShippingLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**containers** | [**List[Container]**](Container.md) | A list of the packages in this shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.create_shipping_labels_request import CreateShippingLabelsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShippingLabelsRequest from a JSON string
create_shipping_labels_request_instance = CreateShippingLabelsRequest.from_json(json)
# print the JSON string representation of the object
print(CreateShippingLabelsRequest.to_json())

# convert the object into a dict
create_shipping_labels_request_dict = create_shipping_labels_request_instance.to_dict()
# create an instance of CreateShippingLabelsRequest from a dict
create_shipping_labels_request_from_dict = CreateShippingLabelsRequest.from_dict(create_shipping_labels_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


