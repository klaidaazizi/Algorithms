#quicksort algorithm

def quicksort(Arr,beg,end):
  if beg < end: 
    q = partition(Arr,beg,end) #find the partition 
    quicksort(Arr,beg,q-1) #recurse left side of partition
    quicksort(Arr,q+1,end) #recurse right side of partition

def partition(A,beg,end):
  value = A[end] #pick last value as partition value
  i = beg - 1 #begin keeping track of values smaller than partition
  for j in range(beg, end - 1): #loop through each ele until the second to last
    if A[j] <= value: #if smaller than value of partition, increase i 
      i = i + 1
      temp = A[i] #exchange A[i] with A[j]
      A[i] = A[j]
      A[j] = temp 
  # if value is larger than partition, exchange i + 1 with end
  t = A[i+1] 
  A[i+1] = A[end] 
  A[end] = t
  return i+1
