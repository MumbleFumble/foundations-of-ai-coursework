[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IQvorXRE)


## Implementation
    
    - NumPy logistic regression (from scratch with gradient descent)
    - PyTorch logistic regression (manual parameter updates with autograd)
    - Simple perceptron (nn.Linear + Sigmoid)
    - Custom multilayer perceptron (MyMLP) with >90% accuracy

## Results 
    - NumPy logistic regression accuracy: ~0.66
    - PyTorch logistic regression accuracy: ~0.62
    - Simple perceptron accuracy: ~0.65
    - MyMLP accuracy: ~95–96%


## Conceptual (Part 4)
    1. Hyperparameters tried: number of hidden layers, widths (8–64), activations (ReLU/Tanh/Sigmoid), learning rate (1e-3 to 2e-2), iterations (1k–60k). Tanh in hidden layers with moderate width worked best here.
    2. Effects: More/larger layers increased capacity and improved fit up to a point; too large or too fast learning caused slower convergence or instability. Final settings balanced accuracy and runtime.
    3. Doubling hidden sizes: modest improvement is possible due to higher capacity, but diminishing returns and risk of overfitting/longer training. On this dataset, gains were small beyond ~32-wide layers.

## Notes / Known issues


    - Hours taken: 9
    - Collaborators: 
    - Known bugs: 
    - AI use: 