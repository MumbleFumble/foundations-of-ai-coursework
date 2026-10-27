[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/u1oODY1i)
# README

## Tell us about your implementation!

    LinearRegression, PolynomialRegression, and RidgeRegression. Added single_feature_regression to fit one feature at a time, plot the line, and report train/test MSE. Updated correlation code so life_expectancy is included to help pick features.

## Tell us about your tests!

## Answer the conceptual questions!
    Task.1.3.
        a. there is a pretty strong negative correlation between number of years in school and adult mortalility rates. This is suprising as you would think the better the education the more likely someone is to live a safe life and live a long time. My guess is that if they have alot of school its a developed country meaning more people make it to adulthood i.e. more deaths.

        b. Another interesting one is GDP and percentage expenditure. Becuase the percentage expenditure shows that the more money a country has the larger PERCENT of that money is spent on health. showing that if you are a poorer country you don't jsut spend less money but also spend less of a percentage, showing it as a lower priority.

        c. lastly would be the relation between alcohol consumption and percentage expenditure on healthcare. showing that for countries that drink more they spend more money on healthcare. This is interesting since countries that don't have the money for alot of alcohol also spend less of that money on healthcare. Although, I would say this also points to the fact that richer countries drink more if you combine it with the relationship in b.

    Task.1.4.

        a. Single Feature Regression using Schooling
        Train MSE: 26.155990022484694
        Test MSE: 31.069430087876466
        Visually it is a pretty clear upward slope with tight grouping round the middle, no dot varys very far from the line except ones at lower end of both features

        b. Single Feature Regression using Adult_Mortality
        Train MSE: 29.44927766379869
        Test MSE: 29.13440250428632
        A well grouped downward slope with values being clumped at lower adult mortalilty. although there is a stretch of low adult mortality at lower life expectancies. most likely due to places with alot of child mortalities.

        c.Single Feature Regression using Income_composition_of_resources
        Train MSE: 14.742738618475954
        Test MSE: 17.956662184737965
        Tight groupings at high life expectancy high human index but it spreads out more and more the lower down the life expectancy and human index you go, being quite spread at the lowest values. 

    Task.3.2.

        starting at lambda 1 the line isn't close to the shape and is rigid. Working down the average estimator lines get closer and closer to the actual shape of f(x),i.e they are becoming more complex(less bias). but then if you start going too small ( around 0.1 and below), you start to get lines flying off and the graph becomes less accurate (high varience). The grouping of lines also gets tighter as you go lower then starts to spread out far again as you get too low, like a normal curve.

        around 0.2 value gives the best models of both acceptably low var and low enough bias.

    Task.4.1.

        since linear keeps high coefficients it gives alot of varience or overfitting, which is clear when you see how low the training data MSE is and how high the test data MSE is. Causing there to be a large range between the two MSEs, showing inaccuracy. 

        Since Ridge puts a limit on the coefficeints we get much less spread and all of the coefficients being smooth and within a similar range. It gives a slightly bigger error in training data for a much better result in the test data. As a result it has a clearly better balance that the standard linear.

        LASSO has a very agressive approach and will completely remove coefficients that are not fitting. This gives alot of power to certain features. alot of the coefficeints in LASSO are 0, this simplifies the model and leads to more underfitting but it still has much better results. Again there is an increase in training error but antoher large decrease in test error causeing the two MSE values to be close to each ohter. Giving the best generalisation of the models.

        Ridge and LASSO both enforce a restriction on the data leading to teir approaches as subsequent vlaues being relatively similar/ on the same track when compared to basic regression.

## Hours taken:

Collaborators:

### Known Bugs:
    

AI Use Description:


You must acknowledge use here and submit transcript if AI was used for portions of the assignment