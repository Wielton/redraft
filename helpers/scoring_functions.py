def yd_pts(yds):
    pts = 0
    if yds <= 19:
        pts = 0
    elif yds >= 20 and yds <= 39:
        pts = 1
    elif yds >= 40 and yds <= 59:
        pts = 2
    elif yds >= 60 and yds <= 79:
        pts = 3
    elif yds >= 80 and yds <= 99:
        pts = 4
    elif yds >= 100 and yds <= 119:
        pts = 5
    elif yds >= 120 and yds <= 149:
        pts = 10
    elif yds >= 150 and yds <= 199:
        pts = 15
    print(pts)
    

def pass_yd_pts(yds):
    pts = 0
    if yds <= 49:
        pts = 0
    elif yds >= 50 and yds <= 99:
        pts = 1
    elif yds >= 100 and yds <= 149:
        pts = 2
    elif yds >= 150 and yds <= 199:
        pts = 3
    elif yds >= 200 and yds <= 249:
        pts = 4
    elif yds >= 250 and yds <= 274:
        pts = 5
    elif yds >= 275 and yds <= 304:
        pts = 10
    elif yds >= 305 and yds <= 349:
        pts = 15
    print(pts)
    

def td_pts(tds):
    pts = 0
    if tds == 0:
        pts = 0
    elif tds == 1:
        pts = 6
    elif tds == 2:
        pts = 12
    elif tds == 3:
        pts = 18
    elif tds == 4:
        pts = 24
    elif tds == 5:
        pts = 30
    elif tds == 6:
        pts = 36
    elif pts == 7:
        pts = 42
    print(pts)
    
