import pytest
import brownie
from brownie import SIGHBoosters, accounts


@pytest.fixture
def boosters():
    boosters = SIGHBoosters.deploy('SIGH Boosters', 'SB', {'from': accounts[0]})
    boosters._updateBaseURI('boosters/sigh.finance/', {'from': accounts[0]})
    boosters.addNewBoosterType('Marvin', 100, 5, {'from': accounts[0]})
    return boosters


def test_deploy(boosters):
    assert boosters.name() == 'SIGH Boosters'
    assert boosters.symbol() == 'SB'
    assert boosters.owner() == accounts[0]


def test_supportsInterface(boosters):
    assert boosters.supportsInterface('0x01ffc9a7') == True  # _INTERFACE_ID_ERC165
    assert boosters.supportsInterface('0x80ac58cd') == True  # _INTERFACE_ID_ERC721
    assert boosters.supportsInterface('0x5b5e139f') == True  # _INTERFACE_ID_ERC721_METADATA
    assert boosters.supportsInterface('0x780e9d63') == True  # _INTERFACE_ID_ERC721_ENUMERABLE
    assert boosters.supportsInterface('0xffffffff') == False  # invalid interface id
    assert boosters.supportsInterface('0x150b7a02') == False  # _ERC721_RECEIVED


def test_callChecks(boosters):
    with brownie.reverts("BOOSTERS: Type doesn't exist"):
        boosters.getDiscountRatiosForBoosterCategory('Jarvis')



def test_addNewBoosterType(boosters):
    boosters.addNewBoosterType('Jarvis', 100, 5, {'from': accounts[0]})
    assert boosters.isCategorySupported('Jarvis') == True
    assert boosters.totalBoostersAvailable('Jarvis') == 0
    assert boosters.getAllBoosterTypes() == ['Marvin','Jarvis']
    assert boosters.getDiscountRatiosForBoosterCategory('Jarvis') == (100, 5)
    with brownie.reverts('Ownable: caller is not the owner'):
        boosters.addNewBoosterType('Jarvis', 150, 5, {'from': accounts[4]})


def test_updateBaseURI(boosters):
    boosters._updateBaseURI('testboosters/sigh.finance/', {'from': accounts[0]})
    assert boosters.baseURI() == 'testboosters/sigh.finance/'
    with brownie.reverts('Ownable: caller is not the owner'):
        boosters._updateBaseURI('boosters/sigh.finance', {'from': accounts[2]})


def test_updateBoosterURI(boosters):
    boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin','Marvin'],['mrvn/1', 'mrvn/2', 'mrvn/3','mrvn/3'], {'from': accounts[0]})
    boosters.updateBoosterURI(1,'ut/1', {'from': accounts[0]})
    assert boosters.tokenURI(1) == 'boosters/sigh.finance/ut/1'
    with brownie.reverts("Non-existent Booster"):
        boosters.updateBoosterURI(1888,'ut/1', {'from': accounts[0]})
    boosters.updateBoosterURI(1,'', {'from': accounts[0]})
    assert boosters.tokenURI(1) == 'boosters/sigh.finance/1'
    boosters._updateBaseURI('', {'from': accounts[0]})
    boosters.updateBoosterURI(1,'ut/1', {'from': accounts[0]})
    assert boosters.tokenURI(1) == 'ut/1'
    boosters.updateBoosterURI(1,'', {'from': accounts[0]})
    assert boosters.tokenURI(1) == '1'


def test_addNewBooster(boosters):
    boosters.createNewSIGHBooster(accounts[0],'Marvin','m/1','', {'from': accounts[0]})
    assert boosters.balanceOf(accounts[0]) == 1
    assert boosters.totalSupply() == 1
    assert boosters.tokenOfOwnerByIndex(accounts[0],0) == 1
    assert boosters.tokenByIndex(0) == 1
    assert boosters.ownerOf(1) == accounts[0]
    assert boosters.ownerOfBooster(1) == accounts[0]
    assert boosters.tokenURI(1) == 'boosters/sigh.finance/m/1'
    assert boosters.getApproved(1) == '0x0000000000000000000000000000000000000000'
    assert boosters.totalBoostersAvailable('Marvin') == 1
    assert boosters.totalBoostersOwnedOfType(accounts[0],'Marvin') == 1
    assert boosters.isValidBooster(1) == True
    assert boosters.getBoosterCategory(1) == 'Marvin'
    assert boosters.getDiscountRatiosForBooster(1) == boosters.getDiscountRatiosForBoosterCategory('Marvin')
    assert boosters.getBoosterInfo(1) == (accounts[0],'Marvin',100,5)
    with brownie.reverts('Ownable: caller is not the owner'):
        boosters.createNewSIGHBooster(accounts[0],'Marvin','m/1','', {'from': accounts[4]})
    with brownie.reverts('Not a valid Type'):
        boosters.createNewSIGHBooster(accounts[0],'Ma_rvin','m/1','', {'from': accounts[0]})


def test_addNewBoosters(boosters):
    boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin','Marvin'],['mrvn/1', 'mrvn/2', 'mrvn/3','mrvn/3'], {'from': accounts[0]})
    assert boosters.totalBoostersAvailable('Marvin') == 4
    assert boosters.totalSupply() == 4
    assert boosters.totalBoostersOwnedOfType(accounts[0],'Marvin') == 4
    assert boosters.isValidBooster(4) == True
    assert boosters.balanceOf(accounts[0]) == 4
    assert boosters.tokenOfOwnerByIndex(accounts[0],1) == 2
    assert boosters.tokenURI(1) == 'boosters/sigh.finance/mrvn/1'
    assert boosters.tokenByIndex(0) == 1
    assert boosters.ownerOfBooster(1) == accounts[0]
    assert boosters.getApproved(1) == '0x0000000000000000000000000000000000000000'
    assert boosters.getBoosterCategory(3) == 'Marvin'
    assert boosters.getDiscountRatiosForBooster(3) == boosters.getDiscountRatiosForBoosterCategory('Marvin')
    assert boosters.getBoosterInfo(4) == (accounts[0],'Marvin',100,5)
    with brownie.reverts('Size not equal'):
        boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin'], ['mrvn/1', 'mrvn/2'], {'from': accounts[0]})
    with brownie.reverts('Size not equal'):
        boosters.createNewBoosters(['Marvin'], ['mrvn/1', 'mrvn/2'], {'from': accounts[0]})
    with brownie.reverts('Not a valid Type'):
        boosters.createNewBoosters(['Marv_in'],['m/1'], {'from': accounts[0]})
    with brownie.reverts('Ownable: caller is not the owner'):
        boosters.createNewBoosters(['Marvin'],['m/1'], {'from': accounts[2]})


def test_updateDiscountMultiplier(boosters):
    boosters.updateDiscountMultiplier('Marvin',1,1, {'from': accounts[0]})
    assert boosters.getDiscountRatiosForBoosterCategory('Marvin') == (1,1)
    boosters.createNewSIGHBooster(accounts[0],'Marvin','m/1','', {'from': accounts[0]})
    assert boosters.getDiscountRatiosForBooster(1) == (1,1)
    with brownie.reverts("BOOSTERS: Type doesn't exist"):
        boosters.updateDiscountMultiplier('Marvi9n',1,1, {'from': accounts[0]})
    with brownie.reverts('BOOSTERS: Platform Fee Discount cannot be 0'):
        boosters.updateDiscountMultiplier('Marvin',0,1, {'from': accounts[0]})
    with brownie.reverts('BOOSTERS: SIGH Pay Fee Discount cannot be 0'):
        boosters.updateDiscountMultiplier('Marvin',1,0, {'from': accounts[0]})
    with brownie.reverts('Ownable: caller is not the owner'):
        boosters.updateDiscountMultiplier('Marvin',1,1, {'from': accounts[1]})


def test_safeTransferFrom(boosters):
    boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin','Marvin'],['mrvn/1', 'mrvn/2', 'mrvn/3','mrvn/3'], {'from': accounts[0]})
    boosters.safeTransferFrom(accounts[0],accounts[1],1, {'from': accounts[0]})
    assert boosters.ownerOfBooster(1) == accounts[1]
    assert boosters.balanceOf(accounts[1]) == 1
    assert boosters.getBoosterInfo(1)[0] == accounts[1]
    with brownie.reverts("Non-existent Booster"):
        boosters.safeTransferFrom(accounts[0],accounts[1],155, {'from': accounts[0]})
    with brownie.reverts("BOOSTERS: Neither owner nor approved"):
        boosters.safeTransferFrom(accounts[4],accounts[1],1, {'from': accounts[0]})
    with brownie.reverts("BOOSTERS: Neither owner nor approved"):
        boosters.safeTransferFrom(accounts[0],accounts[1],1, {'from': accounts[4]})
    boosters.blackListBooster(2,{'from': accounts[0]})
    assert boosters.isBlacklisted(2) == True
    with brownie.reverts("Booster blacklisted"):
        boosters.safeTransferFrom(accounts[0], accounts[5], 2, {'from': accounts[0]})
    boosters.whiteListBooster(2,{'from': accounts[0]})
    assert boosters.isBlacklisted(2) == False


def test_transferByApproved(boosters):
    boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin','Marvin'],['mrvn/1', 'mrvn/2', 'mrvn/3','mrvn/3'], {'from': accounts[0]})
    boosters.approve(accounts[1],1, {'from': accounts[0]})
    assert boosters.getApproved(1) == accounts[1]
    boosters.safeTransferFrom(accounts[0], accounts[5], 1, {'from': accounts[1]})
    assert boosters.ownerOfBooster(1) == accounts[5]
    assert boosters.balanceOf(accounts[5]) == 1
    assert boosters.getBoosterInfo(1)[0] == accounts[5]
    with brownie.reverts("BOOSTERS: Owner cannot be approved"):
        boosters.approve(accounts[0],2, {'from': accounts[0]})
    with brownie.reverts("BOOSTERS: Neither owner nor approved"):
        boosters.approve(accounts[4],2, {'from': accounts[1]})
    boosters.approve(accounts[1],2, {'from': accounts[0]})
    boosters.blackListBooster(2,{'from': accounts[0]})
    assert boosters.isBlacklisted(2) == True
    with brownie.reverts("Booster blacklisted"):
        boosters.safeTransferFrom(accounts[0], accounts[5], 2, {'from': accounts[1]})


def test_setApprovalForAll(boosters):
    boosters.createNewBoosters(['Marvin', 'Marvin', 'Marvin','Marvin'],['mrvn/1', 'mrvn/2', 'mrvn/3','mrvn/3'], {'from': accounts[0]})
    boosters.setApprovalForAll(accounts[1],1, {'from': accounts[0]})
    assert boosters.isApprovedForAll(accounts[0],accounts[1]) == True
    boosters.safeTransferFrom(accounts[0], accounts[4], 2,'', {'from': accounts[1]})
    assert boosters.ownerOfBooster(2) == accounts[4]
    assert boosters.getBoosterInfo(2)[0] == accounts[4]
    boosters.approve(accounts[2],1, {'from': accounts[1]})
    assert boosters.getApproved(1) == accounts[2]
    boosters.safeTransferFrom(accounts[0], accounts[3],1,'', {'from': accounts[1]})
    assert boosters.ownerOfBooster(1) == accounts[3]
    boosters.setApprovalForAll(accounts[1],0, {'from': accounts[0]})
    assert boosters.isApprovedForAll(accounts[0],accounts[1]) == False
    with brownie.reverts("BOOSTERS: Caller cannot be Approved"):
        boosters.setApprovalForAll(accounts[0],1, {'from': accounts[0]})


def test_Ownership(boosters):
    boosters.transferOwnership(accounts[7],{'from':accounts[0]})
    assert boosters.owner() == accounts[7]
    boosters.renounceOwnership({'from':accounts[7]})
    assert boosters.owner() == '0x0000000000000000000000000000000000000000'

