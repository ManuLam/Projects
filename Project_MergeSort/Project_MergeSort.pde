// MergeSort Project

int step = 0;

void setup() {
int[] array = {10,9,8,7,6,5,4,3,2,1};
 printWholeArray(array);
 array = mergeSort(array);
 
}



int[] mergeSort(int[] A) {
  step++;
  int len = A.length;
  if(len==1) 
    return A;
  
  int n = len/2;
  int[] L = new int[n];
  int[] R = new int[len-n];
  
  for(int i=0; i<len; i++) {
   if(n>i)  
     L[i] = A[i];
   else
     R[i-n] = A[i];
    }
    
    //for(Integer x : A ) 
    //     System.out.printf("%s ",x);
   // System.out.print("Left: "); printAry(L);
  //  System.out.print("Right: "); printAry(R);
    L = mergeSort(L);
    R = mergeSort(R);
    A = merge(L,R);
     printWholeArray(A);
  
  return A;
}

int[] merge(int[] L, int[] R) {
 int nL = L.length , nR = R.length;
 int[] temp = new int[nL+nR];
 int a = 0 , b = 0;
 
 for(int i=0; i<temp.length; i++) {
    if(a>=nL) { 
         temp[i] = R[b];
         b++;
        }
    else if(b>=nR) {
         temp[i] = L[a];
         a++;
        }
    else if(L[a]<R[b]) {
         temp[i] = L[a];
         a++;
        }
    else {
         temp[i] = R[b];
         b++;
        }
     }
     return temp;
}

void printAry(int[] A) {
  
 for(Integer x : A) {
 System.out.printf("%s ", x);
   }
  
}

void printWholeArray(int[] A) {
 println();
 print("Whole Array Step "+step+": ");
 for(Integer x : A) {
 System.out.printf("%s ", x);
   }
// println();
  
}