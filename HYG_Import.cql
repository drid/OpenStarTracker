//Set constraints
CREATE CONSTRAINT ON (s:Star) ASSERT s.id IS UNIQUE;
CREATE CONSTRAINT ON (sp:Spectrum) ASSERT sp.spectrum IS UNIQUE;
CREATE CONSTRAINT ON (ci:colorIndex) ASSERT ci.index IS UNIQUE;

//Load All Data
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///HYG-Database/hygxyz-subset.csv' AS line
WITH line, line.ProperName AS Star,
CASE line.Spectrum WHEN NULL THEN '_NA' ELSE line.Spectrum END AS Spectrum,
CASE line.ColorIndex WHEN NULL THEN '_NA' ELSE line.ColorIndex END AS ColorIndex

CREATE (star: Star {
  id: TOINT(line.StarID),
  name: line.ProperName,
  RA: TOFLOAT(line.RA),
  RADeg: TOFLOAT(line.RA)*15,
  Declination: TOFLOAT(line.Dec),
  Distance: TOFLOAT(line.Distance),
  Magnitude: TOFLOAT(line.Mag),
  X: TOFLOAT(line.X),
  Y: TOFLOAT(line.Y),
  Z: TOFLOAT(line.Z)
  })

MERGE (spectrum: Spectrum {spectrum: Spectrum})
CREATE (spectrum)-[:OF]->(star)

MERGE (colorIndex: ColorIndex {index: ColorIndex})
CREATE (colorIndex)-[:OF]->(star)
;

//Calulate DRA DDec
MATCH (n:Star)
  MATCH(ns:Star)
  WHERE ns.id > n.id
    AND ABS(n.RADeg-ns.RADeg) < 3
    AND ABS(n.Declination-ns.Declination) < 3
    AND n.Magnitude < 6
    AND ns.Magnitude < 6
  CREATE (n)-[:DRADEC {
    DRA: (n.RADeg-ns.RADeg),
    DDeclination: n.Declination-ns.Declination,
    DA: acos(sin(n.Declination*pi()/180)*sin(ns.Declination*pi()/180) +
      cos(n.Declination*pi()/180)*cos(ns.Declination*pi()/180)*cos(n.RADeg*pi()/180 - ns.RADeg*pi()/180))*180/pi()
    }]->(ns)
  CREATE (ns)-[:DRADEC {
    DRA: (n.RADeg-ns.RADeg),
    DDeclination: n.Declination-ns.Declination,
    DA: acos(sin(n.Declination*pi()/180)*sin(ns.Declination*pi()/180) +
      cos(n.Declination*pi()/180)*cos(ns.Declination*pi()/180)*cos(n.RADeg*pi()/180 - ns.RADeg*pi()/180))*180/pi()
    }]->(n)
