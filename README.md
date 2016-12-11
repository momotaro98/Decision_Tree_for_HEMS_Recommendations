# Decision_Tree_for_HEMS_Recommendations

This is repo for momotaro98's master degree research.

## Usage

```
pip install decision_tree_for_hems_recommendations
```


### Preparing

`start_train_dt`
`end_train_dt`
**`ac_logs_list`**
`target_season`
`target_hour`

#### `ac_logs_list`
`ac_logs_list`


### Getting IsDeliverContent Flag

```
from decision_tree_for_hems_recommendations import (
	SettingTempDT,
	TotalUsageDT,
	ChangeUsageDT,
)


settemp_DT = SettingTempDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
is_deliver_settemp_content = settemp_DT.ret_predicted_Y_int()

totalusage_DT = TotalUsageDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
is_deliver_totalusage_content = totalusage_DT.ret_predicted_Y_int()

changeusage_DT = ChangeUsageDT(
	start_train_dt=start_train_dt,
	end_train_dt=end_train_dt,
	ac_logs_list=ac_logs_list,
	target_season=target_season,
	target_hour=target_hour,
)
is_deliver_changeusage_content = changeusage_DT.ret_predicted_Y_int()
```
