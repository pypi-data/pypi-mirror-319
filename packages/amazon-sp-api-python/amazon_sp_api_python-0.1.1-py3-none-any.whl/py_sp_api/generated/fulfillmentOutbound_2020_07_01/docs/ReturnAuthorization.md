# ReturnAuthorization

Return authorization information for items accepted for return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_authorization_id** | **str** | An identifier for the return authorization. This identifier associates return items with the return authorization used to return them. | 
**fulfillment_center_id** | **str** | An identifier for the Amazon fulfillment center that the return items should be sent to. | 
**return_to_address** | [**Address**](Address.md) |  | 
**amazon_rma_id** | **str** | The return merchandise authorization (RMA) that Amazon needs to process the return. | 
**rma_page_url** | **str** | A URL for a web page that contains the return authorization barcode and the mailing label. This does not include pre-paid shipping. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.return_authorization import ReturnAuthorization

# TODO update the JSON string below
json = "{}"
# create an instance of ReturnAuthorization from a JSON string
return_authorization_instance = ReturnAuthorization.from_json(json)
# print the JSON string representation of the object
print(ReturnAuthorization.to_json())

# convert the object into a dict
return_authorization_dict = return_authorization_instance.to_dict()
# create an instance of ReturnAuthorization from a dict
return_authorization_from_dict = ReturnAuthorization.from_dict(return_authorization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


