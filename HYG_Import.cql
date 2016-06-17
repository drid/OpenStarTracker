//Set constraints
CREATE CONSTRAINT ON (s:Star) ASSERT s.id IS UNIQUE;
CREATE CONSTRAINT ON (sp:Spectrum) ASSERT sp.spectrum IS UNIQUE;
CREATE CONSTRAINT ON (ci:colorIndex) ASSERT ci.index IS UNIQUE;

//Load Stars w rel color/spectrum
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///HYG-Database/hygdata_v3.csv' AS line
WITH line, line.proper AS Star,
CASE line.spect WHEN NULL THEN '_NA' ELSE line.spect END AS Spectrum,
CASE line.ci WHEN NULL THEN '_NA' ELSE TOINT(line.ci) END AS ColorIndex,
CASE line.con WHEN NULL THEN '_NA' ELSE line.con END AS Constellation

CREATE (star: Star {
  id: TOINT(line.id),
  name: Star,
  RA: TOFLOAT(line.ra),
  RADeg: TOFLOAT(line.ra)*15,
  Declination: TOFLOAT(line.dec),
  Distance: TOFLOAT(line.dist),
  Magnitude: TOFLOAT(line.mag),
  X: TOFLOAT(line.x),
  Y: TOFLOAT(line.y),
  Z: TOFLOAT(line.z)
  })

MERGE (spectrum: Spectrum {spectrum: Spectrum})
CREATE (spectrum)-[:OF]->(star)

MERGE (colorIndex: ColorIndex {index: ColorIndex})
CREATE (colorIndex)-[:OF]->(star)

MERGE (constellation: Constellation {name: Constellation})
CREATE (star)-[:IN]->(constellation)
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
