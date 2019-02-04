.. _erc20_intro

############
Introduction
############

ERC20 [#]_ in Ethereum [#]_ ecosystem is a standard that allows representation of tangible assets as intangible instances. For example shares of company X can be represented as ERC20 tokens [#]_. This conversion makes it possible to trade or exchange them by other DApps [#]_. Leveraging ERC20 tokens facilitate implementation of left side of the below trading model on the Blockchain:

.. figure:: images/erc20_intro_01.png
    :scale: 60%
    :figclass: align-center
    
    *Figure 1: A blockchain trading model using ERC20 tokens*

The right side of the model needs a financial asset which is equivalent to a fiat currency (Like USD or CAD) [#]_. So, the value of it will be stable over time and people be able to count on its value. Stablecoins provide such functionalities in blockchain by pegging to something that has a stable value (Like gold or USD). There would be, essentially, three types of stablecoins :cite:`Ref09` that can be used:

#. **Fiat-collateralized:** It is backed by the equivalent fiat currency.
#. **Crypto-collateralized:** It uses other cryptocurrencies as collateral.
#. **Non-collateralized:** It is not backed by any collateral, similar to other fiat currencies that are maintained by governments.

Representation of stablecoin could be also as ERC20 tokens (For example named as CADT). Value of it comes from engaging parties of the exchange who agreed on the value (i.e., 1 CADT worths 1 $CAD). Assuming share of company X and fiat currency as ERC20 tokens, give two ERC20 tokens (with different values) to trade.

Besides tradability of ERC20 tokens as a financial property, they are technically standardized version of smart contracts :cite:`Ref08`. Similar to any other program, written codes could be vulnerable against security flaws. Some of these security vulnerabilities have been already discovered and handled by the Ethereum community. Here, we introduce a new solution to one of the open issues (:ref:`multiple_withdrawal`) to introduce a secure ERC20 code that could mitigate against all identified security vulnerabilities.

|
|
----

.. rubric:: Footnotes
.. [#] Technical standard used on the Ethereum blockchain for implementing tokens.
.. [#] Ethereum is a decentralized platform that runs distributed applications.
.. [#] A token can be considered as a virtual asset acts as fiat currency that has value to trade.
.. [#] Distributed applications (DApps) run on blockchain and synchronize data through consensus mechanism.
.. [#] Fiat currency (money) does not have any intrinsic value. Its value comes from public faith in the issuer (e.g., government who maintains it).

|
|
----

.. rubric:: References
.. bibliography:: references.bib
    :style: plain

|
|
----

:Date:    Dec 24, 2018
:Updated: |today|
:Authors: :ref:`about`

