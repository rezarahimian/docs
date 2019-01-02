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



|
|
|

----

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
