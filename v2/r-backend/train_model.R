library(readxl)
library(plyr)
library(DAAG)
library(jsonlite)
library(magrittr)

train_model <- function(filepath, model_type) {
  mydata <- read_excel(filepath)

  # Feature engineering (identical to original R scripts)
  mydata$`First Attempt` <- revalue(mydata$`First Attempt`, c("incorrect" = 0))
  mydata$`First Attempt` <- revalue(mydata$`First Attempt`, c("hint" = 0))
  mydata$`First Attempt` <- revalue(mydata$`First Attempt`, c("correct" = 1))

  mydata["Outcome"] <- as.numeric(mydata$`First Attempt`)
  mydata <- na.omit(mydata)

  mydata["KCModel"] <- mydata$`KC (Default)`
  mydata["OpportunityModel"] <- as.numeric(as.character(mydata$Opportunity))
  mydata["CorrectModel"] <- as.numeric(as.character(mydata$Corrects))
  mydata["IncorrectModel"] <- as.numeric(as.character(mydata$Incorrects))
  mydata["TellsModel"] <- as.numeric(as.character(mydata$Hints))

  # Add Row column if missing
  if (!"Row" %in% colnames(mydata)) {
    mydata$Row <- seq_len(nrow(mydata))
  }

  # Select formula based on model type
  if (model_type == "AFM") {
    form <- Outcome ~ AnonStudentId + KCModel + KCModel:OpportunityModel
  } else if (model_type == "PFM") {
    form <- Outcome ~ AnonStudentId + KCModel + KCModel:(CorrectModel + IncorrectModel)
  } else if (model_type == "IFM") {
    form <- Outcome ~ AnonStudentId + KCModel + KCModel:(CorrectModel + IncorrectModel + TellsModel)
  } else {
    stop(paste("Unknown model type:", model_type))
  }

  # Train on full data
  training_model <- glm(form, family = binomial(), data = mydata)

  # Predictions on full data
  probabilities <- predict(training_model, mydata, type = "response")
  predicted_probabilities <- ifelse(probabilities > 0.5, probabilities, 1 - probabilities)
  prediction <- ifelse(probabilities > 0.5, 1, 0)

  predictions_df <- data.frame(
    row = mydata$Row,
    predicted_probability = round(predicted_probabilities, 2),
    prediction = prediction
  )

  # Cross-validation
  cv_result <- CVbinary(training_model, print.details = FALSE)
  acc_cv <- cv_result$acc.cv

  # 80/20 train-test split
  N <- nrow(mydata)
  sample_size <- floor(0.8 * N)
  set.seed(123)
  train_ind <- sample(seq_len(N), size = sample_size)
  traindata <- mydata[train_ind, ]
  testdata <- mydata[-train_ind, ]

  test_model <- glm(form, family = binomial(), data = traindata)
  test_probabilities <- predict(test_model, testdata, type = "response")
  test_prediction <- ifelse(test_probabilities > 0.5, 1, 0)

  rmse <- sqrt(mean((testdata$Outcome - test_prediction)^2))

  # Confusion matrix metrics
  confusion_matrix <- table(ACTUAL = testdata$Outcome, PREDICTED = test_prediction)
  TN <- confusion_matrix[1, 1]
  FP <- confusion_matrix[1, 2]
  FN <- confusion_matrix[2, 1]
  TP <- confusion_matrix[2, 2]
  precision_val <- TP / (TP + FP)
  recall_val <- TP / (TP + FN)
  f1_val <- (2 * (precision_val * recall_val)) / (precision_val + recall_val)

  # Information criteria
  aic <- summary(training_model)$aic
  K <- length(coef(training_model))
  bic <- aic + K * (log(N) - 2)
  likelihood <- -summary(training_model)$deviance / 2
  aicc <- -2 * likelihood + 2 * K + (2 * K * (K + 1) / (N - K - 1))

  # Brier score and log loss
  pred_prob <- predict(training_model, type = "response")
  brier_score <- mean((pred_prob - mydata$Outcome)^2)

  logLoss <- function(pred, actual) {
    -mean(actual * log(pred) + (1 - actual) * log(1 - pred))
  }
  log_loss_val <- logLoss(pred = pred_prob, actual = mydata$Outcome)

  # Build stats
  stats <- list(
    model_type = paste0("R_", model_type),
    aic = round(aic, 2),
    aicc = round(aicc, 2),
    bic = round(bic, 2),
    num_parameters = K,
    likelihood = round(likelihood, 2),
    brier_score = round(brier_score, 2),
    log_loss = round(log_loss_val, 2),
    rmse = round(rmse, 2),
    acc_cv = round(acc_cv, 2),
    precision = round(precision_val, 2),
    recall = round(recall_val, 2),
    f1 = round(f1_val, 2)
  )

  # Build coefficients
  coef_values <- coef(training_model)
  coefficients <- data.frame(
    feature = names(coef_values),
    coef = round(as.numeric(coef_values), 2),
    stringsAsFactors = FALSE
  )

  return(list(
    stats = stats,
    coefficients = coefficients,
    predictions = predictions_df
  ))
}
