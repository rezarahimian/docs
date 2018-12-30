*******************
batchOverflow issue
*******************

Description
###########
This vulnerability took place in April 22, 2018 due to a well known and common issue in many programming languages called `Integer overflow <https://en.wikipedia.org/wiki/Integer_overflow>`_. Some exchanges (like `OKEx <https://okex.com>`_, `Poloniex <https://poloniex.com/>`_ and `HitBTC <https://hitbtc.com/>`_) stopped deposits and withdrawals of ALL ERC20 tokens, especially for `Beauty Ecosystem Coin (BEC) <https://etherscan.io/address/0xc5d105e63711398af9bbff092d4b6769c82f793d>`_ that was targeted by this exploit. In this attack, someone was able to run a `transaction <https://etherscan.io/tx/0xad89ff16fd1ebe3a0a7cf4ed282302c06626c1af33221ebe0d3a470aba4a660f>`_ and transfer two extremely large amount of BEC token to two addresses. Although BEC developers had considered most of the security measurements, only one line of the code (line 257) was vulnerable against this classic integer overflow issue [1]:

.. figure:: images/batch_overflow_04.png
    :align: center
    :figclass: align-center
    
    Figure 1: Vulnerable code in BEC token, batchTransfer() function

Attacker was able to pass a combination of input values that generate large results than the maximum value of ``uint256`` data type. It caused integer overflow and only the least significant bits have been retained (`wrap around <https://en.wikipedia.org/wiki/Integer_overflow>`_). For example, a ``uint8`` variable can represent maximum value of ``(2^8)-1=255 (0xff)``. Multiplying ``0x02`` by ``0x80`` causes integer overflow and produces ``0x00`` as the result (``0x80 * 0x02 = 0x100 => 0x00``). We can achieve the same result by adding ``0x01`` to ``0xff`` (``0xff + 0x01 = 0x100 => 0x00``). So, attacker passed two addresses ( *_receivers.lengh* = ``0x02`` ) and a large value ( *_value* = ``0x8000000000000000000000000000000000000000000000000000000000000000`` (63 0's) ) to *batchTransfer()* function, the result of *amount* variable was calculated as ``0x00`` and this result bypassed sanity checks in lines 259 and 261. Hence, it transferred the specified amount (as specified *_value*) to those two addresses. This transfer was even more than totoal supply of the token.

In addition to BEC token, the following tokens are batchOverflow-affected:

1. UgChain
2. SMART
3. MTC
4. FirstCoin
5. GG Token
6. CNY Token
7. MESH
8. SMT tokens

Reproducing the issue
#####################
The same logic is applicable in solidity programming language and we tested for ``uint256`` data type as shown below:

.. figure:: images/batch_overflow_01.png
    :align: center
    :figclass: align-center
    
    Figure 1: Integer overflow demonstration in solidity
    
We initially set ``c=0x3`` to check its result before and after multiplication operation performed by *a_multiply_b()* function. On the left, we can see initial value of ``c`` before execution of the function and on the right, ``c`` has been set to zero due to wrap around.

.. figure:: images/batch_overflow_02.png
    :align: center
    :figclass: align-center
    
    Figure 2: Result of addition operation in case of integer overflow
    
Ethereum executes *a_multiply_b()* function in unchecked context and shows successful status by returning ``true`` as output:

.. figure:: images/batch_overflow_03.png
    :align: center
    :figclass: align-center
    
    Figure 3: By default, integer overflow does not throw a runtime exception in Ethereum

Although this is expected behavior in Ethereum, it causes security problems as explained in `CVE-2018–10299 <https://nvd.nist.gov/vuln/detail/CVE-2018-10299>`_

Recommendation
##############
Recommendation is always use SafeMath library when performing any arithmetic calculations. This library offered by `OpenZeppelin <https://github.com/OpenZeppelin/zeppelin-solidity/blob/master/contracts/math/SafeMath.sol>`_ and becomes industry standard for catching overflows. Additionally, auditing before launching the code will helps to be in compliance with best practices.

References
##########
.. [1] PeckShield, "New batchOverflow Bug in Multiple ERC20 Smart Contracts (CVE-2018–10299)," 22 4 2018. [Online]. Available: https://medium.com/@peckshield/alert-new-batchoverflow-bug-in-multiple-erc20-smart-contracts-cve-2018-10299-511067db6536 [Accessed 26 12 2018].

.. [2] M. Mulders, "Binance Hack Linked To Viacoin Pump (Official Update)," 7 3 2018. [Online]. Available: https://hackernoon.com/alleged-hack-of-binance-linked-to-viacoin-pump-bb9066bf96bf [Accessed 26 12 2018].
