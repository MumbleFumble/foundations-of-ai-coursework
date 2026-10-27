[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DAU6jAlc)
# README

## Tell us about your implementation!
    two optimisation problems solved using CVXPY.

        For the portfolio optimization, I built a CVXPY model that maximizes expected return while keeping total portfolio risk under a limit. I computed expected returns as the final normalized stock prices and the covariance matrix using daily normalized prices. The optimization uses weights that sum to one and stay nonnegative, and the model adjusts automatically when I change the maximum allowed risk. The result shows how tighter risk constraints reduce investment in higher-variance stocks.

        For the energy planning model, I used Rhode Island’s wind, solar, and demand data to minimize total system cost while meeting hourly electricity demand. My decision variables include how much solar and wind capacity to build, how much battery and metal-air storage to purchase, and how much energy is charged, discharged, and stored each hour. I converted all energy units to megawatts during optimization for numerical stability, then back to kilowatts for output. The model ensures generation and storage together always meet demand and that storage never exceeds its capacity.




## Tell us about your tests!
    Ran 7 tests in 0.277s

    test_zero_demand_zero_cost:

        Verifies that if there is no demand at all, the model builds no generation or storage and the total cost is zero. Ensures no unnecessary investment occurs when there’s no energy need.

    test_constant_demand_balanced_generation

        Tests constant demand with both technologies available at all times but solar being cheaper.
        Expected outcome: Model selects only solar (10 kW built), no wind or storage, confirming cost minimization behavior.
    
    test_storage_always_required

        Constructs a scenario where generation and demand never overlap in time, energy is produced before demand occurs.
        Expected outcome: Storage capacity must be > 0, since energy must be shifted in time to meet late demand.
        Also verifies total cost and generation are both positive, confirming that storage is an essential part of the optimal solution.


## Answer the conceptual questions!
    Task 1:
        IMG_9733.jpeg
        IMG_9734.jpeg

    Task 2a:
        decision variables:

            how much money to invest in each stock, so from our set up: the vector w where w(i) is the proportion of your wealth invested in stock i.

            w = [w1,w2,....,wn]

        cost function:

            we want to maximize our expected return, we may also want some cost function for minimizing risk. But main it is about maximising total return. We can combine these objectives into a single function:

            expected return = u^(T) x w
            risk = Var = w^(T) x sigma w

            function: max [expected return]

            where R is the acceptable risk level


        constraints / s.t:

            Budget (weights sum to 1): 1^(T) x w = 1
            risk: w^(T) x sigma w <= R
            weights are non-negative

        constants:

            data given too us from the historical data, this includes all of the data that it gives to us but we are only using some of that data:

                . u(i): the average/mean return of stock i

                . the covariance between two stock i and j  as a matrix (sigma symbol)

                . and probably the constant for are appropriate risk, call that R

        
        max: expected return
        sunject to: total weights sum to 1
                    risk is less than max risk
                    weights are all >= 0



    Task 2d.
        at very low risk it will only buy one or two stock but will buy alot of them, I assume these are just risky stock but have the best returns. then the lower you get it starts to spread out then it will only buy the safest stock then it decides to buy no stock at all.

        diversifying doesn't "put all your eggs in one basket", it means if a given stock goes down, which can happen no matter how safe it is, you will lose alot unless your wealth is spread out. If its spread the damage of a loss is greatly reduced.

        Spotify, Jhonson & Jhonson, Southwest Airlines, 3M Company

        at 1e-5 it won't buy anything, its because every single possible stock for any amount of stock bought is too risky to fit this risk cutoff.


    Task 3a. 
        constants:
            fw – wind capacity factor at each hour (fraction of wind potential available)
            fs – solar capacity factor at each hour (fraction of solar potential available)
            D – electricity demand at each hour (kW)
            cw – cost of wind generation capacity ($/kW)
            cs – cost of solar generation capacity ($/kW)
            cb_cost – cost of Li-ion storage capacity ($/kWh)
            cm_cost – cost of metal-air storage capacity ($/kWh)
            nb – Li-ion charge efficiency (fraction of input energy stored successfully)
            nm – metal-air charge efficiency (fraction of input energy stored successfully)
            t – number of time steps (hours in the simulated year)

        the decision variables are how much of each source and battery to purchase, and the amount of energy stored in each battery type per hour:
            W - wind built
            S - solar built
            B - Li-ion batteries total capacity
            M - metal-air batteries capacity
            cb - energy charged into Li-ion / hour
            db - energy discharged into Li-ion / hour
            sb - energy stored after an hour in Li-ion
            cm - energy charged into Metal-air / hour
            dm - energy discharged into Metal-air / hour
            sm - energy stored after an hour in Metal-air

        objective function is to minimise the cost of the energy system which is cost of engery storage + energy generation:
            minimise (cw)(W) + (cs)(S) + (cb)(B) + (cm)(M)

        constraints:
            meet demand: (fw)(W) + (fs)(S) + (db) + (dm) >= D + cb + cm

            finding energy stored at hour t:    sb = sb-1 + (nb)(cb) - db
                                                sm = sm-1 + (nm)(cm) - dm

            dont store over max:    0 <= sb <= B
                                    0 <= sm <= M

            non-negative: W,S,B,M,cb,cm,db,dm,sb,sl >= 0

            I can see how if you had charge and discharge as not being seperate variables you might need to let charge be negative to show discharge but I dont have it that way in my model
            

    Task 3c.
        it all depends on if the new method is better, since we havent included much dependancy in our model so if a better sounce is added the current storage values would decrease and if it was worse theyw ould remain unchanged

        it would need the same variables as the other type of generations, hourly output and a cost. THen you would have to add it to the objective formula in the same way. Include it in all the balancing constraints and add a constaints where the sum of gas generation is less than or equal to 0.1 * total generation. then to have the cap change annually add another related function in the constraints to reduce gas by the given 5-10 each year.



## Hours taken: 12

AI Use Description:

You must acknowledge use here and submit transcript if AI was used for portions of the assignment