# Gini coefficient of three percentages

Given
    `x1 + x2 + x3 = 1`
and knowing that
    `Gmax = 2/3 if n = 3`

```
    G = ~2~ * (abs(x1 - x2) + abs(x2 - x3) + abs(x3 - x1)) / ~2~ * n * sum
        = (abs(x1 - x2) + abs(x2 - x3) + abs(x3 - x1)) / 3

    G_normalised = (abs(x1 - x2) + abs(x2 - x3) + abs(x3 - x1)) / 3 / (2/3)
        = (abs(x1 - x2) + abs(x2 - x3) + abs(x3 - x1)) / 2
```

# Max gini
G = abs(x - 0) / 2 * x = 1/2
G = 2/3
G = n / (n + 1)