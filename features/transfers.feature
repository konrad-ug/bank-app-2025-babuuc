Feature: Account transfers

  Background:
    Given Account registry is empty
    And I create an account using name: "Elon", last name: "Musk", pesel: "55555555555"

  Scenario: Incoming transfer increases balance
    When I make an incoming transfer of "1000" to account with pesel "55555555555"
    Then Account with pesel "55555555555" has balance equal to "1000"

  Scenario: Outgoing transfer decreases balance
    Given I make an incoming transfer of "500" to account with pesel "55555555555"
    When I make an outgoing transfer of "200" from account with pesel "55555555555"
    Then Account with pesel "55555555555" has balance equal to "300"

  Scenario: Outgoing transfer fails when insufficient funds
    When I make an outgoing transfer of "100" from account with pesel "55555555555"
    Then Transfer fails with message "Insufficient funds"
    And Account with pesel "55555555555" has balance equal to "0"