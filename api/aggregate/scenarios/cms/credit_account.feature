Feature: CMS service's Credit Account scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name   | last_name   | region   | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John         | Snow        | SG       | john@snow.com | +63 1234567890 |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status |
      | CPid1                       | ECPid1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE |

    Then I onboard End Customer Profile ECPid1 to CMS and verify onboard status as ONBOARD_SUCCESS and status code as 200

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group              |
      | Pid1       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_params_group |

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description            |
      | TXN1             | ISO1     | First transaction code |
      | TXN2             | ISO2     | Second one             |
      | TXN3             | ISO3     | Third transaction code |
      | TXN4             | ISO4     | Fourth one             |

    Then I create bucket config for product Pid1 and verify status code is 200
      | bucket_name               | bucket_code | txn_codes  | interest_type      | repayment_priority | limit_percentage | apr  |
      | Standard Interest Bucket  | STD_001     | TXN1, TXN2 | STANDARD_INTEREST  | 1                  | 50.0             | 10.5 |
      | Immediate Interest Bucket | IMD_002     | TXN3, TXN4 | IMMEDIATE_INTEREST | 2                  | 30.0             | 12.0 |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

  Scenario: Successful Credit Account Creation

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 100000         | 10            |

  Scenario: Attempt to Create Credit Account for Unknown Product

    Then I create below credit accounts and verify account status is ACCOUNT_FAILED and status code is CMSM_9681
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | dummyPid   | SGP     | SGD      | 100000         | 10            |

  Scenario: Failed Credit Account Creation due to Unknown End Customer Profile

    Then I create below credit accounts and verify account status is ACCOUNT_FAILED and status code is E9800
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid2                  | CAid1      | Pid1       | SGP     | SGD      | 100000         | 10            |


  Scenario: Failed Credit Account Creation due to Inactive Product

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name   | product_type   | description                               | product_class | profile_type | product_category | param_group              |
      | Pid3       | My Credit Card | CREDIT_ACCOUNT | Premium Credit Card for Premium Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_params_group |

    Then I create below credit accounts and verify account status is ACCOUNT_FAILED and status code is CMSM_9683
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid3       | SGP     | SGD      | 100000         | 10            |

  Scenario: Credit Account Closure Successful When No Transactions Are Being Made

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 100000         | 10            |

    Given I attempt to close the following credit accounts and verify status code is 200
      | account_id | account_status        |
      | CAid1      | CREDIT_ACCOUNT_CLOSED |

  Scenario:  Credit Account Closure Failed because  Debit Transactions Remain Unrepaid

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 100000         | 10            |

    Given I have mocked the following transactions for CAid1 in the current billing cycle and status code is 200
      | amount | txn_type | day | txn_code | txn_status          |
      | 100    | DEBIT    | 5   | TXN3     | TRANSACTION_SETTLED |

    Then I Wait some time to get the transactions updated

    Given I attempt to close the following credit accounts and verify status code is CMSM_9664
      | account_id |
      | CAid1      |

  Scenario: Credit Account Closure Failed for Unknown Credit Account

    Given I attempt to close the following credit accounts and verify status code is CMSM_9641
      | account_id |
      | CAid2      |

  Scenario: Credit Account Closure Successful because All Debit Transactions Are Repaid

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 100000         | 10            |

    Given I have mocked the following transactions for CAid1 in the current billing cycle and status code is 200
      | amount | txn_type | day | txn_code | txn_status          |
      | 100    | DEBIT    | 5   | TXN3     | TRANSACTION_SETTLED |
      | 100    | CREDIT   | 10  | TXN3     | TRANSACTION_SETTLED |

    Then I Wait some time to get the transactions updated

    Given I attempt to close the following credit accounts and verify status code is 200
      | account_id |
      | CAid1      |

  Scenario: Credit Account Closure Successful as Debit Transactions Was Rejected

    Then I create below credit accounts and verify account status is ACCOUNT_CREATED and status code is 200

      | end_customer_profile_id | account_id | product_id | country | currency | approved_limit | interest_rate |
      | ECPid1                  | CAid1      | Pid1       | SGP     | SGD      | 1000           | 10            |

    Given I have mocked the following transactions for CAid1 in the current billing cycle and status code is 200
      | amount | txn_type | day | txn_code | txn_status           |
      | 2000   | DEBIT    | 5   | TXN3     | TRANSACTION_REJECTED |
      | 2000   | DEBIT    | 5   | TXN3     | TRANSACTION_REJECTED |

    Given I attempt to close the following credit accounts and verify status code is 200
      | account_id |
      | CAid1      |
