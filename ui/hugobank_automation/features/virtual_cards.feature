Feature: Virtual Cards
  Background:
    Given I sign up with bypass number
      | prefix | name  | place_of_birth | maiden_name |
      | +9247  | Ishaa | Sector 17B     | Fernandez   |

  Scenario: I order a virtual card
    When I move to the order visa virtual debit card screen
    When I tap on the each pre defined card name labels
      | toggle       |
      | Shopping     |
      | Grocery      |
      | Subscription |
      | Education    |
    Then I select each pre defined tab and validate the reflection in the card name field
    When I enter card name as Gym in the field
    When I click on the continue button
    When I click on the place order button
    Then I input valid passcode 123456

  Scenario: I validate show card details and copy card number
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I click on the unhide icon and validate full card number expiry and cvv text
    When I click on the copy button and validate copied text

  Scenario: I make a transaction using virtual card and validate it
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I click on the home tab
    When I make an auth clear card transaction of PKR 100
    Then I validate the current balance and transaction record on the virtual card dashboard

  Scenario: I validate the lock and unlock virtual card functionality
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
   When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
   When I wait for the virtual card to be appeared on the card dashboard
   When I lock the virtual card with valid passcode 123456
    When I click on the back button on the virtual card dashboard
   When I click on the back button on the cards dashboard
   When I make an auth clear card transaction of PKR 100
   Then I validate failed transaction record on the virtual card dashboard
   When I click on the back button on the transaction record
   When I unlock the virtual card with valid passcode 123456
   When I click on the back button on the virtual card dashboard
   When I click on the back button on the cards dashboard
   When I make an auth clear card transaction of PKR 100
   Then I validate the current balance and transaction record on the virtual card dashboard

  Scenario: I validate virtual card limits functionality
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I update the virtual card default limit to 200
    Then I input valid passcode 123456
    When I click on the Save button
    Then I input valid passcode 123456
    When I reach to the cards dashboard
    When I click on the home tab
    When I make an auth clear card transaction of PKR 500
    Then I validate failed transaction record on the virtual card dashboard
    When I move to the cards dashboard
    When I click on the home tab
    When I make an auth clear card transaction of PKR 10
    Then I validate the current balance and transaction record on the virtual card dashboard

  Scenario: I validate the daily limit reaching soon alert text
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I update the virtual card default limit to 200
    Then I input valid passcode 123456
    When I click on the Save button
    Then I input valid passcode 123456
    When I reach to the cards dashboard
    When I click on the home tab
    When I make an auth clear card transaction of PKR 190
    Then I validate daily limit reaching soon text on the virtual card dashboard

  Scenario: I validate the daily limit exhausted alert text
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I update the virtual card default limit to 200
    Then I input valid passcode 123456
    When I click on the Save button
    Then I input valid passcode 123456
    When I reach to the cards dashboard
    When I click on the home tab
    When I make an auth clear card transaction of PKR 200
    Then I validate daily limit exhausted text on the virtual card dashboard

  Scenario: I validate E-commerce transaction when toggle is OFF for a virtual card
    Given I have deposited 500 PKR into my account using non-prod options
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I turn off the 'E-commerce' toggle
    When I click on the Save button
    Then I input valid passcode 123456
    When I click on the Save button
    Then I input valid passcode 123456
    Then I move to the homescreen
    When I make an auth clear card transaction of PKR 200
    When I validate failed transaction record on the virtual card dashboard

  Scenario: I validate cancel virtual card functionality
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness   | 123456   |
    When I click on the card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    When I cancel the virtual card
    Then I input valid passcode 123456
    Then I validate the cancelled text on the screen

  Scenario: I order all five virtual cards
    When I move to the order visa virtual debit card screen
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Grocery   | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I move to the order visa virtual debit card screen from the cards dashboard
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Fitness         | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I move to the order visa virtual debit card screen from the cards dashboard
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Gym       | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I move to the order visa virtual debit card screen from the cards dashboard
    Given I order a virtual card with the below name and passcode
      | card_name | passcode |
      | Education | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I move to the order visa virtual debit card screen from the cards dashboard
    Given I order a virtual card with the below name and passcode
      | card_name    | passcode |
      | Subscription | 123456   |
    When I click on the card dashboard
    When I click on the back button on the virtual card dashboard
    When I wait for the virtual card to be appeared on the card dashboard
    Then I validate order virtual card button should be in disable state
