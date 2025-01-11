# CreateReportSpecification


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_options** | **Dict[str, str]** | Additional information passed to reports. This varies by report type. | [optional] 
**report_type** | **str** | The report type. | 
**data_start_time** | **datetime** | The start of a date and time range, in ISO 8601 date time format, used for selecting the data to report. The default is now. The value must be prior to or equal to the current date and time. Not all report types make use of this. | [optional] 
**data_end_time** | **datetime** | The end of a date and time range, in ISO 8601 date time format, used for selecting the data to report. The default is now. The value must be prior to or equal to the current date and time. Not all report types make use of this. | [optional] 
**marketplace_ids** | **List[str]** | A list of marketplace identifiers. The report document&#39;s contents will contain data for all of the specified marketplaces, unless the report type indicates otherwise. | 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.create_report_specification import CreateReportSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of CreateReportSpecification from a JSON string
create_report_specification_instance = CreateReportSpecification.from_json(json)
# print the JSON string representation of the object
print(CreateReportSpecification.to_json())

# convert the object into a dict
create_report_specification_dict = create_report_specification_instance.to_dict()
# create an instance of CreateReportSpecification from a dict
create_report_specification_from_dict = CreateReportSpecification.from_dict(create_report_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


