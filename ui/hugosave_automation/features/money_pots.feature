Feature: Money Pots
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | ns@12gmail.com | 111111   |
    When I wait for the premium upgrade to complete

  Scenario: I create a pot with pot name goal amount and goal date
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P1
    When I enter goal amount as 100
    When I select goal date
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen

  Scenario: I create a pot with only pot name and goal amount
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P2
    When I enter goal amount as 100
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen

  Scenario: I create a pot with only pot name and goal date
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P3
    When I select goal date
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen

  Scenario: I create a pot with only pot name
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P4
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen

  Scenario: I add one dollar to the pot after creation
    When I deposit amount using non prod options 500
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P100
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen
    When I click on the add one dollar to the pot button after creation
    When I click on the add button on the preview screen

  Scenario: I add amount to the pot
    When I deposit amount using non prod options 500
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P101
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen
    When I click on the i will do it later button
    When I click on the add to pot button on the pot dashboard
    When I enter amount 10 and click on preview
    When I click on the add button on the preview screen
    Then I validate amount added successfully text on the screen
    Then I validate current value of the pot 10


  Scenario: I withdraw amount from the pot
    When I deposit amount using non prod options 500
    When I move to the pot dashboard from the homescreen
    When I click on the new pot icon
    When I input pot name as P1011
    When I click on the next button
    When I click on the create pot button
    Then I validate successfully created text on the screen
    When I click on the i will do it later button
    When I click on the add to pot button on the pot dashboard
    When I enter amount 100 and click on preview
    When I click on the add button on the preview screen
    Then I validate amount added successfully text on the screen
    Then I validate current value of the pot 100
    When I click on the withdraw button
    When I enter amount 10 and click on preview
    When I click on the withdraw button on the preview screen
    Then I validate withdrawn successfully text
    Then I validate current value of the pot 90



