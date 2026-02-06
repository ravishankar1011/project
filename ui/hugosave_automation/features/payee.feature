Feature: PAYEE

  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | ns@12gmail.com | 111111   |
    When I wait for the premium upgrade to complete
    Given I tap on the spend account banner on the home screen
    When I tap on the Spend Account Dashboard Button and Close Announcement Modals

  Scenario: Adding payee with invalid OTP
    Given I tap on the Add Payee button on the Spend account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name    | account_no |
      | ram        | DBS Bank Ltd | 6334903364 |
    Then I click on the confirm button
    Then I verify that i reached the OTP Screen
    Then I enter the OTP 123455 to add payee
    Then I check for the error message for incorrect OTP while adding payee


  Scenario: Add a Payee with Valid OTP and Verify Spend Account Dashboard and All Payees Screen
    Given I tap on the Add Payee button on the Spend account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name    | account_no    |
      | Mark       | DBS Bank Ltd | 9418237341424 |
    Then I click on the confirm button
    Then I verify that i reached the OTP Screen
    Then I enter the OTP 123456 to add payee
    Then I tap on the Done button
    Then I check if the newly added payee Mark is appearing on the spend account dashboard
    Then I tap on the See All text link on the Spend account dashboard
    Then I verify that i reached the All Payees Screen
    Then I check if the newly added payee Mark is appearing on the All payees screen
    Then On the All Payees screen, I tap on the payee name Mark
    Then I verify the payee's addition by checking the payee Mark account number on the auto-directed payee individual screen

  Scenario: Validate Error Handling When Name, Account Number, or Bank Name is Left Empty While Adding a Payee
    Given I tap on the Add Payee button on the Spend account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name                    | account_no   |
      |            | Citibank NA Singapore Branch | 132334903364 |
    Then I verify the payee name and validate the error message for invalid input
    Then I verify the confirm button is disabled
    Then I tap on the back button on the Add New Payee screen

    Given I tap on the Add Payee button on the cash account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name | account_no   |
      | ram        |           | 132334903364 |
    Then I verify the payee name and validate the error message for invalid input
    Then I verify the confirm button is disabled
    Then I tap on the back button on the Add New Payee screen

    Given I tap on the Add Payee button on the cash account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name                    | account_no |
      | ram1       | Citibank NA Singapore Branch |            |
    Then I verify the payee name and validate the error message for invalid input
    Then I verify the confirm button is disabled
    Then I tap on the back button on the Add New Payee screen


  Scenario: Validate the payee transaction
    When I deposit amount using non prod options 500
    When I top up the Spend Account with 100
    Given I tap on the Add Payee button on the Spend account dashboard
    Given I enter Payee Name, Select Bank and Account Number
      | payee_name | bank_name                    | account_no  |
      | Mark       | Citibank NA Singapore Branch | 94182234142 |
    Then I click on the confirm button
    Then I verify that i reached the OTP Screen
    Then I enter the OTP 123456 to add payee
    Then I tap on the Done button
    Then I tap on the payee name Mark
    Then I verify the payee's addition by checking the payee Mark account number on the auto-directed payee individual screen
    Then I tap on the New Payment button on the payee individual screen
    Then I enter the payee amount 1 on the New Payment screen
    Then I select the reason chip on the Mark payee New payment screen
    Then I tap on the Preview button on the New Payment screen
    Then I tap on the Pay button on the New Payment Preview screen
    Then I verify if i auto-directed to the payee Mark individual screen
    Then I click on the latest transaction record appears for the Mark payee
    Then I verify the latest transaction is Settled for the Mark payee
