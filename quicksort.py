def quicksort(arr,low,high):
  if low < high: 
    q = partition(arr,low,high) #partition 
    quicksort(arr,low,q-1) #recurse left side of partition
    quicksort(arr,q+1,high) #recurse right side of partition

def partition(arr,low,high):
  pivot = arr[high] #pick last value as pivot
  i = low - 1 #begin keeping track of values smaller than pivot
  for j in range(low, high): #loop through each ele until the second to last
    if arr[j] <= pivot: #if smaller than value of pivot, increase i 
      i = i + 1
      arr[i],arr[j] = arr[j],arr[i] #exchange
       
  # if value is larger than pivot, exchange i + 1 with high
  arr[i+1],arr[high] = arr[high],arr[i+1]
  return (i+1)
