import pytest
import brownie
from brownie import MintableERC20,SIGHBoostersSale,SIGHBoosters, accounts,chain


@pytest.fixture
def _boostersSale():
    #SIGH BOOSTERS
    boosters = SIGHBoosters.deploy('SIGH Boosters', 'SB', {'from': accounts[0]})
    #Add new booster type
    boosters.addNewBoosterType('Deep Thought', 100, 5, {'from': accounts[0]})
    boosters.addNewBoosterType('Heart of Gold', 10, 5, {'from': accounts[0]})
    boosters.addNewBoosterType('The Restaurant at the End of the Universe', 5, 5, {'from': accounts[0]})
    boosters.addNewBoosterType('MARVIN', 100, 5, {'from': accounts[0]})
    boosters.addNewBoosterType('JARVIS', 50, 5, {'from': accounts[0]})
    #Create new boosters
    boosters.createNewBoosters(['Deep Thought','Heart of Gold','The Restaurant at the End of the Universe'],
                               ['dt/1','hg/1','r/1'], {'from': accounts[0]}) # 1 each
    boosters.createNewBoosters(['JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS'],
                               ['jrvs/1','jrvs/2','jrvs/3','jrvs/4','jrvs/5','jrvs/6','jrvs/7','jrvs/8','jrvs/9','jrvs/10'],
                               {'from': accounts[0]}) #10
    boosters.createNewBoosters(['JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS'],
                               ['jrvs/1','jrvs/2','jrvs/3','jrvs/4','jrvs/5','jrvs/6','jrvs/7','jrvs/8','jrvs/9','jrvs/10'],
                               {'from': accounts[0]}) #10
    boosters.createNewBoosters(['MARVIN','MARVIN','MARVIN','MARVIN','MARVIN','MARVIN','MARVIN','MARVIN','MARVIN','MARVIN'],
                               ['mrvn/1','mrvn/2','mrvn/3','mrvn/4','mrvn/5','mrvn/6','mrvn/7','mrvn/8','mrvn/9','mrvn/10'],
                               {'from': accounts[0]}) #10
    #update base URI
    boosters._updateBaseURI('boosters/sigh.finance/', {'from': accounts[0]})

    #SIGH BOOSTERS SALES CONTRACT
    boostersSale = SIGHBoostersSale.deploy(boosters.address, {'from': accounts[0]})
    wbtc =  MintableERC20.deploy('WBTC','WBTC',{'from':accounts[0]})
    boostersSale.updateAcceptedToken(wbtc.address,{'from':accounts[0]})

    return boosters, boostersSale,wbtc


def test_BoosterTransferToSalesContract(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    boosters.safeTransferFrom(accounts[0], boostersSale.address, 7, {'from':accounts[0]})
    assert boosters.ownerOfBooster(7) == boostersSale.address
    assert boostersSale.getCurrentFundsBalance() == boostersSale.getTokenBalance(wbtc.address)
    category =  boosters.getBoosterCategory(7)
    assert boostersSale.getBoosterSaleDetails(category) == (1,0,0)
    with brownie.reverts('SIGH Finance : Not a valid Booster Type'):
        boostersSale.getBoosterSaleDetails('testing')


def test_updatePrice(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    boosters.safeTransferFrom(accounts[0], boostersSale.address, 7, {'from':accounts[0]})
    assert boosters.ownerOfBooster(7) == boostersSale.address
    category =  boosters.getBoosterCategory(7)
    assert boostersSale.getBoosterSaleDetails(category) == (1,0,0)
    boostersSale.updateSalePrice('JARVIS',1000, {'from':accounts[0]})
    assert boostersSale.getBoosterSaleDetails(category) == (1, 1000, 0)
    with brownie.reverts('Invalid Type'):
        boostersSale.updateSalePrice('JAR_VIS',1000, {'from':accounts[0]})
    with brownie.reverts('Not yet initialized'):
        boostersSale.updateSalePrice('MARVIN',1000, {'from':accounts[0]})
    with brownie.reverts('Ownable: caller is not the owner'):
        boostersSale.updateSalePrice('JARVIS',1000, {'from':accounts[4]})


def test_updateTokenAccepted(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    wETH = MintableERC20.deploy('wETH', 'wETH', {'from': accounts[0]})
    boostersSale.updateAcceptedToken(wETH.address, {'from': accounts[0]})
    assert boostersSale.getTokenAccepted() == ('wETH',wETH.address)
    assert boostersSale.getCurrentFundsBalance() == boostersSale.getTokenBalance(wETH.address)
    with brownie.reverts('Invalid address'):
        boostersSale.updateAcceptedToken('0x0000000000000000000000000000000000000000', {'from': accounts[0]})
    with brownie.reverts('Ownable: caller is not the owner'):
        boostersSale.updateAcceptedToken(wETH.address, {'from': accounts[1]})


def test_buyBooster(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    boosters.safeTransferFrom(accounts[0], boostersSale.address, 1, {'from':accounts[0]})
    assert boosters.ownerOfBooster(1) == boostersSale.address
    category = boosters.getBoosterCategory(1)
    boostersSale.updateSalePrice(category,1000, {'from':accounts[0]})
    assert boostersSale.getBoosterSaleDetails(category) == (1, 1000, 0)
    wbtc.approve(boostersSale.address,1000000000000, {'from':accounts[0]})
    with brownie.reverts('ERC20: transfer amount exceeds balance'):
        boostersSale.buyBoosters(accounts[1],'Deep Thought',1,{'from': accounts[0]})
    wbtc.mint(1000000000, {'from': accounts[0]})
    boostersSale.buyBoosters(accounts[1], 'Deep Thought', 1, {'from': accounts[0]})
    assert boosters.ownerOfBooster(1) == accounts[1]
    assert boostersSale.getBoosterSaleDetails(category) == (0, 1000, 1)
    assert boostersSale.getCurrentFundsBalance() == 1000
    boostersSale.transferBalance(accounts[9],1000, {'from':accounts[0]})
    assert boostersSale.getCurrentFundsBalance() == 0
    assert wbtc.balanceOf(accounts[9]) == 1000
    with brownie.reverts('Invalid number of boosters'):
        boostersSale.buyBoosters(accounts[1], 'Deep Thought', 0, {'from': accounts[0]})
    with brownie.reverts('Invalid Booster Type'):
        boostersSale.buyBoosters(accounts[1], 'Deep_Thought', 1, {'from': accounts[0]})
    with brownie.reverts('Boosters not available'):
        boostersSale.buyBoosters(accounts[1], 'Deep Thought', 10, {'from': accounts[0]})


def test_transferBalance(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    boosters.safeTransferFrom(accounts[0], boostersSale.address, 1, {'from': accounts[0]})
    assert boosters.ownerOfBooster(1) == boostersSale.address
    category = boosters.getBoosterCategory(1)
    boostersSale.updateSalePrice(category, 1000, {'from': accounts[0]})
    assert boostersSale.getBoosterSaleDetails(category) == (1, 1000, 0)
    wbtc.approve(boostersSale.address, 1000000000000, {'from': accounts[0]})
    wbtc.mint(1000000000, {'from': accounts[0]})
    boostersSale.buyBoosters(accounts[1], 'Deep Thought', 1, {'from': accounts[0]})
    assert boosters.ownerOfBooster(1) == accounts[1]
    assert boostersSale.getCurrentFundsBalance() == 1000
    with brownie.reverts('Invalid amount'):
        boostersSale.transferBalance(accounts[9], 10000, {'from': accounts[0]})
    with brownie.reverts('Invalid address'):
        boostersSale.transferBalance('0x0000000000000000000000000000000000000000', 10000, {'from': accounts[0]})


def test_transferTokens(_boostersSale):
    boosters, boostersSale, wbtc = _boostersSale
    wTest = MintableERC20.deploy('wTest', 'wTest', {'from': accounts[0]})
    wTest.mint(1000000000, {'from': accounts[0]})
    wTest.transfer(boostersSale.address,1000, {'from': accounts[0]})
    assert wTest.balanceOf(boostersSale.address) == 1000
    assert wTest.balanceOf(boostersSale.address) == boostersSale.getTokenBalance(wTest.address)
    boostersSale.transferTokens(wTest.address,accounts[4],10, {'from': accounts[0]})
    assert wTest.balanceOf(accounts[4]) == 10
    assert wTest.balanceOf(boostersSale.address) == boostersSale.getTokenBalance(wTest.address)
    assert boostersSale.getTokenBalance(wTest.address) == 990
    with brownie.reverts("Invalid address"):
        boostersSale.transferTokens(wTest.address,'0x0000000000000000000000000000000000000000', 1, {'from': accounts[0]})
    with brownie.reverts("Invalid amount"):
        boostersSale.transferTokens(wTest.address,accounts[3], 10000000, {'from': accounts[0]})











