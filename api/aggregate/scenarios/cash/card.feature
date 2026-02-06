Feature: Card Service requests to Cash Service scenarios

  Background: Customer-Profile
    Given I set and verify customer CId1, customer profile CPId1 in the context

    Given I set and verify customer CId1, customer profile CPId1 on cash service on below providers and expect status 200 in the context
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Given I initialise card for Customer Profile CPId1 and expect request status code as 200 and status as SUCCESS

    Then I setup card float account FloatAccID for Customer Profile CPId1 and expect request status code as 200 and status as SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name  | last_name | region | email   | phone_number |
      | CId1                | CPId1                       | ECPId1                          | Integration | Test      | SG     | x@y.com | 123456       |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | customer_profile_id | first_name  | last_name | email   | phone_number | status |
      | CPId1                       | ECPId1                          | CPId1               | Integration | Test      | x@y.com | 123456       | ACTIVE |

    Given I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPId1 of CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Then I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on card service and expect request status as 200 and onboard_status as ONBOARD_SUCCESS

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier       | product_type | profile_type | product_class | max_active_cash_wallets |
      | CashAccProductId | CASH_ACCOUNT | END_CUSTOMER | STANDARD      | 1                       |

    Then I approve the product CashAccProductId and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier          | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | CashWalletProductId | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product CashWalletProductId and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Then I create a end customer cash account with id CashAccId customerProfileID CPId1 with product id CashAccProductId and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id CashWalletProductId with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier   | customer_profile_id | end_customer_profile_id          | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId | CPId1               | 36974646-3489-47aa-b6c2-w232d543 | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId       |

    Then I wait until max time to verify the bank account CashWalletId status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

#    Card - Pay Transaction

  Scenario: Perform an Pay transaction on cash wallet with amount < balance and overdraft not required

    Given I deposit an amount of 1000 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 1000 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Card Pay Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status PAY_PENDING
      | currency | purpose          | amount | push_overdraft |
      | SGD      | Integration Test | 100    | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 900 and total balance of 900 for customerProfileId CPId1

  Scenario: Perform an Pay transaction on cash wallet with amount > balance and overdraft allowed

    Given I deposit an amount of 50 into cash account FloatAccID and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify cash account FloatAccID with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Given I deposit an amount of 100 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 100 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Card Pay Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status PAY_PENDING
      | currency | purpose          | amount | push_overdraft |
      | SGD      | Integration Test | 150    | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of -50 and total balance of -50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 0 and total balance of 0 for customerProfileId CPId1

  Scenario: Perform an Card Pay transaction on cash wallet with amount > balance and overdraft not allowed so expect no funds exception

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Card Pay Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status PAY_DECLINED_INSUFFICIENT_BALANCE
      | currency | purpose          | amount | push_overdraft |
      | SGD      | Integration Test | 100    | false          |

  Scenario: Perform an Card Pay transaction on an invalid Cash Wallet Id i.e. a cash wallet which is not attached onto a card and expect error

    Then I initiate a Card Pay Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status PAY_DECLINED_BAD_REQUEST
      | currency | amount | push_overdraft | purpose          |
      | SGD      | 100    | true           | Integration Test |

#    Card - Apply Fee Transaction

  Scenario: Perform an Apply Fee transaction on an invalid Cash Wallet Id i.e. a cash wallet which is not attached onto a card and expect error

    Then I initiate a Card Pay Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status PAY_DECLINED_BAD_REQUEST
      | currency | purpose          | amount | push_overdraft |
      | SGD      | Integration Test | 100    | true           |

  Scenario: Perform an Apply Fees transaction on cash wallet with amount = balance and overdraft not required

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Fee on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_FEE_PENDING
      | currency | amount | push_overdraft |
      | SGD      | 50     | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 0 and total balance of 0 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 50 and total balance of 50 for customerProfileId CPId1

  Scenario: Perform an Apply Fees transaction on cash wallet with amount > balance and overdraft allowed

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Fee on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_FEE_PENDING
      | currency | amount | push_overdraft |
      | SGD      | 100    | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of -50 and total balance of -50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 100 and total balance of 100 for customerProfileId CPId1

  Scenario: Perform an Apply Fees transaction on cash wallet with amount > balance and overdraft not allowed so expect no funds exception

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Fee on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_FEE_DECLINED_INSUFFICIENT_BALANCE
      | currency | amount | push_overdraft |
      | SGD      | 100    | false          |

  Scenario: Perform an Apply Fee transaction on an invalid Cash Wallet Id i.e. a cash wallet which is not attached onto a card and expect error

    Then I initiate a Apply Fee on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_FEE_DECLINED_BAD_REQUEST
      | currency | amount | push_overdraft |
      | SGD      | 100    | true           |

#    Card - Apply Tax Transaction

  Scenario: Perform an Apply Tax transaction on cash wallet with amount < balance and overdraft not required

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Tax on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_TAX_PENDING
      | currency | amount | push_overdraft |
      | SGD      | 50     | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 0 and total balance of 0 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 150 and total balance of 150 for customerProfileId CPId1

  Scenario: Perform an Apply Tax transaction on cash wallet with amount > balance and overdraft allowed

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Tax on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_TAX_PENDING
      | currency | amount | push_overdraft |
      | SGD      | 100    | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of -50 and total balance of -50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 200 and total balance of 200 for customerProfileId CPId1

  Scenario: Perform an Apply Tax transaction on cash wallet with amount > balance and overdraft not allowed so expect no funds exception

    Given I deposit an amount of 50 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 50 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Tax on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_TAX_DECLINED_INSUFFICIENT_BALANCE
      | currency | amount | push_overdraft |
      | SGD      | 100    | false          |

  Scenario: Perform Apply Tax transaction on an invalid Cash Wallet Id i.e. a cash wallet which is not attached onto a card and expect error

    Then I initiate a Apply Tax on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_TAX_DECLINED_BAD_REQUEST
      | currency | amount | push_overdraft |
      | SGD      | 100    | true           |

#    Card - Apply Yield Transaction

  Scenario: Perform an Apply Yield transaction on cash wallet

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Apply Yield on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_YIELD_PENDING
      | currency | amount | push_overdraft |
      | SGD      | 50     | true           |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 150 and total balance of 150 for customerProfileId CPId1

  Scenario: Perform Apply Yield transaction on an invalid Cash Wallet Id i.e. a cash wallet which is not attached onto a card and expect error

    Then I initiate a Apply Yield on Card Transaction TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status APPLY_YIELD_DECLINED_BAD_REQUEST
      | currency | amount | push_overdraft |
      | SGD      | 100    | true           |

#    Card - Debit Auth Request

  Scenario: Initiate Debit Auth and the Clear it and then initiate unsolicited debit clearing and then initiate debit settlement on these two with same group id

    Given I deposit an amount of 200 into CashWalletId using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId with an increased balance of 200 for customerProfileId CPId1

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Debit Auth Request TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status AUTHORIZATION_APPROVED
      | currency | metadata                     | amount | message_type |
      | SGD      | {"key" : "Integration Test"} | 150    | REQUEST      |

    Then I wait until max time to verify bank account CashWalletId with an available balance of 50 and total balance of 200 for customerProfileId CPId1

    Then I initiate a Debit Clearing Request for below details CustomerProfileId CPId1 and expect request status 200 and txn status CLEARING_APPROVED
      | transaction_id | amount | clearing_group_id |
      | TxId1          | 150    | GroupId1          |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I initiate a Unsolicited Debit Clearing Request TxId2 for below details CustomerProfileId CPId1 and expect request status 200 and txn status CLEARING_APPROVED
      | account_id   | amount | clearing_group_id | currency | metadata                     |
      | CashWalletId | 100    | GroupId1          | SGD      | {"key" : "Integration Test"} |

    Then I wait until max time to verify the Card transaction TxId2 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of -50 and total balance of -50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 100 and total balance of 100 for customerProfileId CPId1

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier        | product_type | profile_type | product_class | max_active_cash_wallets |
      | CashAccProductId1 | CASH_ACCOUNT | CUSTOMER     | STANDARD      | 1                       |

    Then I approve the product CashAccProductId1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID1 | CASH_WALLET  | CUSTOMER     | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | STRICT                 |

    Then I approve the product ProductID1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Then I create a cash account with id CashAccId1 customerProfileId CPId1 with product id CashAccProductId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create account for CustomerProfile with id CPId1 with product id as ProductID1 with bank account type as Payments Account with provider DBS Bank Ltd and expect the header status 200
      | identifier           | customer_profile_id | currency | country | in_trust | on_behalf_of | metadata                   | kyc_completed | trust_verification_completed | cash_account_id |
      | SettlementCashWallet | CPId1               | SGD      | SGP     | false    | CUSTOMER     | {"type": "CardSettlement"} | false         | false                        | CashAccId1      |

    Then I wait until max time to verify the bank account SettlementCashWallet status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Then I initiate a Debit Settlement Request for below details CustomerProfileId CPId1 and expect request status 200 and settlement status SETTLEMENT_APPROVED
      | cumulative_amount | clearing_group_id | settlement_account_id |
      | 250               | GroupId1          | SettlementCashWallet  |

    Then I wait until max time to verify bank account SettlementCashWallet with an available balance of 250 and total balance of 250 for customerProfileId CPId1

#        Card - Credit Auth Request

  Scenario: Initiate Credit Auth and the Clear it and then initiate unsolicited credit clearing

    Then I attach a card onto the cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and attach status SUCCESS

    Then I initiate a Credit Auth Request TxId1 on cash wallet CashWalletId and CustomerProfileId CPId1 and expect request status 200 and txn status AUTHORIZATION_APPROVED
      | currency | metadata                     | amount | message_type |
      | SGD      | {"key" : "Integration Test"} | 30     | REQUEST      |

    Then I wait until max time to verify cash account FloatAccID with an available balance of 70 and total balance of 100 for customerProfileId CPId1

    Then I initiate a Credit Clearing Request for below details CustomerProfileId CPId1 and expect request status 200 and txn status CLEARING_APPROVED
      | transaction_id | amount | clearing_group_id |
      | TxId1          | 50     | GroupId1          |

    Then I wait until max time to verify the Card transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I initiate a Unsolicited Credit Clearing Request TxId2 for below details CustomerProfileId CPId1 and expect request status 200 and txn status CLEARING_APPROVED
      | account_id   | amount | clearing_group_id | currency | metadata                     |
      | CashWalletId | 50     | GroupId1          | SGD      | {"key" : "Integration Test"} |

    Then I wait until max time to verify the Card transaction TxId2 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 100 and total balance of 100 for customerProfileId CPId1

    Then I wait until max time to verify cash account FloatAccID with an available balance of 0 and total balance of 0 for customerProfileId CPId1
