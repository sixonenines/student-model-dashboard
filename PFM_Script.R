library(boot);
library(DAAG);

library(tidyverse);
library(caret);


library(plyr);
library(caret);
library(car);
#library(pROC);
library(readxl);
#library(pROC);
library(readxl);
library(glmnet);
#library(glmnetUtils);

library(optimx);

cmdargs <- commandArgs(trailingOnly=TRUE)


inputfilelocation <- cmdargs[1]
val= cmdargs[2]
outputfilelocation <- paste("./output/PFM_Rstats_",val,".csv",sep="")
coefficientfilelocation <- paste("./output/PFM_Rcoef_",val,".csv",sep="")
predictionfilepath <- paste("./output/PFM_Pred_",val,".csv",sep="")

#write("print", stdout())
#write(filelocation, stdout())
mydata <- read_excel(inputfilelocation)
#names(mydata)




#exportdf <- mydata


#write.csv(filelocation, "./Bobro.csv", row.names=FALSE)






Model_type<-c("PFM")
Models_AIC <- rep(1,1);
Models_BIC <- rep(1,1);
AICc <- rep(1,1);
names(AICc) <- c("PFM")
RMSE <- rep(1,1);
names(RMSE)<-c("PFM")
ACCcv <- rep(1,1);
NumParameters <- rep(1,1);
Likelihood <- rep(1,1);
BrierScore <- rep(1,1);
LogLoss <- rep(1,1);
names(LogLoss)<- c("PFM")
names(Models_AIC)<-c("PFM")
names(Models_BIC)<-c("PFM")
names(ACCcv)<-c("PFM")
names(NumParameters)<-c("PFM")
names(Likelihood)<-c("PFM")
names(BrierScore)<-c("PFM")

Precision<-rep(1,1);
Recall<-rep(1,1);
F1 <- rep(1,1);
names(Precision)<-c("PFM")
names(Recall)<-c("PFM")
names(F1)<-c("PFM")



#Model_type=c("AFM","PFM","IFM")
#Models_AIC <- rep(1,3);
#Models_BIC <- rep(1,3);
#ACCcv <- rep(1,3);
#NumParameters <- rep(1,3);
#Likelihood <- rep(1,3);
#BrierScore <- rep(1,3);
#LogLoss <- rep(1,3);
#names(LogLoss)<- c("AFM","PFM","IFM")
#names(Models_AIC)<-c("AFM", "PFM", "IFM")
#names(Models_BIC)<-c("AFM", "PFM", "IFM")
#names(ACCcv)<-c("AFM", "PFM", "IFM")
#names(NumParameters)<-c("AFM", "PFM", "IFM")
#names(Likelihood)<-c("AFM", "PFM", "IFM")
#names(BrierScore)=c("AFM","PFM","IFM")


#AICc <- rep(1,3);
#names(AICc) <- c("AFM","PFM","IFM")

#RMSE <- rep(1,3);
#names(RMSE)<-c("AFM","PFM","IFM")


mydata$`First Attempt` = revalue(mydata$`First Attempt`, c("incorrect"= 0))
mydata$`First Attempt` = revalue(mydata$`First Attempt`, c("hint"= 0))
mydata$`First Attempt` = revalue(mydata$`First Attempt`, c("correct"= 1))
  
mydata["Outcome"] = as.numeric(mydata$`First Attempt`)

mydata <- na.omit(mydata)
  

mydata["KCModel"] = mydata$`KC (Default)`
mydata["OpportunityModel"] = as.numeric(as.character(mydata$`Opportunity`))
  

mydata["CorrectModel"] = as.numeric(as.character(mydata$`Corrects`))
mydata["IncorrectModel"] = as.numeric(as.character(mydata$`Incorrects`))

mydata["TellsModel"] = as.numeric(as.character(mydata$`Hints`))
  

#AFM_form <- Outcome ~ AnonStudentId +KCModel + KCModel:OpportunityModel
#AFMTrainingModel <- glm(AFM_form, family=binomial(), data= mydata); 


PFM_form <- Outcome ~ AnonStudentId +KCModel + KCModel:(CorrectModel + IncorrectModel)
PFMTrainingModel <- glm(PFM_form, family=binomial(), data= mydata); 

PFMprobabilities <- PFMTrainingModel %>% predict(mydata, type = "response")
PFMpredictedProbabilities <- ifelse(PFMprobabilities>0.5, PFMprobabilities, 1-PFMprobabilities)
PFMprediction <- ifelse(PFMprobabilities >0.5,1,0)

ModelPredictions <- data.frame(Row=mydata$`Row`,R_PFMpredictedProbabilities=PFMpredictedProbabilities,R_PFMprediction=PFMprediction)


#IFM_form <- Outcome ~ AnonStudentId +KCModel + KCModel:(CorrectModel + IncorrectModel + TellsModel)
#IFMTrainingModel <- glm(IFM_form, family=binomial(), data= mydata); 



#cvafm = CVbinary(AFMTrainingModel,print.details=FALSE);
#ACCcv["AFM"] <- cvafm$acc.cv


cvpfm = CVbinary(PFMTrainingModel,print.details=FALSE);
ACCcv["PFM"] <- cvpfm$acc.cv

#cvifm = CVbinary(IFMTrainingModel,print.details=FALSE);
#ACCcv["IFM"] <- cvifm$acc.cv




cols = ncol(mydata)
sample_size = floor(0.8 *nrow(mydata))
set.seed(123)
   
train_ind <- sample(seq_len(nrow(mydata)), size = sample_size)
traindata <- mydata[train_ind, ]
testdata <- mydata[-train_ind, ]

#AFMTrainingTestModel <- glm(AFM_form, family=binomial(), data= traindata); 
PFMTrainingTestModel <- glm(PFM_form, family=binomial(), data= traindata); 
#IFMTrainingTestModel <- glm(IFM_form, family=binomial(), data= traindata); 

#afmProbabilities <- AFMTrainingTestModel %>% predict(testdata, type = "response")

#testdata$afmprediction <- ifelse(afmProbabilities >0.5,1,0)

#Check the error between real outcomes and predicted variables 
#RMSE["AFM"]<-sqrt(mean((testdata$Outcome - testdata$afmprediction)^2))


pfmProbabilities <- PFMTrainingTestModel %>% predict(testdata, type = "response")


testdata$pfmprediction <- ifelse(pfmProbabilities >0.5,1,0)

#Check the error between real outcomes and predicted variables 
RMSE["PFM"]<-sqrt(mean((testdata$Outcome - testdata$pfmprediction)^2))



#ifmProbabilities <- IFMTrainingTestModel %>% predict(testdata, type = "response")

#testdata$ifmprediction <- ifelse(ifmProbabilities >0.5,1,0)

#Check the error between real outcomes and predicted variables 
#RMSE["IFM"]<-sqrt(mean((testdata$Outcome - testdata$ifmprediction)^2))

confusion_matrix=table(ACTUAL=testdata$Outcome,PREDICTED=testdata$pfmprediction)
TN=confusion_matrix[1,1]
FP=confusion_matrix[1,2]
FN=confusion_matrix[2,1]
TP=confusion_matrix[2,2]
Precisions<-TP/ (TP+FP)
Recalls<-TP/ (TP+FN)
F1s<- (2*(Precisions*Recalls)) / (Precisions+Recalls)
Precision["PFM"]<- Precisions
Recall["PFM"] <- Recalls
F1["PFM"] <- F1s





N<-nrow(mydata)
#Models_AIC["AFM"]<-summary(AFMTrainingModel)$aic	
#Models_BIC["AFM"]<-summary(AFMTrainingModel)$aic+length(coef(AFMTrainingModel))*(log(N)-2);


Models_AIC["PFM"]<-summary(PFMTrainingModel)$aic	
Models_BIC["PFM"]<-summary(PFMTrainingModel)$aic+length(coef(PFMTrainingModel))*(log(N)-2);

#Models_AIC["IFM"]<-summary(IFMTrainingModel)$aic	
#Models_BIC["IFM"]<-summary(IFMTrainingModel)$aic+length(coef(IFMTrainingModel))*(log(N)-2);


#NumParameters["AFM"] <- length(coef(AFMTrainingModel))
NumParameters["PFM"] <- length(coef(PFMTrainingModel))
#NumParameters["IFM"] <- length(coef(IFMTrainingModel))
  
#Likelihood["AFM"] <- -summary(AFMTrainingModel)$deviance/2
Likelihood["PFM"] <- -summary(PFMTrainingModel)$deviance/2
#Likelihood["IFM"] <- -summary(IFMTrainingModel)$deviance/2


#afmpred.prob <- predict(AFMTrainingModel,type='response')
pfmpred.prob <- predict(PFMTrainingModel,type='response')
#ifmpred.prob <- predict(IFMTrainingModel,type='response')

#BrierScore["AFM"] <- mean((afmpred.prob-mydata$Outcome)^2)
BrierScore["PFM"] <- mean((pfmpred.prob-mydata$Outcome)^2)
#BrierScore["IFM"] <- mean((ifmpred.prob-mydata$Outcome)^2)


#AICc["AFM"] <- -2*(Likelihood["AFM"])+2*NumParameters["AFM"]+(2*NumParameters["AFM"]*(NumParameters["AFM"]+1)/(N-NumParameters["AFM"]-1))
AICc["PFM"] <- -2*(Likelihood["PFM"])+2*NumParameters["PFM"]+(2*NumParameters["PFM"]*(NumParameters["PFM"]+1)/(N-NumParameters["PFM"]-1))
#AICc["IFM"] <- -2*(Likelihood["IFM"])+2*NumParameters["IFM"]+(2*NumParameters["IFM"]*(NumParameters["IFM"]+1)/(N-NumParameters["IFM"]-1))




logLoss <- function(pred, actual){
  -mean(actual * log(pred) + (1 - actual) * log(1 - pred))}




#LogLoss["AFM"] <- logLoss(pred = afmpred.prob,actual = mydata$Outcome)
LogLoss["PFM"] <- logLoss(pred = pfmpred.prob,actual = mydata$Outcome)
#LogLoss["IFM"] <- logLoss(pred = ifmpred.prob,actual = mydata$Outcome)



#print(Models_AIC)
#print(Models_BIC)
#print(NumParameters)
#print(Likelihood)
#print(BrierScore)
#print(LogLoss)


#AFMTrainingModel$coefficients
Model_type <- paste("R_",Model_type,sep="")
exportdf <- cbind(Model_type,Models_AIC,AICc,Models_BIC,NumParameters,Likelihood,BrierScore,LogLoss,RMSE,ACCcv,Precision,Recall,F1)


#write(exportdf,stdout())
write.csv(ModelPredictions, predictionfilepath, row.names=FALSE)
write.csv(exportdf, outputfilelocation, row.names=FALSE)
write.csv(coef(PFMTrainingModel), coefficientfilelocation,row.names=TRUE)

quit(status=0)