seta = {1,2,3,4,5}
setb = {4,5,6,7,8,9}

# intersection
intersection = seta & setb
union = seta | setb
setc = seta-setb

print(f"union is {union}\n intersection is {intersection}\n only a but not b {setc}\n")