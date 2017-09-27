public class eightQueen {

    public static boolean solve(int[][] a, int c) {
    	if(c >= a.length) return true;

    	for(int i = 0; i < a.length; i++) {
    		if(canPlace(a, i, c)) {
    			a[i][c] = 1;

    		if(solve(a, c+1)) return true;



    		//	a[i][c] = 0;


    		}
    	}

    	return false;
    }

    public static boolean canPlace(int[][] a, int row, int column) {
    	//check the column , lower diag , upper diag
    	int i, j;
    	for(i = 0; i < column; i++)
    		if(a[row][i]==1) return false; //checking column

    	for(i = row, j = column;  i>=0 && j>=0; i--, j--)//when it hits the side wall or top, stop
    		if(a[i][j]==1) return false; 	//checking upper diag <^

    	for(i = row, j = column; i < a.length && j>=0; i++, j--)//when it hits the side wall or bottom, stop
    		if(a[i][j]==1) return false; 	//checking lower diag <v

    		return true;
    }

    public static void solver(int[][] a) {
    	if(solve(a,0)) printArray(a);
    	else System.out.println("cannot be solved");
    }

    public static void printArray(int[][] a) {
    	for(int i = 0; i < a.length; i++) {
    	    for(int j = 0; j < a.length; j++) {
    		System.out.print(a[i][j]+" ");
    		}
    		System.out.println();
    	}
    }



    public static void main(String[]args) {
    	int n = 8;
		int[][] a = new int[n][n];
		solver(a);

    }

}