# Custom function: Symetric Difference

id_improved_1 <- c(67.86, 65, 65.71, 62.86, 62.14)
custom_1 <- c(69.29, 67.14, 65.00, 69.29, 68.57)

t.test(custom_1, id_improved_1, alternative="g", conf.level = 0.95)

data <- data.frame(id_improved=id_improved_1, symmetric_diff=custom_1)
boxplot(data)

# Custom function: Fractional 3 deep

id_improved_2 <- c(58.57, 60.71, 63.57, 66.43, 57.14)
custom_2 <- c(70.00, 68.57, 69.29, 75.00, 75.00)

t.test(custom_2, id_improved_2, alternative="g", conf.level = 0.95)

data <- data.frame(id_improved=id_improved_2, fractional_3=custom_2)
boxplot(data)


t.test(custom_2, custom_1, alternative="g", conf.level = 0.95)

# Custom function: Fractional 2 deep

id_improved_3 <- c(56.43, 65.71, 60.71, 64.29, 62.14)
custom_3 <- c(70.71, 72.86, 72.14, 81.43, 65.00)

t.test(custom_3, id_improved_3, alternative="g", conf.level = 0.95)

data <- data.frame(id_improved=id_improved_3, fractional_2=custom_3)
boxplot(data)


data <- data.frame(idim_1=id_improved_1, custom_1=custom_1,
                   idim_2=id_improved_2, custom_2=custom_2,
                   idim_3=id_improved_3, custom_3=custom_3)
boxplot(data)

