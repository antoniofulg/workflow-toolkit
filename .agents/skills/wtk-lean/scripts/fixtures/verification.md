# Dunning on failed charge - verification

**Verdict**: PASS
**Profile**: standard
**Diff range**: a1b2c3d..e4f5g6h
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)
**Quarantined tests**: none

## Checks

| Check | Test | Holds | Evidence |
| --- | --- | --- | --- |
| C1 | `test/billing/dunning_test.rb` `failed_charge_suspends` | yes | `test/billing/dunning_test.rb:118` - `assert_equal "suspended", sub.status` |
| C2 | `test/billing/status_map_test.rb` `every_provider_status_maps_once` | yes | `test/billing/status_map_test.rb:30` - `assert_equal expected, StatusMap.call(status) for all 9` |
| C3 | `test/billing/status_map_test.rb` `unknown_status_is_recorded` | yes | `test/billing/status_map_test.rb:52` - `assert_event "billing.status_unmapped"` |
| C4 | `test/billing/access_test.rb` `suspended_denies_paid_groups` | yes | `test/billing/access_test.rb:40` - `refute policy.grant?(:paid)` |
| C5 | `test/billing/transitions_test.rb` `suspended_to_trialing_is_rejected` | yes | `test/billing/transitions_test.rb:22` - `assert_raises(InvalidTransition)` |
| C6 | `test/billing/transitions_test.rb` `suspended_to_active` | yes | `test/billing/transitions_test.rb:35` - `assert_equal "active", sub.status` |
| C7 | `test/webhooks/ingest_test.rb` `concurrent_delivery_conflicts` | yes | `test/webhooks/ingest_test.rb:91` - `assert_response 409` |
| C8 | `test/webhooks/ingest_test.rb` `retry_is_idempotent` | yes | `test/webhooks/ingest_test.rb:64` - `assert_equal 1, WebhookDelivery.count` |
| C9 | `test/webhooks/ingest_test.rb` `missing_subscription_id_is_422` | yes | `test/webhooks/ingest_test.rb:77` - `assert_response 422` |
| C10 | `test/webhooks/dispatch_test.rb` `dispatches_every_event_type` | yes | `test/webhooks/dispatch_test.rb:18` - `each of the 5 event types hits its handler` |
| C11 | `test/billing/dunning_test.rb` `provider_timeout_is_inert` | yes | `test/billing/dunning_test.rb:140` - `assert_equal before, sub.reload.status` |

## Coverage

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| provider status -> local (9) | provider webhook reference | C2, table-driven over all 9 | - |
| webhook event types (5) | provider webhook reference | `charge_failed` C1 · `charge_succeeded` C6 · `updated` C10 · `deleted` C10 · `trial_will_end` C10 | - |

## Test policy rows

| Row | Files it classifies | Required proof | Expectation met |
| --- | --- | --- | --- |
| Decides, reached across a boundary | `app/webhooks/ingest.rb` | boundary C9 · own layer C10 | yes |
| Decides, not reached across a boundary | `app/models/billing/status_map.rb` | own layer C2 | yes |
| Instrumentation, pass-throughs | `app/webhooks/payload.rb` | none of its own | yes |

## Faults injected

| Check | Mutation | Location | Disposition |
| --- | --- | --- | --- |
| C1 | returned status `suspended` -> `cancelled` | `app/models/billing/subscription.rb:88` | killed |
| C7 | removed the `409` on a concurrent delivery | `app/webhooks/ingest.rb:44` | killed |
| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | killed |
| C11 | bound `>= 3` -> `> 3` on retry count | `app/models/billing/dunning.rb:22` | killed |
| C11 | log level `info` -> `debug` on the retry trace | `app/models/billing/dunning.rb:40` | arid - logging only, no decision reads it |

## Gate

`bin/rails test` - 138 passed, 0 failed
