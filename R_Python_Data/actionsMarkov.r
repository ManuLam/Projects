#install.packages("heemod")
#install.packages("diagram")
library('heemod')

mat_dim <- define_transition(
  state_names = c('Discovery', 'Interaction', 'Movement'),
  0.32, 0.34, 0.35,
  0.64, 0.22, 0.14,
  0.61, 0.28, 0.11);

# plotting transition matrix
plot(mat_dim)