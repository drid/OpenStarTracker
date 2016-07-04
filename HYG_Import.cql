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
MATCH (n:Star),(n2:Star)
  WHERE n2.id > n.id
    AND n.Magnitude <= 5
    AND n2.Magnitude <= 5
  WITH n,n2,
    DEGREES(
      ATAN(
        (SQRT((cos(n2.DecRad)^2)*(sin(n2.RARad-n.RARad)^2)+
          (cos(n.DecRad)*sin(n2.DecRad)-sin(n.DecRad)*cos(n2.DecRad)*cos(n2.RARad-n.RARad))^2)) /
        (sin(n.DecRad)*sin(n2.DecRad)+cos(n.DecRad)*cos(n2.DecRad)*cos(n2.RARad-n.RARad))
        )
      ) AS AngSep
    WHERE AngSep > 6
      AND AngSep < 40
    CREATE (n)-[:DRADEC {
      AngularSeparation: AngSep
      }]->(n2)
    CREATE (n2)-[:DRADEC {
      AngularSeparation: AngSep
      }]->(n)

// Spample query for UMa
// Relation match ABS no param
MATCH p=()-[r:DRADEC]->()-[r2:DRADEC]->()-[r3:DRADEC]->() -[r4:DRADEC]->()
WHERE ABS(r.AngularSeparation - 25.7) < .046 //1-7
  AND ABS(r2.AngularSeparation - 10.2) < .046 //7-4
  AND ABS(r3.AngularSeparation - 10.1) < .046 //4-6
  AND ABS(r4.AngularSeparation - 15.5) < .046 //6-3
RETURN p LIMIT 30
