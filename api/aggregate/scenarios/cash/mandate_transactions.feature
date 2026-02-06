Feature: Cash Service Mandate Creation, Authorisation, Acceptation and Transactions.

  Background: Setup customer and end-customer profile on Cash Service

    Given I set and verify customer BCId1, customer profile CPId1 on cash service on below providers and expect status 200 in the context
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email   | phone_number |
      | BCId1               | CPId1                       | ECPId1                          | Cash       | Service   | SG     | x@y.com | 00000000     |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | customer_profile_id | first_name | last_name | email   | phone_number | status |
      | CPId1                       | ECPId1                          | CPId1               | Cash       | Service   | x@y.com | 00000000     | ACTIVE |

    Given I onboard EndCustomerProfile ECPId1 of CustomerProfile CPId1 on cash service on below providers and expect status 200
      | provider_name |
      | DBS Bank Ltd  |

    Then I wait until max time to verify EndCustomerProfile ECPId1 of CustomerProfile CPId1 onboard status as ONBOARD_SUCCESS

    Given I create a cash account product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier       | product_type | profile_type | product_class | num_of_active_account |
      | CashAccProductId | CASH_ACCOUNT | END_CUSTOMER | STANDARD      | 1                     |

    Then I approve the product CashAccProductId and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Then I create a end customer cash account with id CashAccId customerProfileID CPId1 with product id CashAccProductId and endCustomerProfileId ECPId1 and expect status as CASH_ACCOUNT_CREATED

    Given I create a product with customer profile CPId1 provider as DBS Bank Ltd and expect product_status PRODUCT_DRAFT
      | identifier | product_type | profile_type | product_class | currency | country | account_type | minimum_balance_limit | minimum_balance_policy |
      | ProductID2 | CASH_WALLET  | END_CUSTOMER | STANDARD      | SGD      | SGP     | SAVINGS      | 0                     | LENIENT                |

    Then I approve the product ProductID2 and verify status as PRODUCT_SUCCESS with provider DBS Bank Ltd for customerProfileId CPId1

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier   | customer_profile_id | end_customer_profile_id | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId | CPId1               |                         | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} | CashAccId       |

    Then I wait until max time to verify the bank account CashWalletId status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

  Scenario: Create, authorize and accept a mandate on cash wallet and perform a mandate transaction using that mandate

    Given I create a Mandate MandateId on Cash Wallet CashWalletId Customer Profile CPId1 and expect header status code as 200 and mandate status as MANDATE_PENDING
      | cash_wallet_id | segment | max_amount | purpose          | metadata        |
      | CashWalletId   | RETAIL  | 100000     | Integration Test | {"key":"value"} |

    Then I authorize the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I accept the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I verify Mandate MandateId for Customer Profile CPId1 is created and expect header status code as 200 and mandate_status as MANDATE_CREATED

    Then I initiate a Mandate Transaction TxId with Mandate MandateId and Cash Wallet CashWalletId for Customer Profile CPId1 with below details and expect header status code as 200 and transaction status as TRANSACTION_PENDING
      | mandate_id | cash_wallet_id | amount | currency | purpose             | metadata        | txn_code | transaction_rail |
      | MandateId  | CashWalletId   | 50000  | SGD      | Integration Testing | {"key":"value"} | MDT      |                  |

    Then I wait until max time to verify the transaction TxId status as TRANSACTION_SETTLED for customerProfileId CPId1

    Then I wait until max time to verify bank account CashWalletId with an available balance of 50000 and total balance of 50000 for customerProfileId CPId1

  Scenario: Create, authorize and accept a mandate on cash wallet and perform a mandate transaction using that mandate with amount greater than maximum amount and expect error

    Given I create a Mandate MandateId on Cash Wallet CashWalletId Customer Profile CPId1 and expect header status code as 200 and mandate status as MANDATE_PENDING
      | cash_wallet_id | segment | max_amount | purpose          | metadata        |
      | CashWalletId   | RETAIL  | 10000      | Integration Test | {"key":"value"} |

    Then I authorize the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I accept the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I verify Mandate MandateId for Customer Profile CPId1 is created and expect header status code as 200 and mandate_status as MANDATE_CREATED

    Then I initiate a Mandate Transaction TxId with Mandate MandateId and Cash Wallet CashWalletId for Customer Profile CPId1 with below details and expect header status code as CSSM_9663 and transaction status as Mandate amount limit breached
      | mandate_id | cash_wallet_id | amount | currency | purpose             | metadata        | txn_code | transaction_rail |
      | MandateId  | CashWalletId   | 50000  | SGD      | Integration Testing | {"key":"value"} | MDT      | FAAST            |

  Scenario: Create, authorize and accept a mandate on cash wallet and perform a mandate transaction using that mandate but with another cash wallet and expect error

    Given I create a Mandate MandateId on Cash Wallet CashWalletId Customer Profile CPId1 and expect header status code as 200 and mandate status as MANDATE_PENDING
      | cash_wallet_id | segment | max_amount | purpose          | metadata        |
      | CashWalletId   | RETAIL  | 10000      | Integration Test | {"key":"value"} |

    Then I authorize the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I accept the Mandate MandateId for Customer profile CPId1 and expect header status code as 200

    Then I verify Mandate MandateId for Customer Profile CPId1 is created and expect header status code as 200 and mandate_status as MANDATE_CREATED

    Given I create account for EndCustomerProfile with id ECPId1 for CustomerProfile CPId1 with product id ProductID2 with bank account type as e-money with provider DBS Bank Ltd and expect the header status 200
      | identifier    | customer_profile_id | end_customer_profile_id | currency | country | in_trust | on_behalf_of | metadata                           | cash_account_id |
      | CashWalletId1 | CPId1               |                         | SGD      | SGP     | false    | CUSTOMER     | {"key": "TransactionIntegration1"} |                 |

    Then I wait until max time to verify the bank account CashWalletId1 status as CASH_WALLET_CREATED with provider DBS Bank Ltd for customerProfileId CPId1

    Then I initiate a Mandate Transaction TxId with Mandate MandateId and Cash Wallet CashWalletId1 for Customer Profile CPId1 with below details and expect header status code as CSSM_9101 and transaction status as Mandate is not created or invalid
      | mandate_id | cash_wallet_id | amount | currency | purpose             | metadata        | txn_code | transaction_rail |
      | MandateId  | CashWalletId1  | 50000  | SGD      | Integration Testing | {"key":"value"} | MDT      |                  |
