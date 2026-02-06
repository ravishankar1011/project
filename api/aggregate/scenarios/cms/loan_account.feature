Feature: CMS service's Loan Account scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John       | Snow      | SG     | john@snow.com | +63 1234567890 |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status |
      | CPid1                       | ECPid1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE |

    Then I onboard End Customer Profile ECPid1 to CMS and verify onboard status as ONBOARD_SUCCESS and status code as 200

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name    | product_type | description             | product_class | profile_type | product_category | param_group                     |
      | Pid1       | My Loan Account | LOAN_ACCOUNT | LOAN ACCOUNT FOR MYSELF | STANDARD      | CUSTOMER     | GEN              | normal_case_loan_account_params |

    Then I approve following products and verify product status to be PRODUCT_SUCCESS and status code is 200
      | product_id |
      | Pid1       |

  Scenario: Loan Account Creation -> Action Fee Charged -> Success

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description          |
      | FEE              | ISO_FEE  | Fee transaction code |

    Then I create fee for the Product and verify status code as 200
      | product_id | fee_code | txn_code | fee_type   | push_overdraft | rule_group        | fee_details |
      | Pid1       | LA_FEE   | FEE      | ACTION_FEE | true           | la_fee_rule_group | ACTION      |

    Then I update the following products and verify the response status is 200
      | product_id | param_group |
      | Pid1       | fee         |

    Then I create below loan accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | approved_amount | tenure | interest_rate | beneficiary_account      |
      | ECPid1                  | LAid1      | Pid1       | 1000            | 24     | 7.5           | loan_beneficiary_account |

    Given I fetch the original ledgers balances for loan account and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Then I fetch and verify the latest ledgers balances for loan account and verify status code as 200
      | loan_account_id | case       | amount |
      | LAid1           | la_opening | 100    |


  Scenario: Attempt to Create Loan Account for Unknown Product

    Then I create below loan accounts and verify account status is ACCOUNT_CREATED and status code is CMSM_9681
      | end_customer_profile_id | account_id | product_id | approved_amount | tenure | interest_rate | beneficiary_account      |
      | ECPid1                  | LAid1      | dummyPid   | 100000          | 24     | 6.5           | loan_beneficiary_account |

  Scenario: Failed Loan Account Creation due to Inactive Product

    Then I create following products and verify product status to be PRODUCT_DRAFT and status code is 200
      | product_id | product_name | product_type | description                     | product_class | profile_type | product_category | param_group                     |
      | Pid2       | My Loan      | LOAN_ACCOUNT | Personal Loan for End Customers | STANDARD      | CUSTOMER     | GEN              | normal_case_loan_account_params |

    Then I create below loan accounts and verify account status is ACCOUNT_CREATION_FAILED and status code is CMSM_9683
      | end_customer_profile_id | account_id | product_id | approved_amount | tenure | interest_rate | beneficiary_account      |
      | ECPid1                  | LAid1      | Pid2       | 100000          | 24     | 6.5           | loan_beneficiary_account |
