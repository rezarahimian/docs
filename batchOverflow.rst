********************
Batch Overflow issue
********************

This vulnerability took place in April 2018 due to integer overflow exploit. Some exchanges (like `OKEx <https://www.okex.com>`_) stopped deposits and withdrawals of ALL ERC20 tokens, especially `Beauty Ecosystem Coin (BEC) <https://etherscan.io/address/0xc5d105e63711398af9bbff092d4b6769c82f793d>`_ that was targeted by this exploit. Attacker was able to pass values larger than the maximum value that can be held by ``uint256`` data type. As result of integer overflow, only the least significant bits would be retained and effectively causing `wrap around <https://en.wikipedia.org/wiki/Integer_overflow>`_. For example, adding 0x01 to an ``uint8`` (8-bit unsigned integer) that can represent maximum value of ``2^8-1=255 (0xff)``, causes overflow and produces ``0x00`` as the result (0xff + 0x01 = 0x100 => 0x00). The same logic is applicable in solidity programming language and we tested for ``uint256`` data type as shown below:
.. image:: ../images/batch_overflow_01.png
    :align: center
    :alt: alternate text
