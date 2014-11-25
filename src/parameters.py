pairSpanCost = dict()

# Parncutt et al. Table 2
pairSpanCost[()] = {0:0}
pairSpanCost[(1, 2)] = {-5:10, -4:7, -3:4, -2:3, -1:2, 1:0, 2:0, 3:0, 4:0, 5:0, 6:1, 7:2, 8:3, 9:6, 10:9}
pairSpanCost[(1, 3)] = {-4:11, -3:8, -2:5, -1:4, 1:2, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:1, 9:2, 10:3, 11:6, 12:9}
pairSpanCost[(1, 4)] = {-3:12, -2:9, -1:6, 1:4, 2:3, 3:2, 4:1, 5:0, 6:0, 7:0, 8:0, 9:0, 10:1, 11:2, 12:3, 13:6, 14:9}
pairSpanCost[(1, 5)] = {-1:12, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1, 7:0, 8:0, 9:0, 10:0, 11:1, 12:2, 13:3, 14:6, 15:9}
pairSpanCost[(2, 3)] = {1:0, 2:0, 3:2, 4:6, 5:10}
pairSpanCost[(2, 4)] = {1:4, 2:2, 3:0, 4:0, 5:2, 6:6, 7:10}
pairSpanCost[(2, 5)] = {2:6, 3:4, 4:2, 5:0, 6:0, 7:2, 8:4, 9:8, 10:12}
pairSpanCost[(3, 4)] = {1:0, 2:0, 3:4, 4:8}
pairSpanCost[(3, 5)] = {1:4, 2:2, 3:0, 4:0, 5:2, 6:6, 7:10}
pairSpanCost[(4, 5)] = {1:0, 2:0, 3:2, 4:6, 5:10}

# Pair span costs not defined in Table 2, but calculated using the same rules (rules 1 through 3
# with regard to Table 1).
pairSpanCost[(1, 2)][0] = 1
pairSpanCost[(1, 3)][0] = 3
pairSpanCost[(1, 4)][0] = 5
pairSpanCost[(1, 5)][0] = 9
pairSpanCost[(2, 3)][0] = 4
pairSpanCost[(2, 4)][0] = 8
pairSpanCost[(2, 5)][1] = 10
pairSpanCost[(2, 5)][0] = 14
pairSpanCost[(3, 4)][0] = 4 # This cost may be too high.
pairSpanCost[(3, 4)][-1] = 8 # This cost may be too high.
pairSpanCost[(3, 4)][-2] = 12 # This cost may be too high.
pairSpanCost[(3, 5)][0] = 8 # This cost may be too high.
pairSpanCost[(3, 5)][-1] = 12 # This cost may be too high.
pairSpanCost[(3, 5)][-2] = 16 # This cost may be too high.
pairSpanCost[(4, 5)][0] = 4 # This cost may be too high.
pairSpanCost[(4, 5)][-1] = 8 # This cost may be too high.
pairSpanCost[(4, 5)][-2] = 12 # This cost may be too high.

substitutionCost = 3