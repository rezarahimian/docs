********************
Batch Overflow issue
********************

This vulnerability took place in April 2018 due to integer overflow exploit.
Some exchanges (like `OKEx <www.okex.com>`_) stopped deposits and withdrawals of ALL ERC20 tokens,
especially Beauty Ecosystem Coin (BEC) that was targeted by this exploit.
Attacker was able to pass values larger than the maximum value that can be held by ``uint256`` data type.
::
  contract overflowDemo { 

    uint256 public a = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;
    uint256 public b = 0x0000000000000000000000000000000000000000000000000000000000000001;
    uint256 public c;

    constructor() public {
        c = 0x3;
    }
    
    function a_plus_b_default() public{
        c = a + b;
    }
  } 

