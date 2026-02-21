library(plumber)
library(jsonlite)

source("train_model.R")

MAX_FILE_SIZE <- 50 * 1024 * 1024  # 50 MB

# Simple in-memory rate limiter
rate_limit_store <- new.env(parent = emptyenv())

check_rate_limit <- function(req, res, max_requests = 10L, window = 60) {
  forwarded <- req$HTTP_X_FORWARDED_FOR
  if (!is.null(forwarded) && nchar(forwarded) > 0) {
    client_ip <- trimws(strsplit(forwarded, ",")[[1]][1])
  } else {
    client_ip <- if (!is.null(req$REMOTE_ADDR)) req$REMOTE_ADDR else "unknown"
  }
  now <- as.numeric(Sys.time())

  if (is.null(rate_limit_store[[client_ip]])) {
    rate_limit_store[[client_ip]] <- list(timestamps = c())
  }

  # Keep only timestamps within the window
  entry <- rate_limit_store[[client_ip]]
  entry$timestamps <- entry$timestamps[
    entry$timestamps > (now - window)
  ]

  if (length(entry$timestamps) >= max_requests) {
    res$status <- 429L
    return(FALSE)
  }

  entry$timestamps <- c(entry$timestamps, now)
  rate_limit_store[[client_ip]] <- entry
  return(TRUE)
}

#* @apiTitle IRT Student Models - R Backend

#* Health check
#* @get /api/health
function() {
  list(status = "ok", service = "r-backend")
}

#* Train a single model
#* @post /api/train
function(req, res) {
  # Rate limit: 10 requests per minute
  if (!check_rate_limit(req, res)) {
    return(list(detail = "Rate limit exceeded. Max 10 requests/minute."))
  }

  # Extract model_type from multipart body
  model_type <- req$body$model_type
  if (is.list(model_type)) model_type <- model_type[[1]]
  if (is.raw(model_type)) model_type <- rawToChar(model_type)

  # Validate model_type
  valid_types <- c("AFM", "PFM", "IFM")
  if (is.null(model_type) || !(model_type %in% valid_types)) {
    res$status <- 400L
    return(list(detail = paste(
      "Invalid model_type. Must be one of:",
      paste(valid_types, collapse = ", ")
    )))
  }

  # Extract uploaded file
  upload <- req$body$file
  if (is.null(upload)) {
    res$status <- 400L
    return(list(detail = "No file uploaded"))
  }

  # File size check
  raw_data <- if (is.raw(upload[[1]])) upload[[1]] else upload
  if (length(raw_data) > MAX_FILE_SIZE) {
    res$status <- 413L
    return(list(detail = "File too large. Maximum size is 50 MB"))
  }

  # Write to temp file
  tmp <- tempfile(fileext = ".xlsx")
  if (is.raw(upload[[1]])) {
    writeBin(upload[[1]], tmp)
  } else if (!is.null(upload$datapath)) {
    file.copy(upload$datapath, tmp)
  } else {
    writeBin(upload, tmp)
  }

  result <- tryCatch({
    train_model(tmp, model_type)
  }, error = function(e) {
    list(error = TRUE, message = conditionMessage(e))
  }, finally = {
    unlink(tmp)
  })

  if (!is.null(result$error) && result$error == TRUE) {
    res$status <- 500L
    return(list(detail = result$message))
  }

  # Convert predictions dataframe to list of lists
  preds_list <- lapply(
    seq_len(nrow(result$predictions)),
    function(i) {
      list(
        row = result$predictions$row[i],
        predicted_probability =
          result$predictions$predicted_probability[i],
        prediction = result$predictions$prediction[i]
      )
    }
  )

  coefs_list <- lapply(
    seq_len(nrow(result$coefficients)),
    function(i) {
      list(
        feature = result$coefficients$feature[i],
        coef = result$coefficients$coef[i]
      )
    }
  )

  list(
    stats = result$stats,
    coefficients = coefs_list,
    predictions = preds_list
  )
}

#* @plumber
function(pr) {
  pr %>%
    pr_set_serializer(serializer_unboxed_json())
}
