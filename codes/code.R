genes = read.table('./new_pipeline/refGene.txt')
genes <- genes[, c('V2', 'V3', 'V4', 'V5', 'V6')]
colnames(genes) <- c('name', 'chrom', 'strand', 'start', 'end')
genes <- genes[!grepl('NR', genes$name),]
genes$should_del <- F

# sort genes based on chr and starting pos
genes <- genes[with(genes, order(chrom, start)), ]

index1 <- which(- genes[1:dim(genes)[1] - 1, 'end'] + genes[2:dim(genes)[1], 'start'] < 1500)
index2 <- index1 + 1
del_ind1 <- index1[genes[index1, 'strand'] != genes[index2, 'strand']]
del_ind2 <- index2[genes[index1, 'strand'] != genes[index2, 'strand']]
genes[union(del_ind1, del_ind2), 'should_del'] = T

db_poly <- read.table('./new_pipeline/hgTables', header = T)

db_poly$tmp <- stringr::str_split_fixed(db_poly[, 'name'], '.polyA', 2)[, 1]
db_poly <- db_poly[! (db_poly$tmp %in% as.character(genes[genes$should_del == T, 'name'])), ]

db_poly$bin <- NULL
db_poly$tmp <- NULL
write.table(db_poly, file = './new_pipeline/poly_db_hg19', row.names = F, quote = F)

