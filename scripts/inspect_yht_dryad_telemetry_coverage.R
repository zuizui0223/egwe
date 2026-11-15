#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: inspect_yht_dryad_telemetry_coverage.R <rdata> <output.csv>")
src <- args[[1]]
out <- args[[2]]

env <- new.env(parent = emptyenv())
loaded <- load(src, envir = env)
required <- c("elkID", "Date", "Easting", "Northing")
eligible_objects <- loaded[vapply(loaded, function(nm) {
  x <- get(nm, envir = env)
  is.data.frame(x) && all(required %in% names(x))
}, logical(1))]

if (length(eligible_objects) != 1) {
  stop(sprintf("expected exactly one dataframe with required movement columns, found %d: %s",
               length(eligible_objects), paste(eligible_objects, collapse=",")))
}

d <- get(eligible_objects[[1]], envir = env)
# Outcome firewall: from this point forward subset to movement-only columns.
d <- d[, required]
d$Date <- as.Date(d$Date)
if (anyNA(d$Date)) stop("Date contains unparsable values")

d <- d[is.finite(d$Easting) & is.finite(d$Northing) & !is.na(d$elkID), ]
md <- format(d$Date, "%m-%d")
d <- d[md >= "09-15" & md <= "11-15", ]
d$year <- as.integer(format(d$Date, "%Y"))

key <- unique(d[, c("year", "Date", "elkID")])
daily <- aggregate(elkID ~ year + Date, data = key, FUN = length)
names(daily)[names(daily) == "elkID"] <- "n_unique_individuals"

years <- sort(unique(daily$year))
rows <- lapply(years, function(y) {
  x <- daily[daily$year == y, ]
  eligible <- x$n_unique_individuals >= 10
  data.frame(
    year = y,
    days_with_any_data = nrow(x),
    eligible_days_n10 = sum(eligible),
    max_daily_individuals = max(x$n_unique_individuals),
    mean_daily_individuals_on_eligible_days =
      if (any(eligible)) mean(x$n_unique_individuals[eligible]) else NA_real_,
    eligible_year_30days = sum(eligible) >= 30
  )
})
summary <- do.call(rbind, rows)
dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
write.csv(summary, out, row.names = FALSE)

cat(sprintf("movement_object=%s\n", eligible_objects[[1]]))
cat(sprintf("movement_rows_after_column_firewall=%d\n", nrow(d)))
cat(sprintf("eligible_years=%s\n",
            paste(summary$year[summary$eligible_year_30days], collapse=",")))
cat(sprintf("n_eligible_years=%d\n", sum(summary$eligible_year_30days)))
