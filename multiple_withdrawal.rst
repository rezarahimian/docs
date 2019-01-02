.. _multiple_withdrawal:

##########################
Multiple withdrawal attack
##########################

.. index:: ! Multiple withdrawal attack, double-spend exploit;

Description
***********
`ERC20 standard <https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md>`_ provides basic functionality to transfer tokens, as well as allowing tokens to be approved. so they can be spent by another third party (e.g., online exchanges, third-party payments, and quantitative fund management). Two functions in ERC20 standard support this functionality:

#. **Approve**: Allows ``_spender`` to withdraw up to the ``_value`` amount from approver’s token pool. If this function is called again it overwrites the current allowance with ``_value``.
#. **TransferFrom**: Transfers ``_value`` amount of tokens from address ``_from`` to address ``_to``. It allows accounts/wallets to transfer tokens on behalf of approver.

.. figure:: images/multiple_withdrawal_01.png
    :figclass: align-center
    
    Figure 1: Standard ERC20 Approve and transferFrom methodes
    
As explain by :cite:`Ref03`, these two functions could be used in multiple withdrawal attack that allows a spender to transfer more tokens than the owner of tokens ever wanted. This is possible because ``Approve`` method overrides current allowance regardless of whether spender already used it or not. Moreover, transferred tokens are not trackable and only ``Transfer`` event will be logged which is not sufficient in case of transferring tokens to a third parity. Here could be a possible attack scenario:

#. Alice allows Bob to transfer N tokens by calling ``Approve(_BobAddr, N)``.
#. After a while, Alice decides to change approval from N to M by calling ``Approve(_BobAddr, M)``.
#. Bob notices Alice's second transaction before it was mined and quickly sends another transaction that calls ``transferFrom(_AlicAddr, _BobAddr, N)``. This transfers N Alice's tokens to Bob.
#. Bob's transaction will be executed before Alice's transaction (because of higher transaction fee or miner’s policy) and Bob front-runs Alice's transaction.
#. Alice’s transaction will be executed after Bob’s and allows Bob to transfer more M tokens.
#. Bob successfully transferred N Alice's tokens and gains ability of transferring another M tokens.
#. Before Alice noticed that something went wrong, Bob calls ``transferFrom`` method again and transfers M Alice's tokens by calling ``transferFrom(_AlicAddr, _BobAddr, M)``.

In fact, Alice attempted to change Bob's allowance from N to M, but she made it possible for Bob to transfer N+M of her tokens at most, while Alice never wanted to allow so many transfers by Bob:

.. figure:: images/multiple_withdrawal_02.png
    :figclass: align-center
    
    Figure 2: ERC20 multiple withdrawal attack

The assumption here is to prevent Bob from withdrawing Alice’s tokens multiple times. If he could withdraw N tokens after the initial Alice’s approval, this would be considered as a legitimate transfer since Alice already approved it (It is Alice’s responsibility to make sure before approving anything to Bob). So we are looking for a solution to prevent multiple withdrawal (N+M) by Bob assuming that Alice has more than N+M tokens in her wallet.
As part of ERC20 definition, two examples from OpenZeppelin `<https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol>`_ and `ConsenSys <https://github.com/ConsenSys/Tokens/blob/fdf687c69d998266a95f15216b1955a4965a0a6d/contracts/eip20/EIP20.sol>`_ are recommended by authors. *OpenZeppelin* implementation uses two additional methods that initially proposed by `MonolithDAO token <https://github.com/MonolithDAO/token/blob/master/src/Token.sol>`_ and ConsenSys has not attempted to work around the issue. There are other suggestions as well. Hence, we have to evaluate all suggested solutions in term of compatibly with the standard and mitigation against the attack.

Suggested solutions
*******************
Several solutions have been suggested by Ethereum community (mostly from developers on Github) to address this attack. These are some considerations for each suggested solution that we discuss them separately in term of compatibility and security:

1. Enforcement in User Interface (UI)
=====================================
ERC20 standard emphasises that:

.. figure:: images/multiple_withdrawal_03.png
    :figclass: align-center
    
    Figure 3: Recommendation of ERC20 standard to mitigate multiple withdrawal attack

So, they recommend to enforce approval processing check in UI level. If someone do not use UI and connects directly to the blockchain, there would be good chance of impacting by this attack. Hence, enforcement should be considered at contract level not UI level. Additionally, There is no way to see from UI if ``Approve(_BobAddr, 0)`` transaction is processed before the subsequent non-zero approval :cite:`Ref03`. This is because of current API in Web3.js [#]_ that does not support such checking :cite:`Ref04`. So, we would not see this enforcement as a feasible solution to this attack.

|
|
|

----

.. rubric:: Footnotes
[#]. `JavaScript UI library <https://github.com/ethereum/wiki/wiki/JavaScript-API>`_ for interacting with Ethereum blockchain.

|
|
|

.. rubric:: References
.. bibliography:: references.bib
    :style: plain

|
|
|

----

:Date:    Dec 25, 2018
:Updated: |today|
:Authors: :ref:`about`
