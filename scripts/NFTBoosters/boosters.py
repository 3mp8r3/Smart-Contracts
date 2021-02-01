import os
from brownie import accounts,network,SIGHBoosters


def main():
    return initiateSIGHBoosterContract()


def initiateSIGHBoosterContract():
    if network.show_active() == 'mainnet-fork' or  network.show_active()== 'development':
        return deployScript(accounts[0])
    elif network.show_active() == 'kovan':
        dev = accounts.add(os.getenv('PRIVATE_KEY'))
        return deployScript(dev)


def deployScript(account):
    boosters = SIGHBoosters.deploy('SIGH Boosters', '👽', {'from': account})

    # Update Boosters baseURI
    boosters._updateBaseURI('boosters.sigh.finance/',{'from':account})

    # Add Booster Types (Inspired from Hitchhicker's to the Galaxy)
    boosters.addNewBoosterType('Deep Thought', 0, 0, {'from': account})
    boosters.addNewBoosterType('Heart of Gold', 0, 0, {'from': account})
    boosters.addNewBoosterType('The Restaurant at the End of the Universe', 1, 5, {'from': account}) #100% , 20%
    boosters.addNewBoosterType('JARVIS', 2, 10, {'from': account})  #50% , 10%
    boosters.addNewBoosterType('MARVIN', 3, 20, {'from': account})  #33.3%, 5%

    #Add Boosters
    boosters.createNewBoosters(['Deep Thought','Heart of Gold','The Restaurant at the End of the Universe'],['dt/1','hg/1','r/1'], {'from': account})
    boosters.createNewBoosters(['JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS','JARVIS'],
                               ['jrvs/1','jrvs/2','jrvs/3','jrvs/4','jrvs/5','jrvs/6','jrvs/7','jrvs/8','jrvs/9','jrvs/10'],
                               {'from': account})
    boosters.createNewBoosters(['MARVIN','MARVIN','MARVIN','MARVIN','MARVIN'],
                               ['mrvn/1','mrvn/2','mrvn/3','mrvn/4','mrvn/5'],
                               {'from': account})
    return boosters

