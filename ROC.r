# load data
X_cnn <- read.table("results_cnn.csv", sep = ",")

# create and plot RoC curve
library(ROCR)

roc_cnn <- ROCR::performance(ROCR::prediction(X_cnn[,2], X_cnn[,1]), "tpr", "fpr")
plot(roc_cnn, col="green") #add = TRUE

legend("topleft",
c("CNN","BBB"),
fill=c("green","red")
)
abline(a=0, b= 1)
auc.perf = performance(pred, measure = "auc")
auc.perf@y.values