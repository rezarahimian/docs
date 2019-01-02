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
    :scale: 90%
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
    :scale: 50%
    :figclass: align-center
    
    Figure 2: ERC20 multiple withdrawal attack

The assumption here is to prevent Bob from withdrawing Alice’s tokens multiple times. If he could withdraw N tokens after the initial Alice’s approval, this would be considered as a legitimate transfer since Alice already approved it (It is Alice’s responsibility to make sure before approving anything to Bob). So we are looking for a solution to prevent multiple withdrawal (N+M) by Bob assuming that Alice has more than N+M tokens in her wallet.
As part of ERC20 definition, two examples from `OpenZeppelin <https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol>`_ and `ConsenSys <https://github.com/ConsenSys/Tokens/blob/fdf687c69d998266a95f15216b1955a4965a0a6d/contracts/eip20/EIP20.sol>`_ are recommended by authors. *OpenZeppelin* implementation uses two additional methods that initially proposed by `MonolithDAO token <https://github.com/MonolithDAO/token/blob/master/src/Token.sol>`_ and ConsenSys has not attempted to work around the issue. There are other suggestions as well. Hence, we have to evaluate all suggested solutions in term of compatibly with the standard and mitigation against the attack.

Suggested solutions
*******************
Several solutions have been suggested by Ethereum community (mostly from developers on Github) to address this attack. These are some considerations for each suggested solution that we discuss them separately in term of compatibility and security:

1. Enforcement in User Interface (UI)
=====================================
ERC20 standard emphasises that:

.. figure:: images/multiple_withdrawal_03.png
    :scale: 80%
    :figclass: align-center
    
    Figure 3: Recommendation of ERC20 standard to mitigate multiple withdrawal attack

So, they recommend to enforce approval processing check in UI level. If someone do not use UI and connects directly to the blockchain, there would be good chance of impacting by this attack. Hence, enforcement should be considered at contract level not UI level. Additionally, There is no way to see from UI if ``Approve(_BobAddr, 0)`` transaction is processed before the subsequent non-zero approval :cite:`Ref03`. This is because of current API in Web3.js [#]_ that does not support such checking :cite:`Ref04`. So, we would not see this enforcement as a feasible solution to this attack.

2. Using minimum viable token
=============================
As suggested by :cite:`Ref05`, we can boil down ERC20 standard to a very basic functionalities by implementing only essential methods. In other words, by skipping implementation of vulnerable functions, effecting the attack would not be possible:

.. figure:: images/multiple_withdrawal_04.png
    :scale: 100%
    :figclass: align-center
    
    Figure 4: Minimum viable token implementation

While removing ``Approve`` and ``TransferFrom`` functions will prevent multiple withdrawal attack, it makes this token incompatible with expectation of ERC20 standards. These methods are not OPTIONAL and must be implemented as part of the standard ERC20 specifications. Moreover, ignoring them will cause failed function calls from standard wallets. So, we would not consider it as a compatible solution although mitigates the vulnerability.

3. Approving token transfer to verified smart contracts or trusted third-party
==============================================================================
Approving token transfer to non-upgradable smart contracts would be safe. Because they do not contain any logic to take advantage of this vulnerability. For example, the below contract uses ``transferFrom`` function to transfer approved amount of tokens to someone who agreed to pay equivalent in Ether. So, it will be safe to allow token transfer by this smart contract:

.. figure:: images/multiple_withdrawal_05.png
    :scale: 100%
    :figclass: align-center
    
    Figure 5: Verified code of a trusted smart contract before approving token transfers

However, upgradable smart contracts may add new logics to a new version that needs reverification before approving token transfer. Similarly, approving token transfer to people that we trust could be considered as a mitigation plan. Since this solution would have limited use cases, it could not be considered as a generic solution to the attack.

4. MiniMeToken implementation
`MiniMeToken <https://github.com/Giveth/minime/blob/master/contracts/MiniMeToken.sol#L225>`_ recommends to reduce allowance to zero before non-zero approval. As shown in the screenshot, the red clause in Approve method, allows to set approval to zero and blue condition checks allowance of ``_spender`` to be zero before setting to non-zero values (If ``_spender`` allowance is zero then allows non-zero values):

.. figure:: images/multiple_withdrawal_06.png
    :scale: 100%
    :figclass: align-center
    
    Figure 6: MiniMeToken suggestion for adding the above code to approve method

As discussed `here <https://github.com/OpenZeppelin/openzeppelin-solidity/issues/438#issuecomment-329172399>`_, this approach is not sufficient and allows Bob to transfer N+M tokens:

#. Bob is allowed to transfer N Alice's tokens.
#. Alice publishes transaction that changes Bob's allowance to zero.
#. Bob front runs Alice's transaction and transfers N Alice's tokens.
#. Alice's transaction is mined and Bob's allowance is now zero. This is exactly what she would see if Bob would not transfer any tokens, so she has no reason to think that Bob actually used his allowance before it was revoked.
#. Now Alice publishes transaction that changes Bob's allowance to M.
#. Alice's second transaction is mined, so now Bob is allowed to transfer M Alice's tokens
#. Bob transfers M Alice's tokens and in total N+M.

At step 3, Bob is able to transfer N tokens. This is a legitimate transaction since Alice already approved it. The issue will happen after Alice’s new transaction to set Bob’s approval to zero. In case of front-running by Bob, Alice needs to check Bob’s allowance for the second time before setting to the new value. Alice may notice this by checking Transfer event that logged by Bob. However, if Bob had transferred tokens to someone else, then Transfer event will not be linked to Bob, and, if Alice's account is busy and many people are allowed to transfer from it, Alice may not be able to distinguish this transfer from a legitimate one performed by someone else. So, this solution does not prevent the attack while tries to follow ERC20 recommendations for setting Bob’s allowance to zero before any non-zero value.

|
|
|

.. rubric:: Footnotes
.. [#] `JavaScript UI library <https://github.com/ethereum/wiki/wiki/JavaScript-API>`_ for interacting with Ethereum blockchain.

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
