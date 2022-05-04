const { assert } = require("chai")

const test = artifacts.require("SFPCODE_v1")

require("chai")
    .use(require("chai-as-promised"))
    .should()

contract("SFPCODE_v1", (accounts) => { //accounts from ganache

before(async () => { //get contract reference global
    contract = await test.deployed()
})
    describe("deployment", async () => {
        it("deploys successfully", async () => {
            const address =  contract.address
            assert.notEqual(address, 0x0)
            assert.notEqual(address, "")
            assert.notEqual(address, null)
            assert.notEqual(address, undefined)
        })
    }) 

    describe("Roles check", async () => {
        //check hasrole all to contract creator
        
        //check role all edit

        //reset all roles to creator

        //revoke roles

        //renounce roles


    }) 

    describe("Mint test", async () => {
        //mint one token to creator address

        //mint more token to creator address

        //mint batch token to creator address

        //mint one token to other address

        //mint more token to other address

        //mint batch token to creator address

    })

    describe("Transfer test", async () => {
        //transfer one token

        //transfer more token

        //transfer batch one token

        //transfer batch more token

    })

    describe("Approval test", async () => {
        //check account 2 not approved for transfer creator(account0) funds

        //Approve account 2 from creator(account0)

        //check approved

        //approved transfer test from creator address to account 1 using account 2

        //remove approve

        //try to transfer again and check failure


    })

    describe("Balances test", async () => {
        //check account 0 balance for all token

        //check account 1 balance for all token

        //check account 2 balance for all token

    })

    describe("Burn test", async () => {
        //burn one token to creator address
        
        //burn more token to creator address

        //burn batch token to creator address

        //burn one token to other address

        //burn more token to other address

        //burn batch token to creator address

    })

    describe("URI test", async () => {
        //read default URI

        //set new URI

        //read new URI

    })


    describe("Pause and Unpause", async () => {
        //pause contract

        //check transfer fail

        //unpause contract

    })

})