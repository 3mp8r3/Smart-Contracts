import os
from brownie import Contract,accounts,network,GlobalAddressesProvider,SIGH, SIGHSpeedController,SIGHVolatilityHarvester,SIGHFinanceConfigurator
from brownie import FeeProvider, LendingRateOracle, LendingPoolLiquidationManager, LendingPoolConfigurator,GenericLogic,ValidationLogic,InstrumentReserveLogic, LendingPool
from brownie import MockProxyPriceProvider, ChainlinkProxyPriceProvider,MintableERC20, DefaultInstrumenteInterestRateStrategy
from brownie import SIGH_PAY_Aggregator, SIGH_Fee_Collector,IToken,StableDebtToken,VariableDebtToken, SIGHHarvester

def main():
    return deploySIGHFinance()


def deploySIGHFinance():
    if network.show_active() == 'mainnet-fork' or  network.show_active()== 'development':
        return deployScript(accounts[0])
    elif network.show_active() == 'kovan':
        dev = accounts.add(os.getenv('PRIVATE_KEY'))
        return deployScript(dev)


def deployScript(account):
    globalAddressesProvider = GlobalAddressesProvider.deploy(account, account, {'from': account}) #SIGH Finance Manager, Lending Pool Manager

    # SIGH CONTRACTS
    SIGH_ = SIGH.deploy({'from':account})
    globalAddressesProvider.setSIGHAddress(SIGH_.address,{'from':account})

    SIGHspeedController_ = SIGHSpeedController.deploy({'from':account})
    globalAddressesProvider.setSIGHSpeedController(SIGHspeedController_.address,{'from':account})

    SIGHVolatilityHarvester_ = SIGHVolatilityHarvester.deploy({'from':account})
    globalAddressesProvider.setSIGHVolatilityHarvesterImpl(SIGHVolatilityHarvester_.address,{'from':account})

    SighFinanceConfigurator_ = SIGHFinanceConfigurator.deploy({'from':account})
    globalAddressesProvider.setSIGHFinanceConfiguratorImpl(SighFinanceConfigurator_.address,{'from':account})

    # LENDING PROTOCOL CONTRACTS
    FeeProvider_ = FeeProvider.deploy({'from':account})
    globalAddressesProvider.setFeeProviderImpl(FeeProvider_.address,{'from':account})

    LendingRateOracle_ = LendingRateOracle.deploy(globalAddressesProvider.address, {'from': account})
    globalAddressesProvider.setLendingRateOracle(LendingRateOracle_.address, {'from': account})

    LendingPoolLiquidationManager_ = LendingPoolLiquidationManager.deploy(globalAddressesProvider.address,{'from': account})
    globalAddressesProvider.setLendingPoolLiqAndLoanManager(LendingPoolLiquidationManager_.address, {'from': account})

    genericLogic_ = GenericLogic.deploy({'from': account})
    validationLogic_ = ValidationLogic.deploy({'from': account})
    instrumentReserveLogic_ = InstrumentReserveLogic.deploy({'from': account})

    LendingPool_ = LendingPool.deploy({'from': account})
    globalAddressesProvider.setLendingPoolImpl(LendingPool_.address, {'from': account})

    LendingPoolConfigurator_ = LendingPoolConfigurator.deploy({'from': account})
    globalAddressesProvider.setLendingPoolConfiguratorImpl(LendingPoolConfigurator_.address, {'from': account})

    #refresh configuration (SIGH Volatility harvester)
    sfConfiguratorAddress = globalAddressesProvider.getSIGHFinanceConfigurator()
    sfConfigurator = Contract.from_abi('sfConfigurator', sfConfiguratorAddress, SIGHFinanceConfigurator.abi)
    sfConfigurator.refreshSIGHVolatilityHarvesterConfig({'from': account})

    #refresh configuration (Lending Pool)
    lpConfiguratorAddress = globalAddressesProvider.getLendingPoolConfigurator()
    lpConfigurator = Contract.from_abi('lpConfigurator', lpConfiguratorAddress, LendingPoolConfigurator.abi)
    lpConfigurator.refreshLendingPoolConfiguration({'from': account})

    lpStorageAddress = globalAddressesProvider.getLendingPool()


    return globalAddressesProvider, sfConfigurator, lpConfigurator

    #Price oracle
    # priceOracle = []
    # if network.show_active() == 'mainnet-fork' or  network.show_active() == 'development':
    #     priceOracle = MockProxyPriceProvider.deploy(globalAddressesProvider.address,{'from': account})
    # elif network.show_active() == 'kovan':
    #     priceOracle = ChainlinkProxyPriceProvider.deploy(globalAddressesProvider.address,{'from': account})
    #
    # globalAddressesProvider.setPriceOracle(priceOracle.address,{'from': account})
    #
    # # SIGH PAY Aggregator & SIGH Fee Collector
    # SIGH_PAY_Aggregator_ = SIGH_PAY_Aggregator.deploy({'from': account})
    # globalAddressesProvider.setSIGHPAYAggregator(SIGH_PAY_Aggregator_.address,{'from': account})
    #
    # SIGH_Fee_Collector_ = SIGH_Fee_Collector.deploy(globalAddressesProvider.address,{'from': account})
    # globalAddressesProvider.setSIGHFinanceFeeCollector(SIGH_Fee_Collector_.address,{'from': account})


def initializeSIGH(globalAddressesProvider,account):
    SIGH_ = globalAddressesProvider.getSIGHAddress()
    SIGHSpeedController_ = globalAddressesProvider.getSIGHSpeedController()
    SIGHVolatilityHarvester_ = globalAddressesProvider.getSIGHVolatilityHarvester()
    SIGHFinanceConfigurator_ = globalAddressesProvider.getSIGHFinanceConfigurator()

    # initialize SIGH Contracts
    SIGH(SIGH_).initMinting(globalAddressesProvider.address,SIGHSpeedController_,{'from': account})
    SIGHSpeedController(SIGHSpeedController_).beginDripping(SIGHVolatilityHarvester_,{'from': account})
    SIGHVolatilityHarvester(SIGHVolatilityHarvester_).refreshConfig({'from': account})


# def initializeLendingProtocol(globalAddressesProvider,account):

def addAMarket(globalAddressesProvider,account):
    wbtc = MintableERC20.deploy('Wrapped Bitcoin', 'WBTC', {'from': account})

    lpConfiguratorAddress = globalAddressesProvider.getLendingPoolConfigurator()
    lpConfigurator = Contract.from_abi('lpConfigurator', lpConfiguratorAddress, LendingPoolConfigurator.abi)

    lpStorageAddress = globalAddressesProvider.getLendingPool()
    lendingPool_ = Contract.from_abi('lendingPool_', lpStorageAddress, LendingPool.abi)

    i_tokenImpl = IToken.deploy(globalAddressesProvider.address, lpStorageAddress, wbtc.address, 'CROP:I-WBTC', 'I-WBTC', {'from': account})
    s_tokenImpl = StableDebtToken.deploy(globalAddressesProvider.address, lpStorageAddress, wbtc.address, 'CROP:S-WBTC', 'S-WBTC', {'from': account})
    v_tokenImpl = VariableDebtToken.deploy(globalAddressesProvider.address, lpStorageAddress, wbtc.address, 'CROP:V-WBTC', 'V-WBTC', {'from': account})
    sighHarvesterImpl = SIGHHarvester.deploy({'from': account})
    interestRateStrategy_ = DefaultInstrumenteInterestRateStrategy.deploy(globalAddressesProvider.address,8e26,1e25,7e25,15e26,6e25,15e26, {'from': account})

    lpConfigurator.initInstrument(i_tokenImpl.address,s_tokenImpl.address,v_tokenImpl.address,sighHarvesterImpl.address,18,interestRateStrategy_.address,{'from':account})

def initSIGHMinting(globalAddressesProvider,account):
    #Initiaite SIGH minting
    sighAddress = globalAddressesProvider.getSIGHAddress()
    SIGH_ = Contract.from_abi('SIGH_', sighAddress, SIGH.abi)
    speedControllerAddress = globalAddressesProvider.getSIGHSpeedController()
    SIGH_.initMinting(globalAddressesProvider.address, speedControllerAddress, {'from': account})

    # Initiate dripping from speed controller to Volatility Harvester
    sfConfiguratorAddress = globalAddressesProvider.getSIGHFinanceConfigurator()
    sfConfigurator = Contract.from_abi('sfConfigurator', sfConfiguratorAddress, SIGHFinanceConfigurator.abi)
    sfConfigurator.beginDrippingFromSIGHSpeedController({'from':account})

    #Update SIGH distribution speed from SIGH SPEED CONTROLLER to VOLATILITY HARVESTER
    sfConfigurator.updateSighVolatilityDistributionSpeedInSIGHSpeedController(10000000, {'from': account})

speedController_ = Contract.from_abi('speedController_', speedControllerAddress, SIGHSpeedController.abi)

