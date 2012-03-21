library (RPostgreSQL)

drv <- dbDriver ('PostgreSQL')
icare <- dbConnect (drv, dbname='icare', user='devlop', password='D9e$45VneW', host='85.14.157.162')
dbSendQuery (icare, "SET search_path = pg_catalog;")

relname <- 'emissions_unitaire_combustion_fabrication'
refobjid <- '57548'
refclassid <- '1259'

dbGetDeps <- function (refobjid, refclassid, db)
{
	fetch (dbSendQuery (db, sprintf ("
	       SELECT d.classid
	            , d.objid
	       FROM pg_depend d
	       WHERE refclassid=%s
	       AND refobjid=%s;", refclassid, refobjid)),
	       -1)
}

deps <- dbGetDeps (refobjid, refclassid, icare)
in.pg_class <- deps[deps$classid == '1259',]

while ()
{
	deps <- lapply (parse (text=sprintf ('dbGetDeps(%s, %s, icare)', deps$objid, deps$classid)), eval)
	deps <- data.frame (classid	= unlist(lapply (deps, '[[', 'classid')),
			    objid	= unlist(lapply (deps, '[[', 'objid')))
	in.pg_class <- rbind (in.pg_class, deps[deps$classid == '1259',])
}


