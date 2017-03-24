# Custom function: 003160f6ddbe92190f930a749c73a7eed24517f0

id_improved <- c(67.86, 65, 65.71, 62.86, 62.14)
custom_1 <- c(69.29, 67.14, 65.00, 69.29, 68.57)

t.test(custom_1, id_improved, alternative="g", conf.level = 0.95)

# Custom function: 8d65a551120f30eae3bcf0823b24b604e34b4f7f

id_improved <- c(58.57, 60.71, 63.57, 66.43, 57.14)
custom_2 <- c(70.00, 68.57, 69.29, 75.00)

t.test(custom_2, id_improved, alternative="g", conf.level = 0.95)

