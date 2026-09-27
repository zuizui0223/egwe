args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) stop("usage: Rscript run_intflex_strongest_refuge_extract.R NETWORK_RDATA SAMPLES_CSV OUTDIR")
network_path <- args[[1]]
samples_path <- args[[2]]
outdir <- args[[3]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

load(network_path)
if (!exists("nets") || !is.list(nets)) stop("locked object nets missing")

samples <- read.csv(samples_path, check.names = FALSE, row.names = 1)

parse_name <- function(x) {
  m <- regexec("^(.+)\\.([0-9]{4})$", x)
  hit <- regmatches(x, m)[[1]]
  if (length(hit) != 3) stop(paste("invalid network name", x))
  list(site = hit[[2]], year = as.integer(hit[[3]]))
}

edge_rows <- list()
net_rows <- list()
e <- 1L
n <- 1L
for (nm in names(nets)) {
  p <- parse_name(nm)
  mat <- nets[[nm]]
  if (!is.matrix(mat) || is.null(rownames(mat)) || is.null(colnames(mat))) stop(paste("invalid matrix", nm))
  yr <- as.character(p$year)
  effort <- NA_real_
  if (p$site %in% rownames(samples) && yr %in% colnames(samples)) effort <- as.numeric(samples[p$site, yr])
  net_rows[[n]] <- data.frame(network = nm, site = p$site, year = p$year,
                              nplant = nrow(mat), npollinator = ncol(mat),
                              sample_rounds = effort, stringsAsFactors = FALSE)
  n <- n + 1L
  idx <- which(mat > 0, arr.ind = TRUE)
  if (nrow(idx) > 0) {
    edge_rows[[e]] <- data.frame(network = nm, site = p$site, year = p$year,
                                 plant = rownames(mat)[idx[, 1]],
                                 pollinator = colnames(mat)[idx[, 2]],
                                 stringsAsFactors = FALSE)
    e <- e + 1L
  }
}

edges <- if (length(edge_rows)) do.call(rbind, edge_rows) else data.frame()
netmeta <- do.call(rbind, net_rows)
write.csv(edges, file.path(outdir, "positive_edges.csv"), row.names = FALSE, quote = TRUE)
write.csv(netmeta, file.path(outdir, "network_metadata.csv"), row.names = FALSE, quote = TRUE)

receipt <- list(
  status = "outcome_opened_locked_extraction_complete",
  n_networks = nrow(netmeta),
  n_positive_edges = nrow(edges),
  n_sites = length(unique(netmeta$site)),
  years = sort(unique(netmeta$year)),
  note = "Matrix cells were opened only after the Stage-B contract was committed. Only binary-positive edge identity and locked network metadata were exported; no alternative endpoint or threshold was searched."
)
json <- paste0(
  "{\n",
  sprintf("  \"status\": \"%s\",\n", receipt$status),
  sprintf("  \"n_networks\": %d,\n", receipt$n_networks),
  sprintf("  \"n_positive_edges\": %d,\n", receipt$n_positive_edges),
  sprintf("  \"n_sites\": %d,\n", receipt$n_sites),
  sprintf("  \"years\": [%s],\n", paste(receipt$years, collapse = ", ")),
  sprintf("  \"note\": \"%s\"\n", receipt$note),
  "}\n"
)
writeLines(json, file.path(outdir, "extraction_receipt.json"))
cat(json)
