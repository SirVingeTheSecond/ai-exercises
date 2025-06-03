data <- read.csv("social_network_ads.csv")

head(data)

if (!require(ggplot2)) {install.packages("ggplot2")}

library(ggplot2)

# scatterplot of age vs estimated salary with color by purchased
ggplot(data, aes(x = Age, y = EstimatedSalary, color = factor(Purchased))) +
  geom_point() +
  labs(title = "Estimated Salary vs Age", x = "Age", y = "Estimated Salary")

ggsave("social_network_ads.png")

data <- read.csv("adult_income.csv")

head(data)

ggplot(data, aes(x = age, y = hours_per_week, color = factor(income_high))) +
  geom_point() +
  labs(title = "Hours per Week vs Age", x = "Age", y = "Hours per Week")
ggsave("adult_income_hpw_age.png")

ggplot(data, aes(x = hours_per_week, y = workclass, color = factor(income_high))) +
  geom_point() +
  labs(title = "Work Class vs Hours per Week", x = "Hours per Week", y = "Work Class")
ggsave("adult_income_hpw_wc.png")