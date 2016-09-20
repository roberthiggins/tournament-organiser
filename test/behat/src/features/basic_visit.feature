Feature: Front page of the website
  In order to use TO from the internet
  As a website user
  I need to be able to visit the font page

  @javascript
  Scenario: I visit the front page
    Given I am on "/"
    Then I should see "Here you can play in or organise wargaming tournaments. Log in to see lists of tournaments you can enter or create your own." appear
