[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/KB1woPx3)
# README

## Tell us about your implementation!
    Implementation of a monte carlo tester to test certain policies for a markovian problem. policies being different ways to move from state to state in a simplified game of black jack. the methods for gathering policies were:
        .Always stand
        .Value Iteration
        .Q learning 
    the last two options here use Q values to try and predict the best action for a given state, to maximise reward (win rate). At the end is the answer to some conceptual questions about how to move to a full version covering th emore compllicated full version of blackjack.

## Answer the conceptual questions!
### Part 1
    1. since the player has stood on 19 this is just the probability of the dealer being able to get each vale from a fixed 16 (no ace). No matter what card the dealer draws they can only draw one more so we look at the probability of getting each value between 17 and 27 and seeing whta they corrispond to - w/l/d. Values the dealer can draw are as follows:
        1 - win
        2 - win
        3 - draw
        4 - lose
        5 - lose
        6 to 10 - win
        13 cards total so:
        P(win) = 10/13
        P(draw) = 1/13
        P(lose) = 2/13

    2. same rules and situation except dealers total is 15, so if they draw an ace they draw again.
        1 - prob from Q1
        2 - win
        3 - win
        4 - draw
        5 - lose
        6 - lose
        7 to 10 - win
        P(win) = 9/13 + 1/13(Q1. P(win)) = 10/13
        P(draw) = 1/13 + 1/13(1/13) = 14/169
        P(lose) = 2/13 + 1/13(2/13) = 28/169

    3. same strategy as Q2,
        1 - prob from Q2
        2 - prob from Q1
        3 - win
        4 - win
        5 - draw
        6 - lose
        7 - lose
        8 to 10 - win
        P(win) = 8/13 + (1/13)(10/13) + (1/13)(10/13) = 10/13
        P(draw) = 1/13 +(1/13)(above) + (1/13)(Q1) = 196/2197
        P(lose) = 2/13 + (1/13)(Q2) + (1/13)(Q1) = 392/2197

    4. optimal value function, w/d/l = 1/0/-1. policy (pi) = 
    P(win)(at state s) - P(lose)(at state s)
    so the best possible value is achieved with the function,

        optimal = max(P(win | s) - P(lose | s))
    

### Part 5
    adding the problem of betting and money would greatly increase your state space. Alot of extra info would have to be added to each state, some kind of boolean to if the cards were of the same type; everry payout would have to chck to see if the winner had an inital 21 with an unused ace; and worst of all would be trying to deal with the fact that games aren't independant and effect what cards are left in the deck. 

    the action set also expands, you need to add in if they will bet double or split.This increase porcessing required by a huge factor again. the whole system of the Reward function changes as now it's about money earn't not just winning or losing. not to mention if oyu have a split that mean each hand has its own functions to go through. 

    Q-learning is still preferable but it will take muhc longer and be a much much more complicted algorithm.


    Card Counting.

        1. To model card counting in the MDP, you'd have to add a count variable to each state that summarizes the balance of high versus low cards. The new state would include the player’s total, whether the player has a usable ace, the dealer’s upcard, and the current count. Each time a card is drawn, the count would increase by 1 for small cards (2–6) and decrease by 1 for high cards (10–A). The reward structure and actions would stay the same as before, but transitions would now also update the count after each revealed card.

        2. This modified problem does not really satisfy the Markov property, since multiple exact deck compositions can produce the same count value but imply slightly different next-card probabilities. However, if we treat the count as the only relevant summary of past cards and define transitions using it, then the process is close to Markov within this simplified model.

        3. Q-Learning would be easier, Value Iteration requires exact transition probabilities P(next_state|action, state), which are hard to calculate when the next-card distribution depends on an approximate count. Q-Learning, on the other hand, learns optimal behavior directly from simulated episodes without needing those probabilities.

        4. The full deck-composition policy would perform better than the count-based policy, it uses complete information about which cards remain in the shoe. The count-based policy loses detail and can only approximate those probabilities. In Monte Carlo simulations, the full-state policy would achieve a higher win rate, while the count-based policy would still perform better than basic strategy but slightly below the true optimal level.
         





## Hours taken: 8 

## Collaborators: N/A

## Known Bugs: N/A

AI Use Description:

You must acknowledge use here and submit transcript if AI was used for portions of the assignment