pragma solidity ^0.4.16;

contract pycoin_ico{

    // Maximum pycoins available for sale
    uint public max_pycoins = 1000000;

    // Introducing USD to pycoin conversion rate
    uint public usd_to_pycoins = 1000;

    // Introducing total no. of pycoins bought by investors
    uint public total_pycoins_bought = 0;

    // Mapping from invester's address to it's equity in pycoins and USD
    mapping(address => uint) equity_pycoins;
    mapping(address => uint) equity_usd;

    // Check if an investor can buy pycoins
    modifier can_buy_pycoins(uint usd_invested){
        require (usd_invested * usd_to_pycoins + total_pycoins_bought <= max_pycoins);
        _;
    }

    // Getting the equity in Pycoins of an investor
    function equity_in_pycoins(address investor) external constant returns (uint){
        return equity_pycoins[investor];
    }

    // Getting the equity in Pycoins of an investor
    function equity_in_usd(address investor) external constant returns (uint){
        return equity_usd[investor];
    }

    // Buying Pycoins
    function buy_pycoins(address investor, uint usd_invested) external
    can_buy_pycoins(usd_invested){
        uint pycoins_bought = usd_invested*usd_to_pycoins;
        equity_pycoins[investor] += pycoins_bought;
        equity_usd[investor] = equity_pycoins[investor] / 1000;
        total_pycoins_bought += pycoins_bought;
    }

    // Selling Pycoins
    function sell_pycoins(address investor, uint pycoins_sold) external{
        equity_pycoins[investor] -= pycoins_sold;
        equity_usd[investor] = equity_pycoins[investor] / 1000;
        total_pycoins_bought -= pycoins_sold;
    }
}