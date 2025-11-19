packages <- c("stargazer","dplyr","ggplot2","modelsummary","kableExtra")
new.packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages,dependencies = TRUE)
lapply(packages, library, character.only = TRUE)

mlb <- read.csv("mlb.csv")
r1 <- lm(log(salary) ~ years + gamesyr + bavg + hrunsyr + rbisyr + frstbase + scndbase + thrdbase + shrtstop + catcher, data = mlb)

modelsummary(models = list(r1),fmt = 3,
             output = "latex",
             statistic = c("({std.error})"),#"t={statistic}","CI = [{conf.low},{conf.high}]"),
             estimate = "{estimate}{stars}",
             stars = c('*'=.1,'**'=.05,'***'=.01),
             notes = "* p < 0.1, ** p < .05, *** p < .01",
             coef_rename = c("years" = "Years experience",
                             "gamesyr" = "Games per year",
                             "bavg" = "Batting Average",
                             "hrunsyr" = "Homeruns per year",
                             "rbisyr" = "RBIs per year",
                             "frstbase" = "First Base",
                             "scndbase" = "Second Base",
                             "thrdbase" = "Third Base",
                             "shrtstop" = "Short Stop",
                             "catcher" = "Catcher"),
             #coef_omit = " ",
             gof_omit = "Log.Lik|AIC|BIC")


r2 <- lm(log(salary) ~ years + gamesyr + bavg + hrunsyr + rbisyr +
           frstbase + scndbase + thrdbase + shrtstop + catcher +
           I(years * frstbase) + I(years * scndbase) + I(years * thrdbase) +
           I(years * shrtstop) + I(years * catcher), data = mlb)


modelsummary(models = list(r1,r2),fmt = 3,
             output = "latex",
             statistic = c("({std.error})"),
             estimate = "{estimate}{stars}",
             stars = c('*'=.1,'**'=.05,'***'=.01),
             notes = "* p < 0.1, ** p < .05, *** p < .01",
             coef_rename = c("years" = "Years experience",
                             "gamesyr" = "Games per year",
                             "bavg" = "Batting Average",
                             "hrunsyr" = "Homeruns per year",
                             "rbisyr" = "RBIs per year",
                             "frstbase" = "First Base",
                             "scndbase" = "Second Base",
                             "thrdbase" = "Third Base",
                             "shrtstop" = "Short Stop",
                             "catcher" = "Catcher"),
             #coef_omit = " ",
             gof_omit = "Log.Lik|AIC|BIC")


SSE_F <- sum((r2$residuals)^2)
SSE_R <- sum((r1$residuals)^2)

K <- length(r2$coefficients)-1
L <- length(r1$coefficients)-1

Fstat <- ((SSE_R-SSE_F)/(K-L))/((SSE_F)/(339-K-1))
Fcrit <- qf(p = 0.05,K-L,339-K-1,lower.tail = F)





