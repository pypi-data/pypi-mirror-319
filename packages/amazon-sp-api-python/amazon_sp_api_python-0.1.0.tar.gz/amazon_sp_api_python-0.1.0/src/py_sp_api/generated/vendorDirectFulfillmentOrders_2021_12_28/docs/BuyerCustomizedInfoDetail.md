# BuyerCustomizedInfoDetail

The details of the products the vendor has configured as customizable.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customized_url** | **str** | A [Base 64](https://datatracker.ietf.org/doc/html/rfc4648#section-4) encoded URL using the UTF-8 character set. The URL provides the location of the zip file that specifies the types of customizations or configurations allowed by the vendor, along with types and ranges for the attributes of their products. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.buyer_customized_info_detail import BuyerCustomizedInfoDetail

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerCustomizedInfoDetail from a JSON string
buyer_customized_info_detail_instance = BuyerCustomizedInfoDetail.from_json(json)
# print the JSON string representation of the object
print(BuyerCustomizedInfoDetail.to_json())

# convert the object into a dict
buyer_customized_info_detail_dict = buyer_customized_info_detail_instance.to_dict()
# create an instance of BuyerCustomizedInfoDetail from a dict
buyer_customized_info_detail_from_dict = BuyerCustomizedInfoDetail.from_dict(buyer_customized_info_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


