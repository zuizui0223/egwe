args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: Rscript inspect_intflex_stage_a.R NETWORK_RDATA OUT_TXT")
network_path <- args[[1]]
out_path <- args[[2]]

env <- new.env(parent = emptyenv())
loaded <- load(network_path, envir = env)
objects <- ls(env, all.names = TRUE)

con <- file(out_path, open = "wt")
on.exit(close(con), add = TRUE)
writeLines("status=value_blind_object_structure_complete", con)
writeLines(paste0("loaded_objects=", paste(sort(loaded), collapse = ",")), con)
writeLines(paste0("environment_objects=", paste(sort(objects), collapse = ",")), con)

if (!"nets" %in% objects) {
  writeLines("nets_present=false", con)
  quit(status = 0)
}

nets <- get("nets", envir = env)
writeLines("nets_present=true", con)
writeLines(paste0("nets_class=", paste(class(nets), collapse = ",")), con)
writeLines(paste0("nets_length=", length(nets)), con)
writeLines(paste0("nets_names=", paste(names(nets), collapse = "|")), con)

is_matrix <- vapply(nets, is.matrix, logical(1))
writeLines(paste0("all_elements_matrix=", all(is_matrix)), con)

if (length(nets) > 0) {
  dims <- vapply(nets, function(x) paste(dim(x), collapse = "x"), character(1))
  writeLines(paste0("matrix_dims=", paste(paste(names(nets), dims, sep = ":"), collapse = "|")), con)
  rowname_flags <- vapply(nets, function(x) !is.null(rownames(x)) && length(rownames(x)) == nrow(x), logical(1))
  colname_flags <- vapply(nets, function(x) !is.null(colnames(x)) && length(colnames(x)) == ncol(x), logical(1))
  writeLines(paste0("all_row_names_present=", all(rowname_flags)), con)
  writeLines(paste0("all_col_names_present=", all(colname_flags)), con)
}

writeLines(
  "inspection_boundary=Only R object names, classes, list element names, matrix dimensions, and presence of row/column names were inspected. No matrix cell, interaction count, species occupancy, refuge value, future outcome, coefficient, score, or p-value was read or computed.",
  con
)
