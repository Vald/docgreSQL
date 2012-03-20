--# @title Table contenant les données de communes pour l'agglo d'Angoulême
--# @name agglomeration_angouleme commune
--# @depends departement_16 commune
--# @field gid int identifiant spatial (géométrique)
--# @field id varchar(12) identifiant textuel
--# @field prec_plani double ???
--# @field nom varchar(45) nom de la commune
--# @field code_insee varchar(5) code affecté à l acommune par l'INSEE
--# @field statut varchar(20) chef-lieu, préfecture, ou pas, ou autre.
--# @field canton varchar(45) canton auquel appartient la commune
--# @field arrondisst varchar(45) arrondissement (si pertinent)
--# @field depart varchar(30) depart auquel appartient la commune
--# @field region varchar(30) region à laquelle appartient la commune
--# @field popul int population de la commune (année ?)
--# @field multican varchar(3) ???
--# @field the_geom geometry définition de l'emprise de chaque commune

CREATE OR REPLACE VIEW agglomeration_angouleme.commune AS (
SELECT *
	FROM departement_16.commune
	WHERE nom IN ('Angoulme','Flac','Gond-Pontouvre','La Couronne','Linars','L''Isle-d''Espagnac','Magnac-sur-Touvre','Nersac','Puymoyen','Ruelle-sur-Touvre','Saint-Michel','Saint-Saturnin','Saint-Yrieix-sur-Charente','Soyaux','Touvre')
);

--# @title Table définissant le contour de l'agglo d'Angouleme
--# @name agglomeration_angouleme contour
--# @depends agglomeration_angouleme commune
--# @field the_geom geometry définition de l'emprise de l'agglo

DROP TABLE IF EXISTS agglomeration_angouleme.contour;
CREATE TABLE agglomeration_angouleme.contour (gid serial4 PRIMARY KEY, the_geom geometry NOT NULL);
TRUNCATE TABLE agglomeration_angouleme.contour;
INSERT INTO agglomeration_angouleme.contour (the_geom)
	SELECT ST_Union (the_geom) the_geom FROM agglomeration_angouleme.commune;
