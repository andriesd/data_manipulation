gene.data <- read.table('Figure2.txt', header = TRUE, sep = '\t', fill = TRUE, quote ='')
nrow(gene.data)

records <- na.omit(gene.data)
nrow(records)

gene.records <- records[c(3:81)]
rownames(gene.records) <- records$ORF

scaled.records <- scale(gene.records)

library(gplots)

heatmap.2(as.matrix(scaled.records), hclustfun = function(x) hclust(x,method = "complete"), 
          scale = "row", dendrogram="row", trace="none", density.info="none", 
          col=redblue(256), lhei=c(2,250), lwid=c(1.5,2.5), margins = c(5, 8), 
          cexRow=0.5, cexCol=0.7, key=FALSE)

heatmap.2(as.matrix(scaled.records), hclustfun = function(x) hclust(x,method = "average"), 
          scale = "row", dendrogram="row", trace="none", density.info="none", 
          col=redblue(256), lhei=c(2,250), lwid=c(1.5,2.5), margins = c(5, 8), 
          cexRow=0.5, cexCol=0.7, key=FALSE)

pear.dist <- function(x){as.dist(1-cor(t(x), method='pearson'))}

heatmap.2(as.matrix(gene.records), distfun=pear.dist, hclustfun = function(x) hclust(x,method = "average"), 
          scale = "row", dendrogram="row", trace="none", density.info="none", 
          col=redblue(256), lhei=c(2,250), lwid=c(1.5,2.5), margins = c(5, 8), 
          cexRow=0.5, cexCol=0.7, key=FALSE)

