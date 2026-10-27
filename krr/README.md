[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/C_3vUy9u)
# README

Tell us about your implementation!

Tell us about your tests!

Answer the conceptual questions!
## Task 1.
    the two jpegs in the folder. IMG_9682 & IMG_9683
    


## Task 3.2.
    Q1.
        0.33326
    Q2.
        0.9517853540447851
    Q3.
        Most likely cause of the problem: SparkPlugs

## Task 3.3.
    Q1. the question with the most valid samples is 1 since it has no values rejected because there was no prior evidence to reject with. It uses n valid
        samples whereas the other two questions cut off some of the samples via rejection. But the question that cut the most is hard to say, as questiom two is only one run of sample generation whereas question 3 is 3 different sample generations. the sum of the samples after filtering from the three sample generations is similar to the samples left in question2. however the question that requires the most samples to be generated and the one with the most samples rejected is question 3. as it has three different probabilites that as calculated, 3n total samples generated.

    Q2. When the number of samples increases the probabilities get more precise and we get more significant figures. The ratio of total samples to samples 
        left after rejection is similar as n increases (n = num samples). the estimation that goes vastly different first is the ones from Q3, this is most likely because it is the estimation with the most rejections so you are left with very few valid samples when you make n low. Q1 doesn't change very much based on n since it always has all the samples being valid, giving it plenty of samples to work with even when n is lower. 

    Q3. knowing how many total samples you need is based off how many valid ssmples you need. get a round estimate of how many valid samples you will get
        from n total samples by analysing the ratio from given values of n. give a confidence interval (i.e.95%) and monitor if it is narrower than a given significance level (i.e. +- 0.001).

## Task 3.4.
    We rank candidate tests by their net value of information. For each test node, we use the BN to predict each outcome’s probability, recompute the best repair action under that outcome, and average those utilities to get EVSI. We then subtract the test’s labor cost and pick the test with the highest positive net value; if none are positive, we proceed directly with the repair that has the highest expected utility under the current beliefs.

## Task 4.4.
    PDDL lets you focus on describing the porblem instead of worrying about how the search works. It is convenient since planners take care of the reasoning for you, so you don’t have to implement algorithms like A* or BFS. The challenge is that debugging is much harder and you have less control over what happens during the search.
    
    I ran into issues with the grid directions and coordinate order, which caused me to consitently have no paths found even tho a similar structure had worked in my 1x1 it just didn't for the 2x2

## Tests.
    TestHeartDiseaseNetwork

        -test_network_structure
            Verifies the heart disease network contains the expected 6 CPTs and that specific CPTs use the expected formats.
            Checks:
            Presence of nodes: Smoking, Exercise, BloodPressure, Cholesterol, HeartDiseaseRisk, ECGResults.
            Smoking is a root CPT with table {"Yes": 0.20, "No": 0.80}.
            BloodPressure has parents ["Smoking","Exercise"] and a specific conditional table for all parent combinations.
        -test_estimate_probability
            Empirical checks using sampling (large num_samples for stability).
            Verifies P(Smoking=Yes) ≈ 0.20 (tolerance ±0.015).
            Verifies a conditional probability P(HeartDiseaseRisk=High | Smoking=Yes, BloodPressure=Normal, Cholesterol=Normal) ≈ 0.12 (tolerance ±0.02).

    TestBayesianNetwork 

        -test_cpt_get_probability_root
            Confirms root CPT get_probability returns the stored prior.
            Confirms providing extraneous parent values raises an error.
        -test_cpt_get_probability_with_parents
            Confirms CPT with parents returns the correct conditional probability when given a complete parent assignment.
            Confirms incomplete parent assignments raise an error.
        -test_build_cpt_from_data_no_parents
            Tests building a CPT from raw data (DataFrame) for a root node; checks frequencies are converted into probabilities.
        -test_build_cpt_from_data_with_parent
            Tests CPT construction for a child node with one parent by grouping counts per parent value and normalizing to probabilities.
        -test_estimate_probability_basic_prior
            Verifies Monte‑Carlo estimate for a simple prior matches the CPT (seeded RNG for reproducibility). Uses many samples to ensure accuracy.
        -test_estimate_probability_with_evidence_no_match
            Tests a corner case where evidence contradicts a deterministic CPT (probability 0); expected estimate is exactly 0.

### Hours taken: 22

Collaborators:

### Known Bugs: 
    had to do a huge amount of trouble shooting for my implementation in task 3.2 . was having and error in sample node value and had to create alot of checks and fallbacks. progam works fine but there was a bug there for a long time hence the fallbacks of a uniform distribution

AI Use Description:

You must acknowledge use here and submit transcript if AI was used for portions of the assignment