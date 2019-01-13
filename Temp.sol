
    function transferFrom(address _from, address _to, uint256 _tokens) public returns (bool success) {
        require(_to != address(0));
        require(balances[_from] >= _tokens);                // Checks if approver has enough tokens
        require(allowed[_from][msg.sender] >= _tokens);     // Checks allowance of the spender
        require(_tokens <= (
                            (allowed[_from][msg.sender] >= transferred[_from][msg.sender]) ? 
                             allowed[_from][msg.sender].sub(transferred[_from][msg.sender]) : 0)
                            );                              // Prevent token transfer more than allowance

        balances[_from] = balances[_from].sub(_tokens);
        transferred[_from][msg.sender] = transferred[_from][msg.sender].add(_tokens);
        balances[_to] = balances[_to].add(_tokens);
        emit Transfer(_from, _to, _tokens);
        return true;
    }