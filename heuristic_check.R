# Custom function: 003160f6ddbe92190f930a749c73a7eed24517f0

id_improved <- c(67.86, 65, 65.71, 62.86, 62.14)
custom <- c(69.29, 67.14, 65.00, 69.29, 68.57)

t.test(custom, id_improved, alternative="g", conf.level = 0.95)
