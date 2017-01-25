library(ggplot2)
library(hexbin)

scores <- read.table('star_sentimentscore.txt', sep='\t')

visual <- ggplot(scores, aes(V1, V2)) + geom_point(shape=1) + geom_smooth(method=lm, se=FALSE) + labs(x="Weighted Average Star Rating", y="Average Sentiment Score") 
print(visual)

visual + stat_binhex() 

cor(x=scores$V1, y=scores$V2, method="pearson")

