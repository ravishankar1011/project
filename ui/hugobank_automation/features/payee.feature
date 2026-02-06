Feature: Payee
 Background: Signup
   Given I sign up with bypass number
     | prefix    |  name  | place_of_birth | maiden_name |
     | +9247     | Ishaa  | Sector 17B     | Fernandez   |

 Scenario: Validate external payee addition with missing account details
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name | account_prefix |
     |           |                |
   Then The Submit button should be disabled

   When I enter account details
     | bank_name | account_prefix |
     |           | 1020           |
   Then The Submit button should be disabled
   Then I clear the account number field

   When I enter account details
     | bank_name       | account_prefix |
     | Test Bank Raast |                |
   Then The Submit button should be disabled

 Scenario: Add external payee with invalid account number
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix |
     | Test Bank Raast | 111            |
   Then I should see an error message No account found

 Scenario: Add external payee with incorrect OTP
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 111111
   Then I should see an error message Incorrect OTP

 Scenario: Add external payee with incorrect passcode
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 111111
   Then I should see an error message Incorrect Passcode

 Scenario: Add external payee with Account Number and IBAN number
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I validate the UI of the Account Page
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   Then I go to Home Screen from Payee screen

   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details with IBAN
     | bank_name       | IBAN_prefix  |
     | Test Bank Raast | PK20         |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully

 Scenario: Pay to External Payee
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   And I click on Proceed and Pay buttons
   And I enter the passcode 123456
   Then The transaction should be settled

 Scenario: Add external payee using RAAST ID with invalid details
   Given I tapped on the Fund Transfer button and selected RAAST ID
   Then I validate Submit button is in disable state
   When I enter the incorrect RAAST ID
   Then I should see an error message No account found
   Then I clear the RAAST ID input field
   When I enter the RAAST ID
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 111111
   Then I should see an error message Incorrect OTP
   When I enter the OTP 123456
   And I enter the passcode 111111
   Then I should see an error message Incorrect Passcode

 Scenario: Add external payee using RAAST ID and make payment
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected RAAST ID
   When I enter the RAAST ID
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   And I click on Proceed and Pay buttons
   And I enter the passcode 123456
   Then The transaction should be settled

 Scenario: I create and delete a schedule for an external payee
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I delete the payment schedule
   Then I verify that the payment schedule has been deleted successfully

 Scenario: I validate stopping and resuming a payment schedule for an external payee
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I verify stopping the payment schedule
   And I verify Resuming the payment Schedule

 Scenario: I validate schedule combinations and trigger the schedule for an external payee
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
	   | frequency | amount | start_date | make_payment | preview_button |
       | Weekly    |        |            |              | disabled       |
       | Monthly   | 100    |            |              | disabled       |
       | Weekly    | 20     |            | Once         | disabled       |
       | Daily     | 100    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I go to Home Screen from Payee screen
   And I trigger the payment schedule using non-prod options
   Then I verify that the schedule is triggered and amount 200.00 is settled on the payee screen

 Scenario: I validate editing payment schedule for an external payee
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
	   | frequency | amount | start_date | make_payment | preview_button |
	   | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   When I navigate to the edit schedule screen
   When I edit the schedule with the following details
      | frequency | amount | make_payment | save_button |
      | Weekly    | 300    | Once         | enabled     |
   And I click the Save button
   Then I verify the edited schedule is displayed on Payee Screen

 Scenario: I validate the payment schedule transaction is not triggered after stopping it
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   When I stop the schedule
   Then I click on the back button
   Then I go to Home Screen from Payee screen
   And I trigger the payment schedule using non-prod options
   Then I verify that the schedule is not triggered

 Scenario: I validate editing and deleting an external payee
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   Then I validate editing payee
   And I validate deleting payee

 Scenario: I validate deleting payee leads to deleting schedule
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   And I validate deleting payee with schedule

 Scenario: I validate external payee limits functionality
   Given I tapped on the Fund Transfer button and selected Other Bank Account Details
   When I enter account details
     | bank_name       | account_prefix  |
     | Test Bank Raast | 1020            |
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   Then I should see an error message Insufficient account balance
   Then I click on the back button on the payee transaction screen
   Then I go to Home Screen from Payee screen
   Given I have deposited 500 PKR into my account using non-prod options
   When I edit my other bank limit to 100
   When I select already added payee
   And I click on Pay button
   And I enter amount 200 and select purpose of transaction
   Then I should see an error message Reached the account transfer limit

 Scenario: Store internal account details and Raast ID
   Given I save the internal account number and IBAN number
   When I link the Raast ID to the Hugobank account number
   Then I save the internal Raast ID

 Scenario: Add internal payee with invalid details
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter invalid HugoBank account number
   Then I should see an error message No account found
   Then I clear the internal account number field
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 111111
   Then I should see an error message Incorrect OTP
   When I enter the OTP 123456
   And I enter the passcode 111111
   Then I should see an error message Incorrect Passcode

 Scenario: Add internal payee with IBAN number
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank IBAN number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully

 Scenario: Add internal payee and make payment
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   And I click on Proceed and Pay buttons
   And I enter the passcode 123456
   Then The transaction should be settled

 Scenario: Add internal payee using RAAST ID with incorrect details
   Given I tapped on the Fund Transfer button and selected RAAST ID
   When I enter the internal RAAST ID
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 111111
   Then I should see an error message Incorrect OTP
   When I enter the OTP 123456
   And I enter the passcode 111111
   Then I should see an error message Incorrect Passcode

 Scenario: Add internal payee using RAAST ID and make payment
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected RAAST ID
   When I enter the internal RAAST ID
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   And I click on Proceed and Pay buttons
   And I enter the passcode 123456
   Then The transaction should be settled

 Scenario: I create and delete a payment schedule for internal payee
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I delete the payment schedule
   Then I verify that the payment schedule has been deleted successfully

 Scenario: I validate stopping and resuming a payment schedule for internal payee
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
     | frequency | amount | start_date | make_payment | preview_button |
     | Daily     | 200    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I verify stopping the payment schedule
   And I verify Resuming the payment Schedule

 Scenario: I validate schedule combinations and triggering it for internal payee
   Given I have deposited 500 PKR into my account using non-prod options
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Create Payment Schedule button on the New Payee Screen
   And I create a new schedule with the following details
	   | frequency | amount | start_date | make_payment | preview_button |
	   | Weekly    |        |            |              | disabled       |
	   | Monthly   | 100    |            |              | disabled       |
	   | Weekly    | 20     |            | Once         | disabled       |
	   | Monthly   |        |            | Once         | disabled       |
	   | Weekly    |        | today      | Twice        | disabled       |
	   | Daily     | 100    | today      | Once         | enabled        |
   And I confirm the Schedule
   Then I verify the new schedule is displayed on Payee Screen
   Then I go to Home Screen from Payee screen
   And I trigger the payment schedule using non-prod options
   Then I verify that the schedule is triggered and amount 200.00 is settled on the payee screen

 Scenario: I validate internal payee limits functionality
   Given I tapped on the Fund Transfer button and selected HugoBank Account Details
   When I enter HugoBank account number
   And I click on Submit button
   And I click on Get OTP button
   And I enter the OTP 123456
   And I enter the passcode 123456
   Then The payee should be added successfully
   When I click on Pay button
   And I enter amount 100 and select purpose of transaction
   Then I should see an error message Insufficient account balance
   Then I click on the back button on the emulator
   Then I go to Home Screen from Payee screen
   Given I have deposited 500 PKR into my account using non-prod options
   When I edit my other HugoBank limit to 100
   When I select already added payee
   And I click on Pay button
   And I enter amount 200 and select purpose of transaction
   Then I should see an error message Reached the account transfer limit
