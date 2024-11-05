# Connect4
Connect4 bot (without using RL) that plays using minimax algorithm and custom written evaluation function

The bot works by evaluating the state of the board using a specialised evaluation function (in engine.py) and doing an efficient (alpha beta pruned) search over the state space. The evaluation function is also memoized as many of the same board states come up during the search.

The bot performs very well considering the details of the evaluation function.
I intend on writing a version in C++, due to the static sizes of all the matrices used it makes sense to write the code in C++. This should provide runtime improvements which can be traded for deeper searches into the search tree.

Here's a picture of what the board should look like:

![alt text](https://github.com/ranjit002/Connect4/blob/main/imgs/board.png?raw=true)