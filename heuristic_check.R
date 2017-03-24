# Custom function: 

id_improved <- c(67.86, 2, 3, 1, 1)
custom <- c(69.29, 2, 3, 2, 3)

t.test(id_improved, custom, alternative="g", conf.level = 0.95)
