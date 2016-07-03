import math
def angularSeparation(keypoint1, keypoint2, r):
  x1, y1 = keypoint1.pt
  x2, y2 = keypoint2.pt
  d = math.sqrt((x1-x2)**2+(y1-y2)**2)
  return math.degrees(2*math.asin(2*d/r))

# compute angular distances
# (for geometrical corrected image)
# r is a factor that must be calibrated to the corresponding image
def create_pairs(keypoints, minAS, maxAS, r):
  pairs = []
  idx=0
  for cntr in range(0, len(keypoints)-1):
    for idx2 in range(idx+1, len(keypoints)):
      phi =angularSeparation(keypoints[idx], keypoints[idx2], r)
      if (phi > minAS) & (phi < maxAS):
        pairs.append((idx,idx2,phi))
        print idx,idx2,phi
        idx=idx2-1
        break
    idx+=1
  return pairs

def query(pairs, pixelRes):
  idx=0
  match="MATCH p=()"
  where="\nWHERE 1=1"
  for pair in pairs:
    match+="-[r"+str(idx)+":DRADEC]->()"
    where+="\nAND ABS(r"+str(idx)+".AngularSeparation - "+str(pair[2])+") < "+str(pixelRes)
    idx+=1
  query=match+" "+where+"\nRETURN p LIMIT 20"
  return query
