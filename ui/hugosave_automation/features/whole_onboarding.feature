Feature: Signup: Create a New Account

  Scenario: Disable "Get OTP" Button for Invalid Mobile Number
    Given I verify that I have entered the signup screen
    Given I enter the mobile number 373
    Then I verify that the Get OTP button is disabled

  Scenario: Enter an Invalid OTP After a Valid Mobile Number
    Given I verify that I have entered the signup screen
    Given I enter the mobile number Ph2
    Then I tap on the Get OTP button
    Then I verify that I have entered the OTP screen
    Then I enter the OTP 123453
    Then I verify that an error message is displayed for an incorrect OTP

  Scenario: Enter a valid OTP and enter Invalid User Details During Account Creation
    Given I verify that I have entered the signup screen
    Given I enter the mobile number Ph2
    Then I tap on the Get OTP button
    Then I verify that I have entered the OTP screen
    Then I enter the OTP 123456
    Then I verify that I have entered the Create Account screen

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email             | tick_check_box |
      | John2       | Doe1       | John@gmail.com | true           |
    Then I verify the user details and validate error messages for invalid inputs
    Then I verify the continue button is disabled
    Then I clear the fields

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email         | tick_check_box |
      | John        | Doe        | @hn_gmail.com | true           |
    Then I verify the user details and validate error messages for invalid inputs
    Then I verify the continue button is disabled
    Then I clear the fields

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email             | tick_check_box |
      | sai         |            | jane123@gmail.com | true           |
    Then I verify the user details and validate error messages for invalid inputs
    Then I verify the continue button is disabled
    Then I clear the fields

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email  | tick_check_box |
      | Alex 23     | Doe        |        | false           |
    Then I verify the user details and validate error messages for invalid inputs
    Then I verify the continue button is disabled
    Then I clear the fields

    Scenario: Enter Mismatched Passcodes During Passcode Setup
      Given I verify that I have entered the signup screen
      Given I enter the mobile number Ph2
      Then I tap on the Get OTP button
      Then I verify that I have entered the OTP screen
      Then I enter the OTP 123456
     Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email         | tick_check_box |
      | John        | Doe        | john@mail.com | true          |
      Then I click on the continue button
      Then I check whether I have reached the Set Passcode screen
      Given I enter passcodes in both fields
      | passcode_field1 | passcode_field2 |
      | 111111          | 1111222          |
      Then I verify that the create account button is disabled
      Then I check for the error message
      Then I clear the passcode fields

  Scenario: Complete Onboarding With Mixed Valid and Invalid Inputs
    Given I enter the mobile number 34343
    Then I verify that the Get OTP button is disabled
    Given I enter the mobile number Ph1
    Then I verify that the Get OTP button is  enabled
    Then I tap on the Get OTP button
    Then I verify that I have entered the OTP screen
    Then I enter the OTP 123456
    Then I verify that I have entered the Create Account screen

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email  | tick_check_box |
      | Alex 23     | Doe        |        | true           |
    Then I verify the user details and validate error messages for invalid inputs
    Then I verify the continue button is disabled
    Then I clear the fields

    Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email         | tick_check_box |
      | John        | Doe        | john@mail.com | true          |
    Then I verify the continue button is enabled
    Then I click on the continue button
    Then I check whether I have reached the Set Passcode screen

    Given I enter passcodes in both fields
      | passcode_field1 | passcode_field2 |
      | 111111          | 111112          |
    Then I verify that the create account button is disabled
    Then I check for the error message
    Then I clear the passcode fields

    Given I enter passcodes in both fields
      | passcode_field1 | passcode_field2 |
      | 111111          | 1111111        |
    Then I verify that the create account button is enabled
    Then I click on the Create account button
    Then I verify if I am directed to the Allow Notifications screen and check the text elements and button
    Given I tap on the allow notification button
    Then I verify that i have reached the Home screen

    Scenario: Onboard to save account dashboard
      Given I verify that I have entered the signup screen
      Given I enter the mobile number Ph2
      Then I verify that the Get OTP button is enabled
      Then I tap on the Get OTP button
      Then I verify that I have entered the OTP screen
      Then I enter the OTP 123456
      Then I verify that I have entered the Create Account screen
     Given I enter a casual name, a legal name, an email, and tick the checkbox
      | casual_name | legal_name | email         | tick_check_box |
      | John        | Doe        | john@mail.com | true          |
      Then I verify the continue button is enabled
      Then I click on the continue button
      Then I check whether I have reached the Set Passcode screen
     Given I enter passcodes in both fields
      | passcode_field1 | passcode_field2 |
      | 111111          | 1111111         |
    Then I verify that the create account button is enabled
    Then I click on the Create account button
    Then I verify if I am directed to the Allow Notifications screen and check the text elements and button
    Given I tap on the allow notification button
    Then I verify that i have reached the Home screen
