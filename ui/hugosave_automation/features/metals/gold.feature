Feature: Gold module
 Background:
     Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | ns@12gmail.com | 111111   |
     When I wait for the premium upgrade to complete
     When I deposit amount using non prod options 500
     When I move to the gold dashboard from the homescreen

 Scenario: I buy gold with balance in the save account
  When I click on the buy button
  When I enter amount 50 and click on preview
  When I click on the buy button
  Then I validate successfully bought message on the screen

 Scenario: I buy gold in grams
  When I click on the buy button
  When I switch to grams and enter 10 grams
  When I click on the preview button
  When I click on the buy button
  Then I validate successfully bought message on the screen

 Scenario: I sell gold
  When I click on the buy button
  When I enter amount 50 and click on preview
  When I click on the buy button
  Then I validate successfully bought message on the screen
  When I click on the skip button
  When I click on the sell button
  When I enter amount 5 and click on preview
  When I click on the sell button

 Scenario: I sell gold in grams
  When I click on the buy button
  When I enter amount 50 and click on preview
  When I click on the buy button
  Then I validate successfully bought message on the screen
  When I click on the skip button
  When I click on the sell button
  When I switch to grams and enter 10 grams
  When I click on the preview button
  When I click on the sell button




