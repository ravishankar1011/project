Feature: Confirmation of Deposits by Cash Service

  Background: Setup customerProfile and EndCustomerProfile and add Accounts.

     #CustomerProfile verifying and Onboarding on to Cash service on given providers
    Given I set and verify customer CId1, customer profile CPId1 on cash service on below providers and expect status 200 in the context
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email   | phone_number |
      | CId1                | CPId1                       | ECPId1                          | Cash       | service   | SG     | x@y.com | 00000000     |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | customer_profile_id   | first_name | last_name | email   | phone_number | status |
      | CPId1                       | ECPId1                          | <customer_profile_id> | Cash       | service   | x@y.com | 00000000     | ACTIVE |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    # EndCustomerProfile Onboarding
    Given I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPId1 of CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    # Cash Wallet Product with Deposit Mode set to Notify instead of the default Accept
    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy | deposit_mode |
      | ProductID1 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | STRICT                 | NOTIFY       |

    Then I approve the product ProductID1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID1 with bank account type as PPA with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata                            |
      | CashWalletId1 | IntegrationTest1    | IntegrationEndCustomer  | SGD      | SGP     | false    | false                | CUSTOMER     | {"keyref":"M030126179534319754275"} |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

  Scenario: I deposit an amount of 100 into End Customer Wallet and later accept the deposit

    Given I deposit an amount of 100 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail | amount |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             | 100    |

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 0 and total balance of 100 for customerProfileId CPId1

    Then I get the deposit transaction TxId1 details for cash wallet CashWalletId1 for customerProfileId CPId1

    Then I confirm the deposit transaction TxId1 for customerProfileId CPId1 and expect the header status as 200 transaction status as TRANSACTION_PENDING
      | accept |
      | true   |

    Then I wait until max time to verify the transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I verify for bank account CashWalletId1 total balance is 100 and available balance is 100 for customerProfileId CPId1


  Scenario: I deposit an amount of 100 into End Customer Wallet and later reject the deposit

    Given I deposit an amount of 100 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail | amount |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             | 100    |

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 0 and total balance of 100 for customerProfileId CPId1

    Then I get the deposit transaction TxId1 details for cash wallet CashWalletId1 for customerProfileId CPId1

    Then I confirm the deposit transaction TxId1 for customerProfileId CPId1 and expect the header status as 200 transaction status as TRANSACTION_PENDING
      | accept |
      | false  |

    Then I wait until max time to verify the transaction TxId1 status as TRANSACTION_REJECTED for customerProfileId CPId1

    Then I verify for bank account CashWalletId1 total balance is 0 and available balance is 0 for customerProfileId CPId1


  Scenario: I transfer an amount of 100 from CashWalletId2 to CashWalletId1 with partial overdraft and accept the multi deposit on CashWalletId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID  | CASH_WALLET  | CUSTOMER     | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | STRICT                 |

    Then I approve the product ProductID and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for CustomerProfile with id CPId1 with product id as ProductID with bank account type as Payments Account with provider DBS Bank Ltd and expect the header status 200
      | identifier         | customer_profile_id | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata              | kyc_completed | trust_verification_completed |
      | CustomerCashWallet | IntegrationTest1    | SGD      | SGP     | false    | false                | CUSTOMER     | {"key": "MyMetaData"} | false         | false                        |

    Then I wait until max time to verify the bank account CustomerCashWallet status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 1000 into CustomerCashWallet using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CustomerCashWallet with an increased balance of 1000 for customerProfileId CPId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as PPA with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata                            |
      | CashWalletId2 | IntegrationTest1    | IntegrationEndCustomer  | SGD      | SGP     | false    | false                | CUSTOMER     | {"keyref":"M030126179534319754275"} |

    Then I wait until max time to verify the bank account CashWalletId2 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 50 into CashWalletId2 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail | amount |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             | 100    |

    Then I wait until max time to verify bank account CashWalletId2 with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I initiate transaction to transfer funds with below details and expect the header statuscode 200 and transaction status as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_wallet_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashWalletId2  | 100    | Integration Test | true                 | {"key": "MyMetaData"} | SGD      | CARD_TXN     | CashWalletId1       |

    Then I verify for bank account CashWalletId2 total balance is 50 and available balance is -50 for customerProfileId CPId1

    Then I settle transaction to transfer funds with below details and expect the header statuscode 200 and transaction_status as TRANSACTION_SETTLED
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              | overdraft_funding_cash_wallet_id |
      | TxId1          | CPId1               | 100    | FAST             | true                 | {"key": "MyMetaData"} | CustomerCashWallet               |

    Then I wait until max time to verify the transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I verify for bank account CashWalletId2 total balance is -50 and available balance is -50 for customerProfileId CPId1

    Then I get the deposit transaction TxId2 details for cash wallet CashWalletId1 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 0 and total balance of 100 for customerProfileId CPId1

    Then I confirm the deposit transaction TxId2 for customerProfileId CPId1 and expect the header status as 200 transaction status as TRANSACTION_PENDING
      | accept |
      | true   |

    Then I wait until max time to verify the transaction TxId2 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I verify for bank account CashWalletId1 total balance is 100 and available balance is 100 for customerProfileId CPId1


  Scenario: I transfer an amount of 100 from CashWalletId2 to CashWalletId1 with partial overdraft and reject the multi deposit on CashWalletId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID  | CASH_WALLET  | CUSTOMER     | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | STRICT                 |

    Then I approve the product ProductID and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for CustomerProfile with id CPId1 with product id as ProductID with bank account type as Payments Account with provider DBS Bank Ltd and expect the header status 200
      | identifier         | customer_profile_id | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata              | kyc_completed | trust_verification_completed |
      | CustomerCashWallet | IntegrationTest1    | SGD      | SGP     | false    | false                | CUSTOMER     | {"key": "MyMetaData"} | false         | false                        |

    Then I wait until max time to verify the bank account CustomerCashWallet status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 1000 into CustomerCashWallet using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CustomerCashWallet with an increased balance of 1000 for customerProfileId CPId1

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as PPA with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id | currency | country | in_trust | is_overdraft_allowed | on_behalf_of | metadata                            |
      | CashWalletId2 | IntegrationTest1    | IntegrationEndCustomer  | SGD      | SGP     | false    | false                | CUSTOMER     | {"keyref":"M030126179534319754275"} |

    Then I wait until max time to verify the bank account CashWalletId2 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 50 into CashWalletId2 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail | amount |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             | 100    |

    Then I wait until max time to verify bank account CashWalletId2 with an available balance of 50 and total balance of 50 for customerProfileId CPId1

    Then I initiate transaction to transfer funds with below details and expect the header statuscode 200 and transaction status as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_wallet_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashWalletId2  | 100    | Integration Test | true                 | {"key": "MyMetaData"} | SGD      | CARD_TXN     | CashWalletId1       |

    Then I verify for bank account CashWalletId2 total balance is 50 and available balance is -50 for customerProfileId CPId1

    Then I settle transaction to transfer funds with below details and expect the header statuscode 200 and transaction_status as TRANSACTION_SETTLED
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              | overdraft_funding_cash_wallet_id |
      | TxId1          | CPId1               | 100    | FAST             | true                 | {"key": "MyMetaData"} | CustomerCashWallet               |

    Then I wait until max time to verify the transaction TxId1 status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I verify for bank account CashWalletId2 total balance is -50 and available balance is -50 for customerProfileId CPId1

    Then I get the deposit transaction TxId2 details for cash wallet CashWalletId1 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 0 and total balance of 100 for customerProfileId CPId1

    Then I confirm the deposit transaction TxId2 for customerProfileId CPId1 and expect the header status as CSSM_9659 transaction status as Cannot Reject transaction
      | accept |
      | false  |
