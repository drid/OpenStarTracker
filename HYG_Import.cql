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
  RARad: TOFLOAT(line.rarad),
  Declination: TOFLOAT(line.dec),
  DecRad: TOFLOAT(line.decrad),
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
MATCH (n:Star),(ns:Star)
  WHERE ns.id > n.id
    AND n.Magnitude <= 5
    AND ns.Magnitude <= 5
  WITH n,ns,
    DEGREES(
      ATAN(
        (SQRT((cos(ns.DecRad)^2)*(sin(ns.RARad-n.RARad)^2)+
          (cos(n.DecRad)*sin(ns.DecRad)-sin(n.DecRad)*cos(ns.DecRad)*cos(ns.RARad-n.RARad)))) /
        (sin(n.DecRad)*sin(ns.DecRad)+cos(n.DecRad)*cos(ns.DecRad)*cos(ns.RARad-n.RARad))
        )
      ) AS AngSep
    WHERE AngSep > 6
      AND AngSep < 40
    CREATE (n)-[:DRADEC {
      AngularSeparation: AngSep
      }]->(ns)
    CREATE (ns)-[:DRADEC {
      AngularSeparation: AngSep
      }]->(n)
