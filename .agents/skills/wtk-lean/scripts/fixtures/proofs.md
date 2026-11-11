# billing proofs

**HEAD**: e4f5a6b
**Shell**: /bin/sh
**Result**: 11 pass, 0 fail

| Proof | Result | Line |
| --- | --- | --- |
| C1: run billing / test_failed_charge_suspends = . | pass | BillingDunningTest#test_failed_charge_suspends = 0.02 s = . |
| C2: run billing / test_every_provider_status_maps_once = . | pass | BillingStatusMapTest#test_every_provider_status_maps_once = 0.01 s = . |
| C3: run billing / test_unknown_status_is_recorded = . | pass | BillingStatusMapTest#test_unknown_status_is_recorded = 0.01 s = . |
| C4: bin/rails test test/billing/access_test.rb -n "/suspended_denies_paid_groups/" | pass | exit 0 |
| C5: bin/rails test test/billing/transitions_test.rb -n "/suspended_to_trialing_is_rejected/" | pass | exit 0 |
| C6: bin/rails test test/billing/transitions_test.rb -n "/suspended_to_active/" | pass | exit 0 |
| C7: bin/rails test test/webhooks/ingest_test.rb -n "/concurrent_delivery_conflicts/" | pass | exit 0 |
| C8: bin/rails test test/webhooks/ingest_test.rb -n "/retry_is_idempotent/" | pass | exit 0 |
| C9: bin/rails test test/webhooks/ingest_test.rb -n "/missing_subscription_id_is_422/" | pass | exit 0 |
| C10: bin/rails test test/webhooks/dispatch_test.rb -n "/dispatches_every_event_type/" | pass | exit 0 |
| C11: run billing / test_provider_timeout_is_inert = . | pass | BillingDunningTest#test_provider_timeout_is_inert = 0.01 s = . |

## Output

`Run billing` - exit 0

```
BillingDunningTest#test_failed_charge_suspends = 0.02 s = .
BillingDunningTest#test_provider_timeout_is_inert = 0.01 s = .
BillingStatusMapTest#test_every_provider_status_maps_once = 0.01 s = .
BillingStatusMapTest#test_unknown_status_is_recorded = 0.01 s = .

4 runs, 13 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/billing/access_test.rb -n "/suspended_denies_paid_groups/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/billing/transitions_test.rb -n "/suspended_to_trialing_is_rejected/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/billing/transitions_test.rb -n "/suspended_to_active/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/webhooks/ingest_test.rb -n "/concurrent_delivery_conflicts/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/webhooks/ingest_test.rb -n "/retry_is_idempotent/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/webhooks/ingest_test.rb -n "/missing_subscription_id_is_422/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```

`bin/rails test test/webhooks/dispatch_test.rb -n "/dispatches_every_event_type/"` - exit 0

```
1 runs, 2 assertions, 0 failures, 0 errors, 0 skips
```
