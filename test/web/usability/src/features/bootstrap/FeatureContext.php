<?php

use Behat\Behat\Context\ClosuredContextInterface,
    Behat\Behat\Context\TranslatedContextInterface,
    Behat\Behat\Context\BehatContext,
    Behat\Behat\Exception\PendingException;
use Behat\Gherkin\Node\PyStringNode,
    Behat\Gherkin\Node\TableNode;

use Behat\MinkExtension\Context\MinkContext;

require 'vendor/autoload.php';

class FeatureContext extends MinkContext
{
    /**
     * Spin for waiting for a response
     */
    public function spin($text, $lambda, $wait = 5)
    {
        $time = time();
        $stopTime = $time + $wait;
        while (time() < $stopTime)
        {
            try {
                if ($lambda($this)) {
                    return;
                }
            } catch (\Exception $e) {
                // do nothing
            }

            usleep(1000);
        }

        throw new \Exception("Spin function timed out: {$text}");
    }
    /**
     * This will wait for up to n seconds
     *
     * Note you'll need to add the @javascript decorator
     *
     * @When /^I wait for (\d+) second(s)?$/
     */
    public function iWaitForTheResponse($delay)
    {
        $time = 1000 * $delay; // milliseconds
        $this->getSession()->wait($time);
    }

    /**
     * @When /^I wait for "([^"]*)" to appear$/
     * @Then /^I should see "([^"]*)" appear$/
     * @param $text
     * @throws \Exception
     */
    public function iWaitForTextToAppear($text)
    {
        $this->spin($text, function(FeatureContext $context) use ($text) {
            try {
                $context->assertPageContainsText($text);
                return true;
            }
            catch(ResponseTextException $e) {
                // NOOP
            }
            return false;
        });
    }

    /**
     * @When /^I wait for "([^"]*)" to appear in field "([^"]*)"$/
     * @Then /^I should see "([^"]*)" appear in field "([^"]*)"$/
     * @param $text
     * @param $el
     * @throws \Exception
     */
    public function iWaitForTextToAppearInField($text, $el)
    {
        $this->spin($text, function(FeatureContext $context) use ($text, $el) {

            try {
                $context->assertFieldContains($el, $text);
                return true;
            }
            catch(ResponseTextException $e) {
                // NOOP
            }

            return false;
        });
    }

    /**
    * @Given /^I am authenticated as "([^"]*)" using "([^"]*)"$/
    */
    public function iAmAuthenticatedAs($username, $password) {
        $this->visit('/login');
        $this->iWaitForTextToAppear('Login to your account');
        $this->fillField('username', $username);
        $this->fillField('password', $password);
        $this->pressButton('Login');
        $this->iWaitForTextToAppear('Welcome to the Tournament Organiser');
    }

    /**
    * @Given /^I visit category page for "([^"]*)"$/
    */
    public function iVisitCategoryPage($tourn) {
        $this->visit('/tournament/'.$tourn.'/categories');
        $this->iWaitForTextToAppear('Once per tournament');
    }

    /**
    * @Given /^I enter game score "([^"]*)", "([^"]*)" for entry "([^"]*)" in tournament "([^"]*)"$/
    */
    public function iEnterGameScore($cat, $score, $user, $tourn) {
        $this->visit('/tournament/'.$tourn.'/entry/'.$user.'/entergamescore');
        $this->iWaitForTextToAppear($cat);
        $this->fillField($cat, $score);
        $this->pressButton('Enter Score');
        $this->iWaitForTextToAppear('Score entered for '.$user.': '.$score);
    }

    /**
    * @Given /^I fill category (\d+) with "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)"$/
    */
    public function iSetDefaultCategories($pos, $name, $per, $min, $max) {
        $this->fillField($pos.'_name', $name);
        $this->fillField($pos.'_percentage', $per);
        $this->fillField($pos.'_min_val', $min);
        $this->fillField($pos.'_max_val', $max);
    }

    /**
    * @Given /^I sign up "([^"]*)"$/
    */
    public function iSignUp($name) {
        $this->visit('/signup');
        $this->iWaitForTextToAppear('Username');
        $this->fillField('username', $name);
        $this->fillField('email', $name.'@foobar.com');
        $this->fillField('password1', $name.'_password');
        $this->fillField('password2', $name.'_password');
        $this->pressButton('Sign Up');
        $this->iWaitForTextToAppear('Account created');
    }

    /**
    * @Given /^I visit the tournament creation page$/
    */
    public function iVisitTournamentCreationPage() {
        $this->visit('/tournament/create');
        $this->iWaitForTextToAppear('Create Tournament');
        $this->iWaitForTextToAppear('Tournament Name:');
        $this->iWaitForTextToAppear('Tournament Date:');
        $this->iWaitForTextToAppear('(Optional) Number of Rounds:');
        $this->iWaitForTextToAppear('(Optional) Add Score Categories:');
    }
}
