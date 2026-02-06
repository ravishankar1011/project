Feature: Concurrent transactions of various cases of Cash Service

  Background: Setup customer and end-customer profile on Cash Service

    Given I set and verify customer CId1, customer profile CPId1 on cash service on below providers and expect status 200 in the context
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email   | phone_number |
      | CId1                | CPId1                       | ECPId1                          | Cash       | service   | SG     | x@y.com | 00000000     |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | customer_profile_id | first_name | last_name | email   | phone_number | status |
      | CPId1                       | ECPId1                          | CPId1               | Cash       | service   | x@y.com | 00000000     | ACTIVE |

    Given I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPId1 of CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier        | product_type | profile_type | product_class | max_active_cash_wallets |
      | CashAccProductId1 | CASH_ACCOUNT | CUSTOMER     | STANDARD      | 1                       |

    Then I approve the product CashAccProductId1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier        | product_type | profile_type | product_class | max_active_cash_wallets |
      | CashAccProductId2 | CASH_ACCOUNT | END_CUSTOMER | STANDARD      | 1                       |

    Then I approve the product CashAccProductId2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1


  Scenario: End Customer initiates 50 transactions and then settles all those 50 transactions with amount same as initial blocked amount.

    Then I create a end customer cash account with id CashAccId2 customerProfileID CPId1 with product id CashAccProductId2 and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id          | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId1 | CPId1               | 36974646-3489-47aa-b6c2-w232d543 | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId2      |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 1000 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an increased balance of 1000 for customerProfileId CPId1

    Then I initiate 50 multiple transactions to transfer funds with respective details and expect the header statuses as 200 and transaction statuses as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_account_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashAccId2      | 10     | Integration Test | false                | {"key": "MyMetaData"} | SGD      | CARD_TXN     |                     |

    Then I verify for bank account CashWalletId1 total balance is 1000 and available balance is 500 for customerProfileId CPId1

    Then I settle 50 multiple transactions to transfer funds with respective details and expect the header statuses 200 and transaction statuses as TRANSACTION_PENDING
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              |
      | TxId1          | CPId1               | 10     | FAST             | false                | {"key": "MyMetaData"} |

    Then I wait until max time to verify the group of transactions TxId1 statuses as TRANSACTION_SETTLED amount as 10 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 500 and total balance of 500 for customerProfileId CPId1


  Scenario: End Customer initiates 50 transactions and then settles all those 50 transactions with amount greater than initial blocked amount and less than his balance

    Then I create a end customer cash account with id CashAccId2 customerProfileID CPId1 with product id CashAccProductId2 and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id          | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId1 | CPId1               | 36974646-3489-47aa-b6c2-w232d543 | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId2      |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 1000 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an increased balance of 1000 for customerProfileId CPId1

    Then I initiate 50 multiple transactions to transfer funds with respective details and expect the header statuses as 200 and transaction statuses as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_account_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashAccId2      | 10     | Integration Test | false                | {"key": "MyMetaData"} | SGD      | CARD_TXN     |                     |

    Then I verify for bank account CashWalletId1 total balance is 1000 and available balance is 500 for customerProfileId CPId1

    Then I settle 50 multiple transactions to transfer funds with respective details and expect the header statuses 200 and transaction statuses as TRANSACTION_PENDING
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              |
      | TxId1          | CPId1               | 15     | FAST             | false                | {"key": "MyMetaData"} |

    Then I wait until max time to verify the group of transactions TxId1 statuses as TRANSACTION_SETTLED amount as 15 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 250 and total balance of 250 for customerProfileId CPId1


  Scenario: End Customer initiates 50 transactions and then settles all those 50 transactions with amount lesser than initial blocked amount

    Then I create a end customer cash account with id CashAccId2 customerProfileID CPId1 with product id CashAccProductId2 and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id          | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId1 | CPId1               | 36974646-3489-47aa-b6c2-w232d543 | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId2      |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 1000 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an increased balance of 1000 for customerProfileId CPId1

    Then I initiate 50 multiple transactions to transfer funds with respective details and expect the header statuses as 200 and transaction statuses as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_account_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashAccId2      | 15     | Integration Test | false                | {"key": "MyMetaData"} | SGD      | CARD_TXN     |                     |

    Then I verify for bank account CashWalletId1 total balance is 1000 and available balance is 250 for customerProfileId CPId1

    Then I settle 50 multiple transactions to transfer funds with respective details and expect the header statuses 200 and transaction statuses as TRANSACTION_PENDING
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              | new_transaction_id |
      | TxId1          | CPId1               | 10     | FAST             | false                | {"key": "MyMetaData"} | TxId2              |

    Then I wait until max time to verify the group of transactions TxId1 statuses as TRANSACTION_AMOUNT_BLOCKED amount as 5 for customerProfileId CPId1

    Then I wait until max time to verify the group of transactions TxId2 statuses as TRANSACTION_SETTLED amount as 10 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 250 and total balance of 500 for customerProfileId CPId1


  Scenario: End Customer initiates 50 transactions and then settles all those 50 transactions with amount less that balance and partial overdraft required and later deposits with lent recovery

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID1 | CASH_WALLET  | CUSTOMER     | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | STRICT                 |

    Then I approve the product ProductID1 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Then I create a cash account with id CashAccId1 customerProfileId CPId1 with product id CashAccProductId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create account for CustomerProfile with id CPId1 with product id as ProductID1 with bank account type as Payments Account with provider DBS Bank Ltd and expect the header status 200
      | identifier         | customer_profile_id | currency | country | in_trust | on_behalf_of | metadata              | kyc_completed | trust_verification_completed | cash_account_id |
      | CustomerProfileBA1 | IntegrationTest1    | SGD      | SGP     | false    | CUSTOMER     | {"key": "MyMetaData"} | false         | false                        | CashAccId1      |

    Then I wait until max time to verify the bank account CustomerProfileBA1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 500 into CustomerProfileBA1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CustomerProfileBA1 with an increased balance of 500 for customerProfileId CPId1

    Then I create a end customer cash account with id CashAccId2 customerProfileID CPId1 with product id CashAccProductId2 and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id          | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId1 | CPId1               | 36974646-3489-47aa-b6c2-w232d543 | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId2      |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Given I deposit an amount of 250 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an increased balance of 250 for customerProfileId CPId1

    Then I initiate 50 multiple transactions to transfer funds with respective details and expect the header statuses as 200 and transaction statuses as TRANSACTION_AMOUNT_BLOCKED
      | identifier | customer_profile_id | cash_account_id | amount | purpose          | is_overdraft_allowed | metadata              | currency | sub_txn_type | receiver_account_id |
      | TxId1      | CPId1               | CashAccId2      | 10     | Integration Test | true                 | {"key": "MyMetaData"} | SGD      | CARD_TXN     |                     |

    Then I verify for bank account CashWalletId1 total balance is 250 and available balance is -250 for customerProfileId CPId1

    Then I settle 50 multiple transactions to transfer funds with respective details and expect the header statuses 200 and transaction statuses as TRANSACTION_PENDING
      | transaction_id | customer_profile_id | amount | transaction_rail | is_overdraft_allowed | metadata              | overdraft_funding_cash_wallet_id |
      | TxId1          | CPId1               | 10     | FAST             | true                 | {"key": "MyMetaData"} | CustomerProfileBA1           |

    Then I wait until max time to verify the group of transactions TxId1 statuses as TRANSACTION_SETTLED amount as 10 for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of -250 and total balance of -250 for customerProfileId CPId1

    Given I deposit an amount of 100 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of -150 and total balance of -150 for customerProfileId CPId1

    Given I deposit an amount of 200 into CashWalletId1 using cash DevDeposit and expect the header status 200
      | identifier           | customer_profile_id | purpose  | currency | transaction_rail |
      | DevDepositIdentifier | CPId1               | TRANSFER | SGD      | FAST             |

    Then I wait until max time to verify bank account CashWalletId1 with an available balance of 50 and total balance of 50 for customerProfileId CPId1
