# GenerateCollectionFormRequest

The request schema Call to generate the collection form.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | 
**ship_from_address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.generate_collection_form_request import GenerateCollectionFormRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateCollectionFormRequest from a JSON string
generate_collection_form_request_instance = GenerateCollectionFormRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateCollectionFormRequest.to_json())

# convert the object into a dict
generate_collection_form_request_dict = generate_collection_form_request_instance.to_dict()
# create an instance of GenerateCollectionFormRequest from a dict
generate_collection_form_request_from_dict = GenerateCollectionFormRequest.from_dict(generate_collection_form_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


