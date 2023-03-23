library(ggplot2)     # plots
library(lubridate)   # datetime parsing
library(tidyr)       # data manipulation
library(scales)      # dates

############################### time series load  #############################
serie <- read.csv("../data/radon-data.csv")
serie$time <- as_datetime(serie$time)         # convert the dates

#################################### plots #################################### 
# We fix the color for all the plots:
colors_onoff <- c("On" = "red", "Off" = "black")
colors_realpred <- c("Predictions" = "red", "Real values" = "black")

# 1. Complete radon level series
ggplot(serie, aes(x = time, y = radon)) + 
  geom_line() + 
  labs(x = "Time (10 minutes frequency)",
       y = "Radon level (Bq/m³)",
       color = "Legend")
ggsave("../figures/radon_complete_signal.png", width = 10, height = 5)

# 2. Remaining variables 
p1 <- ggplot(serie, aes(x = time, y = temperature)) + geom_line()
p2 <- ggplot(serie, aes(x = time, y = humidity)) + geom_line()
p3 <- ggplot(serie, aes(x = time, y = pressure)) + geom_line()
p4 <- ggplot(serie, aes(x = time, y = tvoc)) + geom_line()
png("../figures/remaining_variables.png", width = 960, height = 480)
gridExtra::grid.arrange(p1, p2, p3, p4, ncol=2)
dev.off()

# 3. Violin plot of radon levels
ggplot(serie, aes(x = 1, y = radon)) +
  geom_violin(trim = FALSE) + 
  geom_boxplot(width = 0.1) +
  theme(axis.text.x = element_blank()) + 
  labs(x = "Density",
       y = "Radon level (Bq/m³)")
ggsave("../figures/radon_violin.png", width = 10, height = 5)

# 4. Ventilation influence
ggplot(serie[c(40000:40500), ], aes(x = time, 
                                    y = radon,
                                    group = 1,
                                    colour = state
                                    )
       ) + 
  geom_line() + 
  labs(x = "Time (10 minutes frequency)",
       y = "Radon level (Bq/m³)",
       color = "Ventilation status") + 
  scale_color_manual(values = colors_onoff)
ggsave("../figures/radon_signal_ventilation_influence.png", 
       width = 10, height = 5)


# 5. Radon forecasting.
predictions <- read.csv("../data/predictions.csv")
ggplot(predictions, aes(x = c(1:length(real)))) +
  geom_line(aes(y = predictions, color = "Predictions")) + 
  geom_line(aes(y = real, color = "Real values")) + 
  labs(x = "Time forecast",
       y = "Radon level (Bq/m³)",
       color = "Legend") + 
  scale_color_manual(values = colors_realpred)
ggsave("../figures/LSTM_forecasting.png", width = 10, height = 5)

# 6. Same, but closer
ggplot(predictions[c(600:700),], aes(x = c(1:length(real)))) +
  geom_line(aes(y = predictions, color = "Predictions")) + 
  geom_line(aes(y = real, color = "Real values")) + 
  labs(x = "Time forecast",
       y = "Radon level (Bq/m³)",
       color = "Legend") + 
  scale_color_manual(values = colors_realpred)
ggsave("../figures/LSTM_forecasting_close.png", width = 10, height = 5)


###################### test forecast results ##################################
actions <- read.csv("../data/test_forecast_results/actions_ANN_predictor.csv")
measures <- read.csv("../data/test_forecast_results/measures_ANN_predictor.csv")
predictions <- read.csv("../data/test_forecast_results/predictions_ANN_predictor.csv")

# parse all the dates
actions$time <- as_datetime(actions$time)
measures$time <- as_datetime(measures$time)
predictions$time <- as_datetime(predictions$time)

# we will change the names for simplicity
colnames(measures)[which(names(measures)=="radon")] <- "real"
colnames(predictions)[which(names(predictions)=="value")] <- "predictions"

# the model was working for 4 days:
start <- "2022-04-11 16:00"
end <- "2022-04-15 00:00"

actions <- subset(actions, time > start & time < end)[,c("time", "value")]
measures <- subset(measures, time > start & time < end)[,c("time", "real")]
predictions <- subset(predictions, 
                      time > start & time < end)[,c("time", "predictions")]

# combine them in a standalone table
standalone <- merge(measures, predictions, by="time", all=TRUE)
standalone[,"status"] <- NA

last_status <- "Off"
j <- 1
for ( i in 1:nrow(actions) ){
  current_date <- actions$time[i]
  current_status <- actions$value[i]
  while (current_date > standalone$time[j]) {
    standalone$status[j] <- last_status
    j <- j + 1
  }
  last_status <- current_status
}

# we now need to fill the gaps introduced by the left join
standalone <- fill(standalone, value, .direction="up")
standalone[is.na(standalone)] <- "Off" # the remaining (the firsts obervations)

ggplot(standalone, aes(x = time)) +
  geom_line(aes(y = predictions, color = "Predictions")) +
  geom_line(aes(y = real, color = "Real values")) + 
  scale_x_datetime(date_breaks = "1 day", labels = date_format("%d/%m")) +
  labs(x = "Forecast",
       y = "Radon level (Bq/m³)",
       color = "Legend") + 
  scale_color_manual(values = colors_realpred)
ggsave("../figures/test_forecast.png", width = 10, height = 5)

# on/off in the forecast
colors <- c("On" = "red", "Off" = "black")
ggplot(standalone, aes(x = time,
                       y = real,
                       group = 1,
                       colour = status)) + 
  geom_line() + 
  geom_hline(yintercept = 300, linetype="dotted", col="red") +
  scale_x_datetime(date_breaks = "1 day", labels = date_format("%d/%m")) + 
  labs(x = "Time (10 minutes frequency)",
       y = "Radon level (Bq/m³)",
       color = "Ventilation status") + 
  scale_color_manual(values = colors_onoff)
ggsave("../figures/test_forecast_fan_status.png", width = 10, height = 5)
