Feature: Loan Transaction Scenarios

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

    Then I create below loan accounts and verify account status is ACCOUNT_CREATED and status code is 200
      | end_customer_profile_id | account_id | product_id | approved_amount | tenure | interest_rate | beneficiary_account      |
      | ECPid1                  | LAid1      | Pid1       | 100000          | 24     | 7.5           | loan_beneficiary_account |

  Scenario: Successful Loan Disbursement Transaction

    Given I fetch the original balance for the loan account and store it in the context
      | loan_account_id |
      | LAid1           |

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 5000   | SGD      | L1       |
      | LAid1           | 6000   | SGD      | L1       |
      | LAid1           | 4000   | SGD      | L1       |

    Then I verify the loan account balance after the transaction and status code as 200
      | loan_account_id |
      | LAid1           |

  Scenario: Transaction Amount Greater than Approved Loan Limit for LA Disbursement

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_INVALID and status code as CMSM_9653
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 100001 | SGD      | L1       |

  Scenario: Invalid Currency for LA Disbursement

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_INVALID and status code as E9400
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 10000  | SGDA     | L1       |

  Scenario Outline: Loan Account Not Found for LA Disbursement

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_INVALID and status code as <status_code>
      | loan_account_id | amount | currency | txn_code |
      | <account_id>    | 96     | SGD      | L1       |

    Examples:
      | account_id | status_code |
      | EMPTY      | E9400       |
      | LAid2      | CMSM_9641   |

  Scenario: Interest Txn -> Loan Repayment -> (Partial Interest) Recovered

    Given I fetch the original balance for the loan account and store it in the context
      | loan_account_id |
      | LAid1           |

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 1000   | SGD      | L1       |

    Then I verify the loan account balance after the transaction and status code as 200
      | loan_account_id |
      | LAid1           |

    Then I initiate interest transaction and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Given I fetch the original ledgers balances for loan account and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Then I Initiate Dev LA Repayment and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | purpose | amount | currency | customer_profile_id | account_type |
      | LAN     | 5      | SGD      | Cid1                | REPAYMENT_LA |

    Then I fetch and verify the latest ledgers balances for loan account and verify status code as 200
      | loan_account_id | case             | amount |
      | LAid1           | partial_interest | 5      |

  Scenario: Loan Disbursement -> Interest Txn -> Loan Repayment -> (Full Interest + Partial Principal) Recovered

    Given I fetch the original balance for the loan account and store it in the context
      | loan_account_id |
      | LAid1           |

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 1000   | SGD      | L1       |

    Then I verify the loan account balance after the transaction and status code as 200
      | loan_account_id |
      | LAid1           |

    Then I initiate interest transaction and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Given I fetch the original ledgers balances for loan account and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Then I Initiate Dev LA Repayment and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | purpose | amount | currency | customer_profile_id | account_type |
      | LAN     | 10     | SGD      | Cid1                | REPAYMENT_LA |

    Then I fetch and verify the latest ledgers balances for loan account and verify status code as 200
      | loan_account_id | case              | amount |
      | LAid1           | partial_principal | 10     |

  Scenario: Loan Disbursement -> Interest Txn -> Loan Repayment -> (Full Interest + Full Principal) Recovered

    Given I fetch the original balance for the loan account and store it in the context
      | loan_account_id |
      | LAid1           |

    Then I create loan disbursement transaction and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | loan_account_id | amount | currency | txn_code |
      | LAid1           | 1000   | SGD      | L1       |

    Then I verify the loan account balance after the transaction and status code as 200
      | loan_account_id |
      | LAid1           |

    Then I initiate interest transaction and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Given I fetch the original ledgers balances for loan account and verify status code as 200
      | loan_account_id |
      | LAid1           |

    Then I Initiate Dev LA Repayment and verify transaction status as TRANSACTION_SETTLED and status code as 200
      | purpose | amount | currency | customer_profile_id | account_type |
      | LAN     | 1006.2 | SGD      | Cid1                | REPAYMENT_LA |

    Then I fetch and verify the latest ledgers balances for loan account and verify status code as 200
      | loan_account_id | case          |
      | LAid1           | full_recovery |
