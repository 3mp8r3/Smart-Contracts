import os
from brownie import accounts,network,SIGHBoostersSale,MintableERC20
from scripts.NFTBoosters import boosters


def main():
    return initializeSIGHBoostersSalesContract()


def initializeSIGHBoostersSalesContract():
    boosterContract = boosters.initiateSIGHBoosterContract()   # FIRST INITIALIZE THE SIGH BOOSTERS CONTRACT
    if network.show_active() == 'mainnet-fork' or  network.show_active()== 'development':
        return deployScript(boosterContract,accounts[0])
    elif network.show_active() == 'kovan':
        dev = accounts.add(os.getenv('PRIVATE_KEY'))
        return deployScript(boosterContract,dev)


def deployScript(boosterContract,account):
    # Initializing basic state
    boostersSale = SIGHBoostersSale.deploy(boosterContract.address, {'from': account})
    DAI = MintableERC20.deploy('DAI', 'DAI', {'from': account})
    boostersSale.updateAcceptedToken(DAI.address,{'from':account})
    # Sending some Boosters
    boosterContract.safeTransferFrom(account, boostersSale.address, 1, {'from':account})
    boostersSale.updateSalePrice('Deep Thought', 42000000000000000000000000, {'from': account})

    boosterContract.safeTransferFrom(account, boostersSale.address, 2, {'from':account})
    boostersSale.updateSalePrice('Heart of Gold', 24000000000000000000000000, {'from': account})

    boosterContract.safeTransferFrom(account, boostersSale.address, 3, {'from':account})
    boostersSale.updateSalePrice('The Restaurant at the End of the Universe', 11000000000000000000000000, {'from': account})

    boosterContract.safeTransferFrom(account, boostersSale.address, 4, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 5, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 6, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 7, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 8, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 9, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 10, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 11, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 12, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 13, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 14, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 15, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 16, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 17, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 18, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 19, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 20, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 21, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 22, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 23, {'from':account})
    boostersSale.updateSalePrice('JARVIS', 1000000000000000000000, {'from': account})

    boosterContract.safeTransferFrom(account, boostersSale.address, 14, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 15, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 16, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 17, {'from':account})
    boosterContract.safeTransferFrom(account, boostersSale.address, 18, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 24, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 25, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 26, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 27, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 28, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 29, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 30, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 31, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 32, {'from':account})
    # boosterContract.safeTransferFrom(account, boostersSale.address, 33, {'from':account})
    boostersSale.updateSalePrice('MARVIN', 500000000000000000000, {'from': account})

    return DAI,boosterContract,boostersSale
