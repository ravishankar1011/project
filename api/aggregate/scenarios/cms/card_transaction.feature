Feature: CMS service's Card Transactions Scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John       | Snow      | SG     | john@snow.com | +63 1234567890 |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status |
      | CPid1                       | ECPid1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE |

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group              |
      | Pid1       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_params_group |

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description            |
      | TXN1             | ISO1     | First transaction code |
      | TXN2             | ISO2     | Second one             |
      | TXN3             | ISO3     | Third transaction code |
      | TXN4             | ISO4     | Fourth one             |
      | CARD-TXN         | ISO5     | Card Txn one           |

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name               | bucket_code | txn_codes            | interest_type      | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket  | STD_001     | TXN1, TXN2           | STANDARD_INTEREST  | 1                  | 50.0             | 10.5 |
      | Immediate Interest Bucket | IMD_002     | TXN3, TXN4, CARD-TXN | IMMEDIATE_INTEREST | 2                  | 70.0             | 12.0 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

    Then I onboard End Customer Profile ECPid1 to CMS and verify onboard status as ONBOARD_SUCCESS and status code as 200

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 10000          |

    Then I attach card to below credit accounts
      | account_id | status  |
      | CAid1      | SUCCESS |

  Scenario: Auth -> Clear Same Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid11          | CAid1      | REQUEST      | SGD      | 45.86  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid11          | ClearingGrp1      | 45.86  | 200         | TRANSACTION_SETTLED |

  Scenario: Auth -> Clear Partial Amount -> Clear Remaining Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid21          | CAid1      | REQUEST      | SGD      | 50     | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      # here status is for original transaction when partially cleared
      | transaction_id | clearing_group_id | amount | status_code | status                     |
      | Tid21          | ClearingGrp1      | 30     | 200         | TRANSACTION_AMOUNT_BLOCKED |
      | Tid21          | ClearingGrp1      | 20     | 200         | TRANSACTION_SETTLED        |

  Scenario: Auth -> Clear Higher Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid31          | CAid1      | REQUEST      | SGD      | 259.48 | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status                     |
      | Tid31          | ClearingGrp1      | 262.07 | 200         | TRANSACTION_AMOUNT_BLOCKED |
      | Tid31          | ClearingGrp1      | 262.07 | 200         | TRANSACTION_SETTLED        |

  Scenario: Auth Txn rejected for Insufficient credit limit

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                             | metadata         | transaction_code |
      | Tid42          | CAid1      | REQUEST      | SGD      | 12000  | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | {"Category":"1"} | CARD-TXN         |

  Scenario: Auth Txn rejected (Bucket Limit Breached)

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                             | metadata         | transaction_code |
      | Tid42          | CAid1      | REQUEST      | SGD      | 7001   | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | {"Category":"1"} | CARD-TXN         |

  Scenario: Auth -> Update to Same Amount -> Clear Same Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid11          | CAid1      | REQUEST      | SGD      | 45.37  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                     | metadata         | transaction_code |
      | Tid11          | CAid1      | REQUEST      | 45.37  | 200         | TRANSACTION_AMOUNT_BLOCKED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid11          | ClearingGrp1      | 45.37  | 200         | TRANSACTION_SETTLED |

  Scenario: Auth -> Update to Lower Amount -> Clear Updated Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid21          | CAid1      | REQUEST      | SGD      | 153.24 | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                     | metadata         | transaction_code |
      | Tid21          | CAid1      | REQUEST      | 124.56 | 200         | TRANSACTION_AMOUNT_BLOCKED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid21          | ClearingGrp1      | 124.56 | 200         | TRANSACTION_SETTLED |

  Scenario: Auth -> Update to Higher Amount -> Clear Updated Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid31          | CAid1      | REQUEST      | SGD      | 78.58  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                     | metadata         | transaction_code |
      | Tid31          | CAid1      | REQUEST      | 85.4   | 200         | TRANSACTION_AMOUNT_BLOCKED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid31          | ClearingGrp1      | 85.4   | 200         | TRANSACTION_SETTLED |

  Scenario: Auth -> Update Txn rejected for Insufficient credit limit

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid41          | CAid1      | REQUEST      | SGD      | 62.34  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                             | metadata         |
      | Tid41          | CAid1      | REQUEST      | 11000  | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | {"Category":"2"} |

  Scenario: Auth -> Update Txn rejected (Bucket Limit Breached)

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid41          | CAid1      | REQUEST      | SGD      | 1006   | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                             | metadata         | transaction_code |
      | Tid41          | CAid1      | REQUEST      | 7001   | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | {"Category":"2"} | CARD-TXN         |

  Scenario: CA_DEBIT_TXN -> Auth Advice (insufficient credit) -> Clear Same Amount

    Given I fetch and set approved limit for the below credit account
      | credit_account_id |
      | CAid1             |

    Then I create below transaction and verify the transaction status as TRANSACTION_SETTLED and status code as 200
      | credit_account_id | amount | currency | txn_code | receiver              |
      | CAid1             | 5000   | SGD      | TXN1     | create_receiver_group |
      | CAid1             | 4000   | SGD      | TXN4     | create_receiver_group |

    Then I verify the credit account balance after the transaction and status code as 200
      | credit_account_id |
      | CAid1             |

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid12          | CAid1      | ADVICE       | SGD      | 2000   | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid12          | ClearingGrp1      | 11000  | 200         | TRANSACTION_SETTLED |

  Scenario: CA_DEBIT_TXN -> Auth Advice (insufficient credit) -> Update Advice (higher amount) -> Clear Updated Amount

    Given I fetch and set approved limit for the below credit account
      | credit_account_id |
      | CAid1             |

    Then I create below transaction and verify the transaction status as TRANSACTION_SETTLED and status code as 200
      | credit_account_id | amount | currency | txn_code | receiver              |
      | CAid1             | 5000   | SGD      | TXN1     | create_receiver_group |
      | CAid1             | 4000   | SGD      | TXN4     | create_receiver_group |

    Then I verify the credit account balance after the transaction and status code as 200
      | credit_account_id |
      | CAid1             |

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid21          | CAid1      | ADVICE       | SGD      | 2000   | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                     | metadata         | transaction_code |
      | Tid21          | CAid1      | ADVICE       | 2010   | 200         | TRANSACTION_AMOUNT_BLOCKED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid21          | ClearingGrp1      | 2010   | 200         | TRANSACTION_SETTLED |

  Scenario: CA_DEBIT_TXN -> Auth Advice (insufficient credit) -> Update No Advice (lower amount) -> Clear updated amount

    Given I fetch and set approved limit for the below credit account
      | credit_account_id |
      | CAid1             |

    Then I create below transaction and verify the transaction status as TRANSACTION_SETTLED and status code as 200
      | credit_account_id | amount | currency | txn_code | receiver              |
      | CAid1             | 5000   | SGD      | TXN1     | create_receiver_group |
      | CAid1             | 4000   | SGD      | TXN4     | create_receiver_group |

    Then I verify the credit account balance after the transaction and status code as 200
      | credit_account_id |
      | CAid1             |

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid41          | CAid1      | ADVICE       | SGD      | 2000   | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                     | metadata         | transaction_code |
      | Tid41          | CAid1      | REQUEST      | 1000   | 200         | TRANSACTION_AMOUNT_BLOCKED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid41          | ClearingGrp1      | 1000   | 200         | TRANSACTION_SETTLED |

  Scenario: CA_DEBIT_TXN -> Auth Advice (insufficient credit) -> Update No Advice (higher amount, update should fail) -> Clear original amount

    Given I fetch and set approved limit for the below credit account
      | credit_account_id |
      | CAid1             |

    Then I create below transaction and verify the transaction status as TRANSACTION_SETTLED and status code as 200
      | credit_account_id | amount | currency | txn_code | receiver              |
      | CAid1             | 5000   | SGD      | TXN1     | create_receiver_group |
      | CAid1             | 4000   | SGD      | TXN4     | create_receiver_group |

    Then I verify the credit account balance after the transaction and status code as 200
      | credit_account_id |
      | CAid1             |

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid51          | CAid1      | ADVICE       | SGD      | 2000   | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I update below auth transactions and verify balances
      | transaction_id | account_id | message_type | amount | status_code | status                             | metadata         | transaction_code |
      | Tid51          | CAid1      | REQUEST      | 2010   | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid51          | ClearingGrp1      | 2000   | 200         | TRANSACTION_SETTLED |

  Scenario: Auth -> Revert

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid51          | CAid1      | REQUEST      | SGD      | 30.56  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I revert the following transactions
      | transaction_id | status_code | status               | refund |
      | Tid51          | 200         | TRANSACTION_REVERTED | False  |

  Scenario: Auth -> Clear -> Revert (should fail)

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid61          | CAid1      | REQUEST      | SGD      | 15.23  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid61          | ClearingGrp1      | 15.23  | 200         | TRANSACTION_SETTLED |

    Then I revert the following transactions
      | transaction_id | status_code | status                             | refund |
      | Tid61          | 200         | AUTHORIZATION_DECLINED_BAD_REQUEST | False  |

  Scenario: Auth -> Multiple Clear -> Initiate Debit Settlement Same Cumulative Amount

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid71          | CAid1      | REQUEST      | SGD      | 15.23  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |
      | Tid72          | CAid1      | REQUEST      | SGD      | 20.27  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid71          | ClearingGrp3      | 15.23  | 200         | TRANSACTION_SETTLED |
      | Tid72          | ClearingGrp3      | 20.27  | 200         | TRANSACTION_SETTLED |

    Then I initiate Debit Settlement and verify collection balance
      | clearing_group_id | cumulative_amount | external_ref | settlement_account_detail       | status_code | status              |
      | ClearingGrp3      | 35.5              | ref          | debit_settlement_account_detail | 200         | SETTLEMENT_APPROVED |

  Scenario: Auth -> Multiple Clear -> Initiate Debit Settlement Different Cumulative Amount (Should Fail)

    Then I create below auth transactions and verify balances
      | transaction_id | account_id | message_type | currency | amount | status_code | status                 | metadata         | transaction_code |
      | Tid71          | CAid1      | REQUEST      | SGD      | 15.23  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |
      | Tid72          | CAid1      | REQUEST      | SGD      | 20.27  | 200         | AUTHORIZATION_APPROVED | {"Category":"2"} | CARD-TXN         |

    Then I clear below transactions
      | transaction_id | clearing_group_id | amount | status_code | status              |
      | Tid71          | ClearingGrp3      | 15.23  | 200         | TRANSACTION_SETTLED |
      | Tid72          | ClearingGrp3      | 20.27  | 200         | TRANSACTION_SETTLED |

    Then I initiate Debit Settlement and verify collection balance
      | clearing_group_id | cumulative_amount | external_ref | settlement_account_detail       | status_code | status                          |
      | ClearingGrp3      | 30                | ref          | debit_settlement_account_detail | 200         | SETTLEMENT_DECLINED_BAD_REQUEST |

  Scenario: Detach Card Again (Already Detached) -> (Should Fail)

    Then I detach card to below credit accounts
      | account_id | status   | status_code |
      | CAid1      | DETACHED | 200         |

    Then I detach card to below credit accounts
      | account_id | status                            | status_code |
      | CAid1      | DETACH_REJECTED_ACCOUNT_NOT_FOUND | 200         |

  Scenario: Attach Card Again (Already Attached) -> (Should Pass)

    Then I attach card to below credit accounts
      | account_id | status  |
      | CAid1      | SUCCESS |

  Scenario: Detach Card -> (Success) -> Attach Card Again -> (Should Pass)

    Then I detach card to below credit accounts
      | account_id | status   | status_code |
      | CAid1      | DETACHED | 200         |

    Then I attach card to below credit accounts
      | account_id | status  |
      | CAid1      | SUCCESS |
