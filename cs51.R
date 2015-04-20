library(XML)
URLpart1 = "http://www.basketball-reference.com/leagues/NBA_"
URLpart3 = "_games.html"
for(i in 1972:2015){
  URL = paste(URLpart1, i, URLpart3, sep = "")
  tablefromURL = readHTMLTable(URL)
  table = tablefromURL[[1]] 
  write.csv(table,paste("games",i,".csv",sep=""))
}


